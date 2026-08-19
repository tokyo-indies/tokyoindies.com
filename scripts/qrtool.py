import argparse
import qrcode
import io
import re

from lineup import read_tsv

import requests
from PIL import Image
from fpdf import FPDF


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
        image = Image.new(mode="RGB", size=(400, 400), color="white")
    return image


def make_qr(url):
    """Given a URL, return a pillow image with no border."""
    # Removing the border is weird for some reason
    qr = qrcode.QRCode(border=0)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf


def build_qr_pdf(presenters):
    # presenters are:
    # [image url, qr url, title, author]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", style="B", size=16)
    pdf.image("qr-header.png", w=pdf.epw)
    pdf.ln()

    # units are mm
    height = 40
    margin = 10
    color = "#134f5c"

    pdf.set_text_color(0x13, 0x4F, 0x5C)

    # columns
    c1w = pdf.epw * 0.4
    c2w = pdf.epw * 0.3
    c3w = pdf.epw * 0.3

    for image_url, url, title, author in presenters:
        X = margin
        Y = pdf.get_y()  # will re-use
        # center the image
        img = fetch_image(image_url)
        iinfo = pdf.image(img, h=height, w=c1w, x=X, keep_aspect_ratio=True)
        # iwidth = iinfo.rendered_width
        # pdf.image(ipath, w=c1w, x = (c1w - iwidth) // 2)

        X += c1w
        qr = make_qr(url)
        pdf.image(qr, h=height, x=X + 10, y=Y)

        X += c2w
        pdf.set_xy(X, Y)
        pdf.write_html(f"<center><b>{title}</b><br>{author}</center>")
        pdf.set_xy(margin, Y + height + 2)

    pdf.output("blarg.pdf")


def main():
    parser = argparse.ArgumentParser(
        prog="qrtool", description="Generate QR ref pdf"
    )
    parser.add_argument("tsv")

    args = parser.parse_args()

    with open(args.tsv) as tsvfile:
        presenters = read_tsv(tsvfile)

    clean = []
    for pres in presenters:
        clean.append(
            [
                pres["image"],
                pres["homepage"],
                pres["title"],
                pres["name"],
            ]
        )
    build_qr_pdf(clean)


if __name__ == "__main__":
    main()
