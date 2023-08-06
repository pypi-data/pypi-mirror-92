#!/usr/bin/env bash
if [ -n "$1" ]
then name=$1
else name=v10000
fi;

password=Betterme8
cloudml dev create -n $name -p $password \
--priority_class preferred \
-d cr.d.xiaomi.net/cloud-ml/devsave:33103-v100 \
-cm rw \
-rs v100 \
-c 4 -M 8G \
# -g 1 -gt v100 -gm 32g \



