"""
@doc: a helper for accessing AWS resources using credentials.
@note: priority is environment variables -> .aws/credentials -> ~/spec_creds.json -> manually entered
"""
import boto3
import botocore
import os
import json
import io
from pathlib import Path

HM = str(Path.home())

access = os.environ.get("AWS_ACCESS_KEY_ID")
secret = os.environ.get("AWS_SECRET_ACCESS_KEY")

def check_bucket(bucket):
    """
    """
    check = False
    try:
        try:
            s3 = boto3.resource('s3')
            s3.meta.client.head_bucket(Bucket=bucket)
            check = True
        except:
            if access is None:
                set_creds()
            s3 = boto3.resource('s3')
            s3.meta.client.head_bucket(Bucket=bucket)
            check = True

    except botocore.exceptions.ClientError as e:
        error = e.response['Error']
        if error['Code'] == '404':
            print("It appears that the bucket does not exist")
        elif error['Code'] == '403':
            print("It appears that the bucket exists but access is not configured")
        else:
            print(error)
    return check

def list_objects(bucket):
    """
    """
    keys = []
    s3 = get_resource()
    kwargs = {'Bucket': bucket}
    while True:
        resp = s3.meta.client.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            keys.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break

    return keys

def get_resource():
    """
    @doc: create a boto3 session
    @args: None
    @return: a boto3 session object
    """
    sess = boto3.Session(aws_access_key_id = access, aws_secret_access_key = secret)
    ret = sess.resource('s3')
    return ret

def read_creds(profile='default'):
    """
    @doc: look for locally stored AWS credentials
    @args: None
    @return: a tuple of str with access key and secret
    @note: if none are found then return None
    """
    ret = None
    get_cred = False
    if os.path.isfile("{}/.aws/credentials".format(HM)):
        access = None
        secret = None
        with open("{}/.aws/credentials".format(HM)) as file:
            lines = file.readlines()
        for line in lines:
            if profile in line:
                get_cred = True
            if "key_id" in line and get_cred:
                access = line[line.find("=") + 2:].rstrip()
            elif "access_key" in line and get_cred:
                secret = line[line.find("=") + 2:].rstrip()
                get_cred = False
        ret = access, secret
    return ret

def set_creds(profile='default'):
    """
    @doc: set credentials based on profile as listed in the ~/.aws/credentials file
    @args: profile is a str of the profile credentials desired
    @return: Boolean for whether or not the creds read was successful
    @note: will fail without either environment variables set or a credentials file.
    """
    global access
    global secret
    success = True
    if access is None and profile == 'default':
        no_creds = True
        creds = read_creds(profile)
        if creds is not None:
            if creds[0] is not None and creds[1] is not None:
                no_creds = False
                access = creds[0]
                secret = creds[1]

        if no_creds:
            try:
                creds = json.load(open(HM + "/spec_creds.json", "r"))
                access = creds["AWS_S3_SPECIAL_KEY"]
                secret = creds["AWS_S3_SPECIAL_SECRET"]

            except:
                print("No access or secret found.  The values set here will not be stored.")
                access = input("Please enter your AWS access key: ")
                secret = input("Please enter your AWS secret key: ")
                success = False

    elif profile != 'default':
        creds = read_creds(profile)
        if creds is not None:
            if creds[0] is not None and creds[1] is not None:
                no_creds = False
                access = creds[0]
                secret = creds[1]

            else:
                success = False
        else:
            success = False

    return success
