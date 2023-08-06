#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : download_video
# @Time         : 2020/12/15 6:18 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

from moviepy.editor import *
from meutils.pipe import *
from mi.db.Hive import Hive
from mi.db import Mongo

from meutils.date_utils import date_difference

from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")

mongo = Mongo()
xindao_ocr = mongo.db.xindao_ocr

conn = Hive('/home/work/keytab/h_browser.keytab').conn

date = date_difference('%Y%m%d', days=1)
sql = f"""
select id, url
from feeds.content_databus_xindao_batch_idx
where date = {date}
and xindaoid is not null
and category[0] is not null
and url like "http%"
and cpApi not like "%fengxing%"
"""

df = pd.read_sql(sql, conn)


def video2picture2text(video='/fds/1_Work/2_DownVideo/videos/互联网_yidian_V_07d0oZik.mp4', top_duration=180):
    p = Path(video)
    pic_dir = ''.join(p.name[::-1].split('.')[-1:])[::-1]
    (p.parent / pic_dir).mkdir(exist_ok=True)

    r = {'items': {}, 'text': ''}
    with VideoFileClip(video) as clip:
        duration = int(clip.duration)
        for i in tqdm(range(min(duration, top_duration))):
            clip_ = clip.subclip(i, i + 1)
            image = p.parent / pic_dir / f'{i}.png'
            clip_.save_frame(image)
            items = ocr.ocr(str(image), cls=True)

            r['items'][str(i)] = items
            for item in items:
                text = item[1][0].strip()
                if text not in r['text']:
                    r['text'] = r['text'] + '\n' + text

    os.system(f"rm -rf {p.parent / pic_dir}")
    return r


def pipeline(row):
    if xindao_ocr.find_one({'id': row.id}) is None:
        os.system(f"wget {row.url} -q -O {row.id}.mp4")

        p = Path(f"{row.id}.mp4")
        if p.exists() and p.stat().st_size / 1024 / 1024 > 1:
            r = video2picture2text(f"{row.id}.mp4")
            r['id'] = row.id
            xindao_ocr.insert_one(eval(str(r)))
        else:
            logger.info(f'下载视频失败{row.id}: {row.url}')


for row in df.itertuples() | xtqdm:
    pipeline(row)
