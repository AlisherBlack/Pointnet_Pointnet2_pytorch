set -eu

pointnet_dir=$(realpath $(dirname $0)/..)


pushd $pointnet_dir >/dev/null


model_name=pointnet_cls

python train_classification.py \
    --model $model_name \
    --log_dir $model_name \
     --use_normals \
    --root_dir /home/alisherblack/stuff/sonata/cache/modelnet40_normal_resampled


popd >/dev/null

