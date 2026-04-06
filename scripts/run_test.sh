set -eu

pointnet_dir=$(realpath $(dirname $0)/..)

pushd $pointnet_dir >/dev/null

# python test_semseg.py \
#     --log_dir pointnet_sem_seg_wo_stn \
#     --root_dir ./data/stanford_indoor3d/ \
#     --test_area 5 \

python test_classification.py \
    --log_dir pointnet_cls \
    --use_normals \
    --root_dir /home/alisherblack/stuff/sonata/cache/modelnet40_normal_resampled

popd >/dev/null

