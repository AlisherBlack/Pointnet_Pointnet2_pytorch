set -eu

pointnet_dir=$(realpath $(dirname $0)/..)


pushd $pointnet_dir >/dev/null


model_name=pointnet_sem_seg_wo_stn

python train_semseg.py \
    --model $model_name \
    --log_dir $model_name \
    --test_area 5 \
    --root_dir ./data/stanford_indoor3d/


popd >/dev/null

