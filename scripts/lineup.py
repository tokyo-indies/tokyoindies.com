#!/usr/bin/env python
# generate social media posts
import csv
import sys
import re

from util import read_tsv


def post_twitter(intro, presentations):
    out = intro + "\n\n"
    for presen in presentations:
        title = presen["title"]
        handle = presen["twitter"]
        if not handle:
            handle = "/ " + presen["name"]
        out += f"- {title} {handle}\n"

    return out


def post_bluesky(intro, presentations):
    out = intro + "\n\n"

    for presen in presentations:
        title = presen["title"]
        if link := presen["homepage"]:
            title = f"[{title}]({link})"
        handle = presen.get("bluesky")
        if not handle:
            handle = "/ " + presen["name"]

        out += f"- {title} {handle}\n"

    return out


def post_discord(intro, presentations):
    out = intro + "\n\n"

    for presen in presentations:
        title = presen["title"]
        handle = presen["discord"] or presen["name"]
        if link := presen["homepage"]:
            title = f"[{title}]({link})"
        if pv := presen["pv"]:
            handle += f" [(PV)]({pv})"
        out += f"- {title} {handle}\n"

    return out


def post_html(intro, presentations):
    out = intro + "\n\n"

    for presen in presentations:
        title = presen["title"]
        handle = presen["name"]
        if link := presen["homepage"]:
            title = f"[{title}]({link})"
        if pv := presen["pv"]:
            handle += f" [(PV)]({pv})"
        out += f"- {title} {handle}\n"

    return out


def main():

    intro = "今月の紹介作品:"

    # 0. read in tsv
    with open(sys.argv[1]) as tsvfile:
        presentations = read_tsv(tsvfile)

    # 1. twitter
    print("----- twitter -----")
    print(post_twitter(intro, presentations))

    # 2. bluesky
    print()
    print("----- bluesky -----")
    print(post_bluesky(intro, presentations))

    # 3. discord
    print()
    print("----- discord -----")

    print(post_discord(intro, presentations))

    print()
    print("----- html -----")
    print(post_html(intro, presentations))


if __name__ == "__main__":
    main()
