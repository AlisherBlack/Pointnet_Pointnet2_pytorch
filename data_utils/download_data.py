import subprocess
from pathlib import Path
from loguru import logger
from functools import wraps


def unpack_data(path_to_data: Path) -> Path:
    path_to_data = Path(path_to_data)
    out_dir = path_to_data.parent

    logger.info(f"Unpacking: {path_to_data}")

    if path_to_data.suffix == ".zip":
        subprocess.run(
            f"unzip '{path_to_data}' -d '{out_dir}'",
            shell=True,
            check=True,
        )

    elif path_to_data.suffixes[-2:] == [".tar", ".gz"] or path_to_data.suffix == ".tgz":
        subprocess.run(
            f"tar -xzf '{path_to_data}' -C '{out_dir}'",
            shell=True,
            check=True,
        )

    elif path_to_data.suffix == ".tar":
        subprocess.run(
            f"tar -xf '{path_to_data}' -C '{out_dir}'",
            shell=True,
            check=True,
        )

    elif path_to_data.suffix == ".gz":
        subprocess.run(
            f"gunzip -k '{path_to_data}'",
            shell=True,
            check=True,
        )

    else:
        logger.warning("Unknown format → skipping unpack")
        return path_to_data

    logger.success("Unpacked successfully")
    return out_dir


def clean_macos_artifacts(root: Path):
    logger.info("Cleaning macOS artifacts")

    subprocess.run(
        f"find '{root}' -name '__MACOSX' -type d -exec rm -rf {{}} +",
        shell=True,
    )
    subprocess.run(
        f"find '{root}' -name '.DS_Store' -type f -delete",
        shell=True,
    )
    subprocess.run(
        f"find '{root}' -name '._*' -type f -delete",
        shell=True,
    )

    logger.success("Artifacts removed")


def download_pipeline(force: bool = False, cleanup_on_error: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(url: str, name: str, out_dir: str, *args, **kwargs):
            out_dir_path = Path(out_dir)
            out_dir_path.mkdir(exist_ok=True)
            archive_path = out_dir_path / name

            def cleanup():
                if cleanup_on_error:
                    logger.warning("Cleanup triggered")
                    archive_path.unlink(missing_ok=True)

            try:
                if archive_path.exists() and not force:
                    logger.info(f"Using existing archive: {archive_path}")
                else:
                    func(url, name, out_dir, *args, **kwargs)

                unpack_data(archive_path)
                clean_macos_artifacts(out_dir_path)

                archive_path.unlink(missing_ok=True)
                logger.success("Pipeline finished")

            except KeyboardInterrupt:
                logger.error("Interrupted")
                cleanup()
                raise

            except Exception as e:
                logger.error(f"Failed: {e}")
                cleanup()
                raise

        return wrapper

    return decorator


@download_pipeline(force=True, cleanup_on_error=True)
def download_func_ydisk(url, name, out_dir):
    path_to_save = Path(out_dir) / name

    subprocess.run(
        f"curl -L $(yadisk-direct {url}) -o {path_to_save}",
        shell=True,
        check=True,
    )


def parse_args():
    import argparse

    parser = argparse.ArgumentParser("Testing")
    parser.add_argument("--url", type=str)
    parser.add_argument("--name", type=str)
    parser.add_argument("--out_dir", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    download_func_ydisk(
        url=args.url,
        name=args.name,
        out_dir=args.out_dir,
    )
