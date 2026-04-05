set -eu

pointnet_dir=$(realpath $(dirname $0)/..)

pushd $pointnet_dir >/dev/null

python test_semseg.py --log_dir pointnet_sem_seg --test_area 5 --root_dir ./data/stanford_indoor3d-sanity-check/

popd >/dev/null

