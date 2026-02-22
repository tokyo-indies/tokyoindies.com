#!/usr/bin/env python
# generate social media posts
import csv
import sys

def remap(row):

    remapper = {"プレゼンター名": "name",
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
    out["bluesky"] = out["bluesky"].replace("https://bsky.app/profile/", "@")
    out["discord"] = ("@" + out["discord"]) if out["discord"] else ""
    return out


def main():

    # 0. read in tsv
    presentations = []
    with open(sys.argv[1]) as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in reader:
            if row["Status"] != "Confirmed":
                continue
            presentations.append(remap(row))

    # 1. twitter
    print("----- twitter -----")
    print("今月の作品:")
    print()

    for presen in presentations:
        title = presen["title"]
        handle = presen["twitter"]
        if not handle:
            handle = "/ " + presen["name"]
        print(f"- {title} {handle}")


    # 2. bluesky
    print()
    print("----- bluesky -----")
    print("今月の作品:")
    print()

    for presen in presentations:
        title = presen["title"]
        if link := presen["homepage"]:
            title = f"[{title}]({link})"
        handle = presen.get("bluesky")
        if not handle:
            handle = "/ " + presen["name"]
        
        print(f"- {title} {handle}")

    # 3. discord
    print()
    print("----- discord -----")
    print("今月の作品:")
    print()

    for presen in presentations:
        title = presen["title"]
        handle = presen["discord"] or presen["name"]
        if link := presen["homepage"]:
            title = f"[{title}]({link})"
        if pv := presen["pv"]:
            handle += f" [(PV)]({pv})"
        print(f"- {title} {handle}")
    
    print()
    print("----- html -----")
    print("今月の作品:")
    print()

    for presen in presentations:
        title = presen["title"]
        handle = presen["name"]
        if link := presen["homepage"]:
            title = f"[{title}]({link})"
        if pv := presen["pv"]:
            handle += f" [(PV)]({pv})"
        print(f"- {title} {handle}")

if __name__ == "__main__":
    main()
