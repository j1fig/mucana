import subprocess
import os
import zipfile

from . import utils


FILE="build.zip"
BUILD_DIR="build"
FILEID='1xP1AKzJdMISnkGWGNKUm_EfJvjCurgmW'
URL=f"https://docs.google.com/uc?export=download&id={FILEID}"


def ensure_cached():
    if not os.path.exists(FILE):
        # wget seems to be the only current option that behaves properly
        # whilst downloading gdrive shared files.
        cmd = [
            "wget", "--no-check-certificate",
            "-r", URL, "-O", FILE,
        ]
        subprocess.run(cmd)
    if not os.path.isdir(BUILD_DIR):
        with zipfile.ZipFile(FILE, "r") as z:
            z.extractall(path=BUILD_DIR)


def as_list():
    builds = os.listdir(_PROJECTS_DIR)
    return [utils.camel_to_kebab(b) for b in builds]


def as_dir_map():
    builds = os.listdir(_PROJECTS_DIR)
    return {b: utils.camel_to_kebab(b) for b in builds}


def sync():
    dir_map = as_dir_map()
    for b, p in dir_map.items():
        bucket = f"s3://{p}{_BUCKET_SUFFIX}"
        src = f"{_PROJECTS_DIR}/{b}"
        cmd = [
            "aws",
            "--profile", "personal",
            "--region", "eu-west-1",
            "s3", "sync",
            src, bucket,
        ]
        subprocess.run(cmd)
