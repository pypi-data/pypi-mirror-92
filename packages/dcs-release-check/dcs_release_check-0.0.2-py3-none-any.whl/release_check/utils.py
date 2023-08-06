import re
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_dt

from .constants import DEFAULT_VERSION_PATTERN


def _normalize_tag(var: str, re_version: re.Pattern):
    groups = re_version.match(var)
    if not groups:
        return None
    return groups[1]


def _fetch_releases(
    gh_user: str, gh_project: str, re_version: re.Pattern, after: str = None
):
    # Request to GitHub, `after` param is used for paging
    r = requests.get(
        f"https://github.com/{gh_user}/{gh_project}/releases.atom",
        params={"after": "" if after is None else after},
    )
    r.raise_for_status()
    html = r.text
    soup = BeautifulSoup(html, features="html.parser")

    versions = []
    after = None
    for tag in soup.find_all("entry"):
        link = tag.find("link")
        updated = parse_dt(tag.find("updated").text)
        href = link.attrs["href"]
        if "tag" not in href:
            continue
        version = href.split("/")[-1]  # last part of URL is the version
        after = version  # keep version string as is for paging
        version = _normalize_tag(version, re_version)
        if version is None:
            continue
        versions.append({"version": version, "updated": updated})

    return versions, after


def fetch_releases(
    gh_user: str,
    gh_project: str,
    re_version: re.Pattern = re.compile(DEFAULT_VERSION_PATTERN),
    n_min: int = None,
):
    versions, after = _fetch_releases(gh_user, gh_project, re_version)
    if n_min is not None:
        while len(versions) < n_min:
            nv, after = _fetch_releases(gh_user, gh_project, re_version, after=after)
            versions.extend(nv)
    return versions