import argparse
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_dt
import toml
from tabulate import tabulate
import json

# Default pattern matches most version strings for final versions, such as
# v.1.0.0, v1.0.0, 1.0.0, version-1.0.0, release-1.0.0
DEFAULT_VERSION_PATTERN = re.compile(r"^.*?(\d+\.\d+\.\d+)$")


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
    re_version: re.Pattern = DEFAULT_VERSION_PATTERN,
    n_min: int = None,
):
    versions, after = _fetch_releases(gh_user, gh_project, re_version)
    if n_min is not None:
        while len(versions) < n_min:
            nv, after = _fetch_releases(gh_user, gh_project, re_version, after=after)
            versions.extend(nv)
    return versions


def main(args):
    cfg = toml.load(open(args.config))
    repos = cfg["repos"]["github"]
    latest_versions = []
    for repo, pattern in repos.items():
        gh_user, gh_project = repo.split("/")
        regex = DEFAULT_VERSION_PATTERN if pattern == "default" else re.compile(pattern)
        latest = fetch_releases(gh_user, gh_project, re_version=regex, n_min=1)[0]
        latest_versions.append(
            {
                "host": "github.com",
                "repository": repo,
                "latest_version": latest["version"],
                "updated": latest["updated"].date().isoformat(),
            }
        )

    latest_versions.sort(key=lambda row: row["repository"])
    if args.format == "print":
        arr = [
            [item["repository"], item["latest_version"], item["updated"], item["host"]]
            for item in latest_versions
        ]
        print(tabulate(arr, headers=["Repo", "Latest Version", "Updated at", "Host"]))
    elif args.format == "json":
        print(json.dumps(latest_versions))


def run():
    parser = argparse.ArgumentParser(
        "release-check", description="Check releases on Github"
    )
    parser.add_argument("--config", "-c", required=True, help="Configuration file")
    parser.add_argument(
        "--format", default="print", choices=["print", "json"], help="Output format"
    )
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    run()