import subprocess

from cicd import config

from cicd.util import aws_util, download_util, file_util
from pkg_resources import resource_filename
import sys
from shutil import which

def deps():
    if not which('terraform'):
        if sys.platform == 'darwin':
            subprocess.run(['brew', 'tap', 'hashicorp/tap'], check=True)
            subprocess.run(['brew', 'install', 'hashicorp/tap/terraform'], check=True)
        if sys.platform == 'linux':
            download_url = 'https://releases.hashicorp.com/terraform/0.14.4/terraform_0.14.4_linux_amd64.zip'
            with download_util.download_to_tmp(download_url) as (path, folder):
                file_util.unzip_file(path)
                file_util.add_to_bin(f"{folder}/terraform")

def clear_existing_tf_files(terraform_dir):
    terraform_dir_abspath = file_util.abspath(terraform_dir)
    file_util.rm(f"{terraform_dir_abspath}/.terraform")
    file_util.rm(f"{terraform_dir_abspath}/terraform.tfstate")
    file_util.rm(f"{terraform_dir_abspath}/backend-s3")

def init(application_name, lifecycle, resource, backend='s3'):
    if backend == 's3':
        init_s3(application_name, lifecycle, resource)
    else:
        raise Exception("Unknown terraform backend option used")

def init_s3(application_name, lifecycle, resource):
    terraform_dir = f"terraform/{resource}"

    clear_existing_tf_files(terraform_dir)
    account_id = aws_util.get_aws_account_id()
    aws_region = aws_util.get_region()
    state_bucket_name = f"terraform-state-{aws_region}-{account_id}"
    state_name = f"{application_name}/{resource}/{lifecycle}"
    copy_backend_file(terraform_dir, 's3')
    aws_util.ensure_s3_bucket(state_bucket_name)
    terraform(
        'init',
        [
            f"-backend-config=bucket={state_bucket_name}",
            f"-backend-config=key={state_name}",
            f"-backend-config=region={aws_region}",
        ],
        terraform_dir
    )

def copy_backend_file(terraform_dir, backend='s3'):
    backend_file_path = resource_filename('cicd.util', f"resources/tf_backends/{backend}.tf")
    file_util.copyfile(backend_file_path, f"{terraform_dir}/s3-backend.tf")

def apply(application_name, lifecycle, resource, auto_approve=True):
    terraform_dir = f"terraform/{resource}"
    tf_vars_path = file_util.abspath(f"{terraform_dir}/../tfvars/{lifecycle}.tfvars")
    opts = [
        '--var-file', tf_vars_path,
        '--var', f"application_name={application_name}",
    ]
    if auto_approve:
        opts.append('-auto-approve')

    terraform('apply', opts, terraform_dir)

def destroy(application_name, lifecycle, resource, auto_approve=True):
    terraform_dir = f"terraform/{resource}"
    tf_vars_path = file_util.abspath(f"{terraform_dir}/../tfvars/{lifecycle}.tfvars")
    opts = [
        '--var-file', tf_vars_path,
        '--var', f"application_name={application_name}",
    ]
    if auto_approve:
        opts.append('-auto-approve')

    terraform('destroy', opts, terraform_dir)

def terraform(action, opts=[], cwd=file_util.get_cwd()):
    command = ['terraform', action]
    command.extend(opts)
    subprocess.run(command, check=True, cwd=cwd)
