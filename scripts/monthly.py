#!/usr/bin/env python
from datetime import date, timedelta, datetime
import calendar
from zoneinfo import ZoneInfo

import argparse


def get_third_wed(dd=None):
    if dd is None:
        # get the date two weeks in the future, which should be the same month as
        # the next event, probably. Use that to get the third wednesday.
        dd = date.today() + timedelta(days=14)

    base = date(dd.year, dd.month, 1)
    while base.weekday() != calendar.WEDNESDAY:
        base += timedelta(days=1)

    # skip two weeks
    base += timedelta(days=14)
    return base


def main():

    parser = argparse.ArgumentParser(
        prog="monthly", description="Generate monthly event posts"
    )
    parser.add_argument(
        "date", help="day of the event in iso format (ex: 2026-01-18)", nargs="?"
    )
    parser.add_argument(
        "-n", "--dryrun", action="store_true", help="Do not write files"
    )

    args = parser.parse_args()

    base = args.date
    if args.date is not None:
        event = datetime.fromisoformat(args.date)
    else:
        event = get_third_wed()

    # if the timezone is not supplied, Python generates an object with no
    # timezone information. This results in an ISO datetime with no timezone
    # info, which is valid in general, but Hugo won't publish the post T_T
    jst = ZoneInfo("Asia/Tokyo")
    now = datetime.now(jst).isoformat(timespec="seconds")

    japost = f"""---
title: "{event.year}年{event.month}月のTokyo Indies"
date: {now}
draft: false
---

次のTokyo Indiesは{event.month}月{event.day}日開催です。

プレゼンを募集しています。詳細については[プレゼン申込みエージ](/present)をご確認ください。
"""

    mname = event.strftime("%B")  # "January" etc.
    enpost = f"""---
title: "{mname} {event.year} Tokyo Indies"
date: {now}
draft: false
---

The next Tokyo Indies will be held on {mname} {event.day}.

We're accepting presentations on the [presentation page](/en/present).
"""
    print("----- japanese -----")
    print(japost)
    print("----- english -----")
    print(enpost)
    if not args.dryrun:
        isodate = event.isoformat()[:7]
        with open(f"./content/ja/posts/{isodate}.md", "w") as ofile:
            ofile.write(japost)
        with open(f"./content/en/posts/{isodate}.md", "w") as ofile:
            ofile.write(enpost)

    print("----- for socials -----")
    social = """次回のTokyo Indiesは{event.month}月{event.day}日開催です。

会場：MOGRA（秋葉原） 
開催時間：19:00 - 23:00（プレゼンは20:30～）
入場料：1500円 (1ドリンク付き)

プレゼン申請はこちらから。 
http://tokyoindies.com/present/
"""
    print(social)


if __name__ == "__main__":
    main()
