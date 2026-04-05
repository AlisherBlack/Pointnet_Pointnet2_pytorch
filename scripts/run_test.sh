set -eu

pointnet_dir=$(realpath $(dirname $0)/..)

pushd $pointnet_dir >/dev/null

python test_semseg.py \
    --log_dir pointnet_sem_seg_wo_stn \
    --root_dir ./data/stanford_indoor3d/ \
    --test_area 5 \

popd >/dev/null

