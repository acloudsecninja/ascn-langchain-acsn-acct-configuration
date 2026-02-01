# Import required libraries
import os
import boto3
from dotenv import load_dotenv

# Initialize AWS API service clients
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
iam = boto3.client('iam')
route53 = boto3.client('route53')

# Chat Response to fetch file content from S3
def fetch_file_from_s3(bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')

# Chat Response to list public buckets
def list_public_buckets():
    response = s3.list_buckets()
    public_buckets = []

    for bucket in response['Buckets']:
        acl = s3.get_bucket_acl(Bucket=bucket['Name'])
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and 'AllUsers' in grant['Grantee']['URI']:
                public_buckets.append(bucket['Name'])
                break

    return public_buckets

# Chat Response to get bucket contents
def get_bucket_contents(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    contents = [item['Key'] for item in response.get('Contents', [])]
    return contents

# Chat Response to list Route 53 hosted zones
def list_route53_hosted_zones():
    response = route53.list_hosted_zones()
    hosted_zones = [zone['Name'] for zone in response['HostedZones']]
    return hosted_zones

# Chat Response to get EC2 instance size
def get_ec2_instance_size(instance_ip):
    instances = ec2.describe_instances(Filters=[{'Name': 'private-ip-address', 'Values': [instance_ip]}])
    instance_type = instances['Reservations'][0]['Instances'][0]['InstanceType']
    return instance_type

# Chat Response to get user permissions
def get_user_permissions(user_name):
    policies = iam.list_attached_user_policies(UserName=user_name)
    return [policy['PolicyName'] for policy in policies['AttachedPolicies']]

# Chat Response to list Route 53 hosted zones
def list_route53_hosted_zones():
    response = route53.list_hosted_zones()
    hosted_zones = [zone['Name'] for zone in response['HostedZones']]
    return hosted_zones

###### Example usages for chatbot commands interacting with AWS API ######
if __name__ == "__main__":

    # Get contents of a specific S3 bucket
    bucket_name = "take-home-coding"
    contents = get_bucket_contents(bucket_name)
    print(f"Contents of {bucket_name}:")
    print(contents)

   # List Route 53 hosted zones
    hosted_zones = list_route53_hosted_zones()
    print("Route 53 Hosted Zones:")
    print(hosted_zones)
    
    # Get size of an EC2 instance
    ec2_instance_ip = "10.0.1.112"
    instance_size = get_ec2_instance_size(ec2_instance_ip)
    print(f"EC2 Instance Size for IP {ec2_instance_ip}: {instance_size}")

    # Get permissions for a specific IAM user
    iam_user_name = "take-home-coding"
    permissions = get_user_permissions(iam_user_name)
    print(f"Permissions for user {iam_user_name}: {permissions}")

   # List Route 53 hosted zones
    hosted_zones = list_route53_hosted_zones()
    print("Route 53 Hosted Zones:")
    print(hosted_zones)