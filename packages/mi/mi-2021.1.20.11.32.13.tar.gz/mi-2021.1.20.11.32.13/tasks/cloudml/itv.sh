#!/usr/bin/env bash
# @Project      : mi
# @Time         : 2021/1/13 4:51 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : ${DESCRIPTION}

source scripts/config.sh
# /user/s_feeds/wangxuntao/online/DNN/mitv/model/base/checkpoint_batch
#zjyhdfs -rmr /user/s_feeds/wangxuntao/online/DNN/mitv/model/base/checkpoint_batch/*

eval_day=${1:-$YESTERDAY}

end_day=${2:-$LAST2DAY}

days_num=${3:-21}
config_path="conf/mitv_base_online_nn.yaml"

train_day="null"

tf_record_trainSample="hdfs://zjyprc-hadoop/user/s_feeds/dev/user_growth/push/dnn/mitv/tf-record"
cur_path="/user/s_feeds/dev/user_growth/push/dnn/mitv/tf-record"
for ((i=0; i<$days_num; i+=1))
do
    #echo $i
    cur_day=`date -d"$end_day $i days ago" +"%Y%m%d"`
    filepath=$cur_path"/date="$cur_day
    if $ZJYHDFS_TEST_EXIST "$filepath";
    then
        #continue
        sleep 1s
    else
        continue
    fi
    if [ $train_day == "null" ]; then
        train_day=$cur_day
    else
        train_day=$train_day","$cur_day
    fi
done

echo $eval_day $train_day

waitZjyHdfsReady ${tf_record_trainSample}/date=$eval_day 1 &&
echo 'begin training'
python scripts/daily_train.py --config_path $config_path --train_day $train_day --test_day $eval_day
echo " traning finish"

export_model_base="hdfs://zjyprc-hadoop/user/s_feeds/wangxuntao/online/DNN/mitv/export/base"
export_model_path=$export_model_base/date=${eval_day}
echo " export_model_path: "$export_model_path

#online_model="/user/s_feeds/cuizhigang/DNN/model/online"
online_model="/user/s_feeds/songyang7/DNN/model/online"
waitZjyHdfsReady ${export_model_path} 1 &&
zjyhdfs -rm ${online_model}/id_map_*
zjyhdfs -rm ${online_model}/layers
zjyhdfs -rm ${online_model}/embedding_group
zjyhdfs -rm ${online_model}/_SUCCESS
zjyhdfs -cp ${export_model_path}/id_map_* ${online_model}
zjyhdfs -cp ${export_model_path}/layers ${online_model}
zjyhdfs -cp ${export_model_path}/embedding_group ${online_model}
zjyhdfs -cp ${export_model_path}/_SUCCESS ${online_model}

echo "final success"