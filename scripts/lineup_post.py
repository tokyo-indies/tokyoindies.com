import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import os

from lineup import post_markdown
from util import read_tsv

def main():
    parser = argparse.ArgumentParser(
        prog="lineup_post",
        description="Make posts about the lineup"
    )
    parser.add_argument("tsv", help="presenter tsv") 
    parser.add_argument("-t", "--twitch", help="twitch link") 
    parser.add_argument(
        "-n", "--dryrun", action="store_true", help="Do not write files"
    )
    
    args = parser.parse_args()
    
    jst = ZoneInfo("Asia/Tokyo")
    now = datetime.now(jst)

    with open(args.tsv) as tsvfile:
        presentations = read_tsv(tsvfile)

    shortdate = now.strftime("%Y%m")
    ja_content = post_markdown("", presentations).strip()
    japost = f"""---
title: "{now.year}年{now.month}月のTokyo Indiesで紹介されたゲーム"
date: {now}
draft: false
featured_image: "img/tokyo-indies-{shortdate}.png"
---

![Monthly presenter lineup](/img/tokyo-indies-{shortdate}.png)

今月紹介されたゲームは以下の通りです。

{ja_content}

今回のプレゼンは[Twitch]({args.twitch})で配信しています。また来月アキバで会いましょう！
"""
    en_content = post_markdown("", presentations).strip()
    mname = now.strftime("%B")
    enpost = f"""---
title: "Games Shown at {mname} {now.year} Tokyo Indies"
date: {now}
draft: false
featured_image: "img/tokyo-indies-{shortdate}.png"
---

![Monthly presenter lineup](/img/tokyo-indies-{shortdate}.png)

Games shown this month:

{en_content}

A recording of the presentations is also [viewable on Twitch]({args.twitch}). See you next month!
"""

    if not args.dryrun:
        # XXX This is a hack to make sure we're in the right directory.
        # Realistically this will only be run from root or scripts/.
        if Path.cwd().name == "scripts":
            os.chdir("..")

        assert Path("./content/ja/posts").is_dir(), "Please run from the source dir"
        isodate = now.isoformat()[:7]
        with open(f"./content/ja/posts/{isodate}-lineup.md", "w") as ofile:
            ofile.write(japost)
        with open(f"./content/en/posts/{isodate}-lineup.md", "w") as ofile:
            ofile.write(enpost)
    print("Generated lineup posts")
    print("Remember to edit English if game titles or author names are in Japanese!")

if __name__ == "__main__":
    main()
