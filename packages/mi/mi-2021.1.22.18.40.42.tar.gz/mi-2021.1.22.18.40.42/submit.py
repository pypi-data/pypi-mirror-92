#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : submit
# @Time         : 2020/11/23 4:03 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.models.train_job import TrainJob


client = CloudMlClient(
    access_key='AKO6GF5GAN5COTD6VM',
    secret_key='x5/uE1eb+kmeOeIDR3O+Ibu6ugQY2xIQ8pGTv5R9',
    endpoint='https://cnbj5-cloud-ml.api.xiaomi.net'
)

# client.submit_train_job(open('hvd_tf2keras_mnist.json').read())


train_job = TrainJob(
    prepare_command="pip install -U --no-cache-dir -i https://pypi.python.org/pypi meutils",
    # framework='tensorflow',
    # framework_version='2.3.1-xm1.0.0-py3',
    docker_image='cr.d.xiaomi.net/cloud-ml/devsave:33103-cpu666',

    hdfs_krb_account='h_browser@XIAOMI.HADOOP',
    hdfs_krb_keytab='tql',
    hdfs_endpoint='hdfs://zjyprc-hadoop',

    job_name='xx',
    module_name='tasks.cloudml.hdfs2fds',

    cpu_limit='4',
    memory_limit='4G',
    priority_class='best-effort',  # guaranteed or best-effort
    trainer_uri='./',
    fds_endpoint='cnbj1-fds.api.xiaomi.net',
)

client.submit_train_job(train_job.get_json_data())
