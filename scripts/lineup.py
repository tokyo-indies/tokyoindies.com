#!/usr/bin/env python
# generate social media posts
import sys
import re

from util import read_tsv, fetch_image

from PIL import Image, ImageOps

def build_image(presentations):
    # build a composite image with the lineup

    # the final image is 1080x1080 px with 10px borders
    # so each cell is 525x346
    sz = (525, 346)

    images = [fetch_image(pres["image"]) for pres in presentations]
    default = Image.open("banner.png")
    while len(images) < 6:
        images.append(default)
    images = [ImageOps.fit(ii, sz) for ii in images]

    margin = 10
    x = margin
    y = margin
    canvas = Image.new(mode="RGB", size=(1080, 1080), color="white")

    for ii, image in enumerate(images):
        row = ii // 2
        col = ii % 2

        offset = (
                (margin + (col * margin) + (col * sz[0])),
                (margin + (row * margin) + (row * sz[1])),
                 )
        canvas.paste(image, offset)

    return canvas


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

    image = build_image(presentations)
    image.save("lineup.png")


if __name__ == "__main__":
    main()
