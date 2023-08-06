import boto3
import subprocess
import base64
from shutil import which
import sys
from cicd.util import download_util
# To simplifiy things in the beginning, this project will always use us-east-1
# Terraform is free to override this when creating application resources
REGION = 'us-east-1'

ecr_client = boto3.client('ecr', region_name=REGION)
sts_client = boto3.client('sts', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)


def deps():
    if not which('aws'):
        subprocess.run(['pip3', 'install', 'awscli'], check=True)
    if not which('aws-iam-authenticator'):
        if sys.platform == 'darwin':
            subprocess.run(['brew', 'install', 'aws-iam-authenticator'], check=True)
        elif sys.platform == 'linux':
            download_url = "https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/aws-iam-authenticator"
            download_util.download_to_bin(download_url)


def get_repository(application_name, lifecycle):
    repository_name = f"{application_name}/{lifecycle}"
    return ecr_client.describe_repositories(repositoryNames=[repository_name])['repositories'][0]


def ensure_repository(application_name, lifecycle):
    repository_name = f"{application_name}/{lifecycle}"
    try:
        return get_repository(application_name, lifecycle)
    except ecr_client.exceptions.RepositoryNotFoundException as _:
        return ecr_client.create_repository(
            repositoryName=repository_name,
            imageScanningConfiguration={'scanOnPush': True}
            )['repository']


def ecr_login(application_name, lifecycle):
    repository_name = f"{application_name}/{lifecycle}"
    auth_data = ecr_client.get_authorization_token()['authorizationData'][0]
    auth_info = base64.b64decode(auth_data['authorizationToken']).decode('utf-8').split(':')
    auth_user = auth_info[0]
    auth_pass = auth_info[1]
    auth_url = auth_data['proxyEndpoint']
    subprocess.run(f"docker login -u {auth_user} -p {auth_pass} {auth_url}".split(' '))


def get_aws_account_id():
    caller_identity = sts_client.get_caller_identity()
    return caller_identity['Account']


def get_region():
    return REGION


def ensure_s3_bucket(bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
