from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="Pointcept/modelnet40_normal_resampled-compressed",
    repo_type="dataset",
    local_dir="./modelnet40",
    local_dir_use_symlinks=False,
)
