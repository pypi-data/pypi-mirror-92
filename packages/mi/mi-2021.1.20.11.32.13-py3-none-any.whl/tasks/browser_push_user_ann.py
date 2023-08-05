#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : user_ann
# @Time         : 2021/1/7 2:17 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.db import ann
from meutils.np_utils import normalize
from meutils.date_utils import date_difference

from milvus import DataType
from mi.db import Mongo, Hive
from mi.bot import feishu_send

mongo = Mongo()
browser_push_user_ann = mongo.db.browser_push_user_ann

ann = ann.ANN('10.119.12.139')

# Create collection
collection_name = 'browser_push_user_ann'

collection_param = {

    "fields": [
        {"name": "part", "type": DataType.INT32},
        {"name": "vec", "type": DataType.FLOAT_VECTOR, "params": {"dim": 256}},
    ],
    "segment_row_limit": 4096,
    #         "auto_id": False
}

# Path
file = 'browser_push_user_ann_data'
hdfs = "~/infra-client/bin/hdfs --cluster zjyprc-hadoop dfs"
in_path = "/user/h_browser/weizhang/profile/br/user_embedding"

# download data from hdfs
date = date_difference('%Y%m%d', days=1)
is_success = os.popen(f"{hdfs} -test -e {in_path}/date={date}/_SUCCESS && echo $?").read().strip()  # 判断文件是否存在
if is_success:

    logger.info("Create collection")
    ann.create_collection(collection_name, collection_param)
    ann.create_index(collection_name, 'vec')

    logger.info("Download data from hdfs")
    if not Path(file).exists():
        os.system(f"{hdfs} -get {in_path}/date={date} {file}")

    for i, p in tqdm(enumerate(Path(file).glob('*parquet'))):
        df = pd.read_parquet(p)

        vecs = normalize(np.row_stack(df.userEmbedding)).tolist()

        entities = [
            {"name": "vec", "type": DataType.FLOAT_VECTOR, "values": vecs},
            {"name": "part", "type": DataType.INT32, "values": [i] * len(df)},
        ]

        df['id'] = ann.batch_insert(collection_name, entities, 200000)
        df['date'] = datetime.datetime.utcnow()

        browser_push_user_ann.insert_many(df[['id', 'userId', 'date']].to_dict('r'), False)

    logger.info("rm data")
    os.system(f"rm -rf {file}")



else:
    feishu_send({"title": collection_name, "text": "Embedding数据未生成"})
