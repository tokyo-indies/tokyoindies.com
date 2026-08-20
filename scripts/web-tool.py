import csv
from io import StringIO
import os
from pathlib import Path

import streamlit as st

import lineup
from qrtool import build_qr_pdf

# change working dir to scripts directory
# locally this is usually run from the scripts directory, but Streamlit Cloud
# runs it from repo root
if Path(".").absolute().name == "tokyoindies.com":
    os.chdir("scripts")

st.write(
    """
# Tokyo Indies SNS Post Tool

To use this tool, make sure the presenter application spreadsheet has presenters for this month marked as Confirmed in the Status column. Then download the sheet as a TSV file and upload it here. Content to post on each SNS will show up below."""
)

upfile = st.file_uploader("Upload Presenter CSV")

if upfile is not None:

    strio = StringIO(upfile.getvalue().decode("utf-8"))
    pres = lineup.read_tsv(strio)
    intro = st.text_input("Intro text (you can edit this)", "今月の紹介作品:")

    image = lineup.build_image(pres)
    st.image(image)

    "---"
    st.write("# QR Lineup")

    "Note it takes a second to generate this."

    make_pdf = lambda: bytes(build_qr_pdf(pres).output())
    st.download_button("Download QR Lineup PDF", make_pdf, "tokyo-indies-qr.pdf")

    "---"

    st.write("# Twitter")
    st.code(lineup.post_twitter(intro, pres), language="markdown")
    "---"
    st.write("# BlueSky")
    st.write("To post Markdown on BlueSky, use [deck.blue](https://deck.blue).")
    st.code(lineup.post_bluesky(intro, pres), language="markdown")
    "---"
    st.write("# Discord")
    st.code(lineup.post_discord(intro, pres), language="markdown")
    "---"
    st.write("# HTML (blog post)")
    st.code(lineup.post_markdown(intro, pres), language="markdown")
