import csv
import re
import io

import requests
from PIL import Image


def remap(row):

    remapper = {
        "プレゼンター名": "name",
        "作品名": "title",
        "BlueSky": "bluesky",
        "作者X(Twitter)など": "twitter",
        "作者のDiscordユーザー名": "discord",
        "作品ホームページ": "homepage",
        "PV・紹介動画(可能ならYouTubeで)": "pv",
        "告知画像・スクリーンショット": "image",
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


def fetch_image(url):
    # Download an image and give a pillow object
    try:
        # if it's google drive, we need to do some monkey business
        if "drive.google.com" in url:
            match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
            if not match:
                raise ValueError("Invalid Google Drive sharing link format.")

            file_id = match.group(1)
            url = f"https://drive.usercontent.google.com/download?id={file_id}"

        res = requests.get(url)
        image = Image.open(io.BytesIO(res.content))
    except Exception as ee:
        print(ee)
        # TODO write "no image" in the middle
        image = Image.new(mode="RGB", size=(640, 480), color="white")
    return image
