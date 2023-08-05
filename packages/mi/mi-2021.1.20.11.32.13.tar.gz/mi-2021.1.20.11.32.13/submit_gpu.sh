#!/usr/bin/env bash
DATA=`date +'%Y%m%d-%H-%M-%S'`

if [ -n "$2" ]
then taget_name=$2
else taget_name="tql$DATA"
fi;

project_name=$1 # 主程序命名项目名
#if cloudml jobs delete $project_name | grep "Successfully";
#then echo "删除 ..." && sleep 18s;
#fi;

cloudml jobs submit \
-n $taget_name \
-m $project_name \
-u ./ \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-cpu666 \
-fc "ls" \
-pc "pip install -U meutils" \
--priority_class "best-effort" \
-c 30 -M 99G \
-g 1 -gt v100 -gm 32g


# -a "--data-dir=/fds/cifar-10-data --job-dir=/tmp/cifar10 --num-gpus=1 --train-steps=1000"

rm -rf ./build/ ./*.egg-info/ ./dist/;
mv ./*.yaml ./checkpoints

# cloudml jobs list