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
#   --priority_class {guaranteed,preferred,best-effort}
cloudml jobs submit \
-n $taget_name \
-m $project_name \
-u ./ \
-c 77 -M 66G \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-cpu666 \
-hka h_browser@XIAOMI.HADOOP -hkt tql -he hdfs://zjyprc-hadoop \
-pc "pip install -U --no-cache-dir -i https://pypi.python.org/pypi tql" \
--priority_class "best-effort" \
#-g 1 #-gt v100 -gm 32g


#--priority_class "preferred"
#-d cr.d.xiaomi.net/cloud-ml/devsave:33103-mydev \
# #-d cr.d.xiaomi.net/cloud-ml/devsave:33103-mydev \
# -a "--data-dir=/fds/cifar-10-data --job-dir=/tmp/cifar10 --num-gpus=1 --train-steps=1000"

rm -rf ./build/ ./*.egg-info/ ./dist/;
mv ./*.yaml ./checkpoints
# cloudml jobs list
