import argparse
import requests
import re
import toml
from tabulate import tabulate
import json

from .constants import DEFAULT_VERSION_PATTERN
from .utils import fetch_releases


def main_single(args):
    host, repo = args.uri.split(":")
    user, project = repo.split("/")
    versions = fetch_releases(user, project, re_version=re.compile(args.pattern))
    latest_version = versions[0]
    print(latest_version["version"])


def main_batch(args):
    cfg = toml.load(open(args.config))
    repos = cfg["repos"]["github"]
    latest_versions = []
    for repo, pattern in repos.items():
        gh_user, gh_project = repo.split("/")
        regex = (
            re.compile(DEFAULT_VERSION_PATTERN)
            if pattern == "default"
            else re.compile(pattern)
        )
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

    subparsers = parser.add_subparsers(dest="mode", required=True)

    single_parser = subparsers.add_parser("single")
    single_parser.add_argument(
        "uri", help="Resource identifier, e.g. github.com:nextcloud/server"
    )
    single_parser.add_argument(
        "--pattern", default=DEFAULT_VERSION_PATTERN, help="Version regex pattern"
    )

    batch_parser = subparsers.add_parser("batch")
    batch_parser.add_argument(
        "--config", "-c", required=True, help="Configuration file"
    )
    batch_parser.add_argument(
        "--format", default="print", choices=["print", "json"], help="Output format"
    )
    args = parser.parse_args()

    if args.mode == "single":
        main_single(args)
    else:
        main_batch(args)


if __name__ == "__main__":
    run()