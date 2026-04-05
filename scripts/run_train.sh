set -eu

pointnet_dir=$(realpath $(dirname $0)/..)


pushd $pointnet_dir >/dev/null


python train_semseg.py --model pointnet_sem_seg --test_area 5 --log_dir pointnet_sem_seg --root_dir ./data/stanford_indoor3d/


popd >/dev/null

