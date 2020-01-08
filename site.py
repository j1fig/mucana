from typing import NamedTuple
import os
import subprocess

from jinja2 import Environment, PackageLoader, select_autoescape

from . import builds
from . import tf
from . import utils

DIR="site"


class Project(NamedTuple):
    name: str
    url: str


def gen():
    env = Environment(
        loader=PackageLoader('templates'),
        autoescape=select_autoescape(['html',])
    )

    builds = builds.as_list()
    buckets = tf.make_buckets_from_builds(builds)
    projects = [
        Project(name=utils.kebab_to_display(build), url=bucket)
        for build, bucket in zip(builds, buckets)
    ]
    context = {
        "projects": projects,
    }

    template = env.get_template('index.html')
    html = template.render(context)

    if not os.path.isdir(DIR):
        os.makedirs(DIR)

    html_path = os.path.join(DIR, 'index.html')
    with open(html_path, 'w') as f:
        f.write(html)


def sync():
    bucket = f"s3://mucana.org"
    src = f"{DIR}"
    cmd = [
        "aws",
        "--profile", "personal",
        "--region", "eu-west-1",
        "s3", "sync",
        src, bucket,
    ]
    subprocess.run(cmd)
