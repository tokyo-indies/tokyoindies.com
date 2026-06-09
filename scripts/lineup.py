#!/usr/bin/env python
# generate social media posts
import csv
import sys
import re


def remap(row):

    remapper = {
        "プレゼンター名": "name",
        "作品名": "title",
        "BlueSky": "bluesky",
        "作者X(Twitter)など": "twitter",
        "作者のDiscordユーザー名": "discord",
        "作品ホームページ": "homepage",
        "PV・紹介動画(可能ならYouTubeで)": "pv",
    }

    out = {}
    for key, val in remapper.items():
        out[val] = row.get(key).strip()

    # fix socials
    out["twitter"] = out["twitter"].replace("https://x.com/", "@")
    # this is old but people still give it to us sometimes
    out["twitter"] = out["twitter"].replace("https://twitter.com/", "@")
    out["bluesky"] = out["bluesky"].replace("https://bsky.app/profile/", "@")
    # If someone puts a username like "@user" that doesn't work
    if out["bluesky"] is not None and "." not in out["bluesky"]:
        out["bluesky"] = out["bluesky"] + ".bsky.social"
    out["discord"] = ("@" + out["discord"]) if out["discord"] else ""

    # remove non-url values like "will send later"
    for key in ("homepage", "pv"):
        if not re.match("https?://", out[key]):
            out[key] = ""
    return out


def read_tsv(tsvfile):
    presentations = []
    reader = csv.DictReader(tsvfile, delimiter="\t")
    for row in reader:
        if row["Status"] != "Confirmed":
            continue
        presentations.append(remap(row))

    return presentations


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
