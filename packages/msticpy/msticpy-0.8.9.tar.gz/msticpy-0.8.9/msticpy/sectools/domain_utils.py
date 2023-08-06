# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""

Functions to support investigation of a domain or url.

Includes functions to conduct common investigation steps when dealing
with a domain or url, such as getting a screenshot or validating the TLD.

"""
import json
import ssl
import sys
import time
import warnings
from pathlib import Path
from typing import Set, Tuple, Optional
from urllib.error import HTTPError, URLError

import cryptography as crypto
import dns.resolver
import pandas as pd
import pkg_resources
import requests
import tldextract
from IPython import display
from ipywidgets import IntProgress

from .._version import VERSION
from ..common import pkg_config as config
from ..common.exceptions import MsticpyUserConfigError
from ..common.utility import export

__version__ = VERSION
__author__ = "Pete Bryan"


@export
def screenshot(url: str, api_key: str = None) -> requests.models.Response:
    """
    Get a screenshot of a url with Browshot.

    Parameters
    ----------
    url : str
        The url a screenshot is wanted for.
    api_key : str (optional)
        Browshot API key. If not set msticpyconfig checked for this.

    Returns
    -------
    image_data: requests.models.Response
        The final screenshot request response data.

    """
    # Get Browshot API key from kwargs or config
    if api_key is not None:
        bs_api_key: Optional[str] = api_key
    else:
        bs_conf = config.settings.get("DataProviders", {}).get(
            "Browshot"
        ) or config.settings.get("Browshot")
        bs_api_key = None
        if bs_conf is not None:
            bs_api_key = bs_conf.get("Args", {}).get("AuthKey")  # type: ignore

    if bs_api_key is None:
        raise MsticpyUserConfigError(
            "No configuration found for Browshot",
            "Please add a section to msticpyconfig.yaml:",
            "DataProviders:",
            "  Browshot:",
            "    Args:",
            "      AuthKey: {your_auth_key}",
            title="Browshot configuration not found",
            browshot_uri=("Get an API key for Browshot", "https://api.browshot.com/"),
        )

    # Request screenshot from Browshot and get request ID
    id_string = f"https://api.browshot.com/api/v1/screenshot/create?url={url}/&instance_id=26&size=screen&cache=0&key={bs_api_key}"  # pylint: disable=line-too-long
    id_data = requests.get(id_string)
    bs_id = json.loads(id_data.content)["id"]
    status_string = (
        f"https://api.browshot.com/api/v1/screenshot/info?id={bs_id}&key={bs_api_key}"
    )
    image_string = f"https://api.browshot.com/api/v1/screenshot/thumbnail?id={bs_id}&zoom=50&key={bs_api_key}"  # pylint: disable=line-too-long
    # Wait until the screenshot is ready and keep user updated with progress
    print("Getting screenshot")
    progress = IntProgress(min=0, max=40)
    display.display(progress)
    ready = False
    while ready is False:
        progress.value += 1
        status_data = requests.get(status_string)
        status = json.loads(status_data.content)["status"]
        if status == "finished":
            ready = True
        else:
            time.sleep(0.05)
    progress.value = 40

    # Once ready get the screenshot
    image_data = requests.get(image_string)

    if image_data.status_code != 200:
        print(
            "There was a problem with the request, please check the status code for details"
        )

    return image_data


@export
class DomainValidator:
    """Assess a domain's validity."""

    _tld_index: Set[str] = set()
    _ssl_abuse_list: pd.DataFrame = pd.DataFrame()

    @classmethod
    def _check_and_load_tlds(cls):
        """Pull IANA TLD list and save to internal attribute."""
        if not cls._tld_index:
            cls._tld_index: Set[str] = cls._get_tlds()

    @classmethod
    def _check_and_load_abuselist(cls):
        """Pull IANA TLD list and save to internal attribute."""
        if cls._ssl_abuse_list is None or cls._ssl_abuse_list.empty:
            cls._ssl_abuse_list: pd.DataFrame = cls._get_ssl_abuselist()

    @property
    def tld_index(self) -> Set[str]:
        """
        Return the class TLD index.

        Returns
        -------
        Set[str]
            The current TLD index

        """
        self._check_and_load_tlds()
        return self._tld_index

    @property
    def ssl_abuse_list(self) -> pd.DataFrame:
        """
        Return the class SSL Blacklist.

        Returns
        -------
        pd.DataFrame
            SSL Blacklist

        """
        self._check_and_load_abuselist()
        return self._ssl_abuse_list

    # Leaving as class method for backward compatability
    def validate_tld(self, url_domain: str) -> bool:  # pylint: disable=no-self-use
        """
        Validate if a domain's TLD is valid.

        Parameters
        ----------
        url_domain : str
            The url or domain to validate.

        Returns
        -------
        result:
            True if valid public TLD, False if not.

        """
        _, _, tld = tldextract.extract(url_domain.lower())
        return bool(tld)

    def is_resolvable(self, url_domain: str) -> bool:  # pylint: disable=no-self-use
        """
        Validate if a domain or URL be be resolved to an IP address.

        Parameters
        ----------
        url_domain : str
            The url or domain to validate.

        Returns
        -------
        result:
            True if valid resolvable, False if not.

        """
        try:
            dns.resolver.resolve(url_domain, "A")
            result = True
        except dns.resolver.NXDOMAIN:  # pylint: disable=broad-except
            result = False

        return result

    def in_abuse_list(self, url_domain: str) -> Tuple:
        """
        Validate if a domain or URL's SSL cert the abuse.ch SSL Abuse List.

        Parameters
        ----------
        url_domain : str
            The url or domain to validate.

        Returns
        -------
        result:
            True if valid in the list, False if not.

        """
        try:
            cert = ssl.get_server_certificate((url_domain, 443))
            x509 = crypto.x509.load_pem_x509_certificate(  # type: ignore
                cert.encode("ascii")
            )
            cert_sha1 = x509.fingerprint(
                crypto.hazmat.primitives.hashes.SHA1()  # type: ignore # nosec
            )
            result = bool(
                self.ssl_abuse_list["SHA1"]
                .str.contains(cert_sha1.hex())
                .any()  # type: ignore
            )
        except Exception:  # pylint: disable=broad-except
            result = False
            x509 = None

        return result, x509

    @classmethod
    def _get_tlds(cls) -> Set[str]:
        """
        Return IANA Top Level Domains.

        Returns
        -------
        Set[str]
            Set of top level domains.

        """
        try:
            tld_list = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
            temp_df = pd.read_csv(tld_list, skiprows=1, names=["TLD"])
            return set(temp_df["TLD"].dropna())
        except (HTTPError, URLError):
            pass
        except Exception as err:  # pylint: disable=broad-except
            warnings.warn(
                "Exception detected trying to retrieve IANA top-level domain list."
                + "Falling back to builtin seed list. "
                + f"{err.args}",
                RuntimeWarning,
            )
        # pylint: enable=broad-except
        # if we failed to get the list try to read from a seed file
        return cls._read_tld_seed_file()

    @classmethod
    def _read_tld_seed_file(cls) -> Set[str]:
        """Read TLD seed list from seed file."""
        seed_file = "tld_seed.txt"
        conf_file = pkg_resources.resource_filename(__name__, seed_file)

        if not Path(conf_file).is_file():
            # if all else fails we try to find the package default config somewhere
            # in the package tree - we use the first one we find
            pkg_paths = sys.modules["msticpy"]
            if pkg_paths:
                conf_file = str(
                    next(Path(pkg_paths.__path__[0]).glob(seed_file))  # type: ignore
                )

        if conf_file:
            with open(conf_file, "r") as file_handle:
                tld_txt = file_handle.read()
                tld_set = set(tld_txt.split("\n"))
            return tld_set
        return set()

    @classmethod
    def _write_tld_seed_file(cls):
        """Write existing TLD list to a text file."""
        if cls._tld_index:
            seed_file = "tld_seed.txt"
            with open(seed_file, "w") as file_handle:
                file_handle.write("\n".join(sorted(cls.tld_index)))

    @classmethod
    def _get_ssl_abuselist(cls) -> pd.DataFrame:
        """Download and load abuse.ch SSL Abuse List."""
        try:
            ssl_ab_list = pd.read_csv(
                "https://sslbl.abuse.ch/blacklist/sslblacklist.csv", skiprows=8
            )
        except (ConnectionError, HTTPError, URLError):
            ssl_ab_list = pd.DataFrame({"SHA1": []})

        return ssl_ab_list
