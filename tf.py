import json
import os
import subprocess


_TF_VARS_FILENAME="terraform.tfvars.json"
_PROJECTS_DIR='build/Builds'
_POLICIES_DIR='policies'
_POLICY_TEMPLATE='bucket-policy-template.json'
_BUCKET_SUFFIX=".mucana.org"


def make_buckets_from_builds(builds):
    return [b + _BUCKET_SUFFIX for b in builds]


def gen_bucket_cname_vars(builds):
    buckets = make_buckets_from_builds(builds)
    cnames = {p: b for p, b in zip(builds, buckets)}
    with open(_TF_VARS_FILENAME, 'w') as f:
        f.write(json.dumps({"buckets": buckets, "cnames": cnames}))


def gen_bucket_policies(builds):
    buckets = make_buckets_from_builds(builds)
    with open(_POLICY_TEMPLATE, 'r') as f:
        template = json.loads(f.read())

    for b in buckets:
        filename = f"{b}.json"
        with open(os.path.join(_POLICIES_DIR, filename), 'w') as f:
            template["Statement"][0]["Resource"][0] = f"arn:aws:s3:::{b}/*"
            f.write(json.dumps(template))


def apply():
    cmd = ["terraform", "apply"]
    subprocess.run(cmd)
