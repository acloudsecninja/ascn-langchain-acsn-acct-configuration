# ascn-langchain-acsn-acct-configuration

## Prerequisites

Before you start, ensure you have the following:

    AWS Account
    AWS SDK for Python (Boto3)
    Langchain library
    OpenAI LLM Model Configuration / API Key



Step 1: Install Required Libraries

```bash
pip install boto3 langchain
pip install python-dotenv
```

Step 2: Setup AWS Credentials

```bash

##Example Using simple AWS ACCESS and SECRET KEY
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = YOUR_REGION
###
```

Step 3: Create a local .env file

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Note: These Credentials will be found in ~/.aws/credentials

Step 4: Configure a Python Script to setup boto3 (AWS) and Langchain and Import OPENAI Model with specfic commands at python script ./run

```bash
## Import and install the folllowing information into the python script which is ran at starting of the python script
import os
import boto3
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Load .env variables from .env file
load_dotenv()

# Get Local API key from environment variable which is setup locally on your system
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize AWS API names
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
iam = boto3.client('iam')

# Chat Response to fetch file content from S3
def fetch_file_from_s3(bucket_name, file_key):
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    return response['Body'].read().decode('utf-8')

# Chat Response to check public buckets
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

# Chat Response to get EC2 instance size
def get_ec2_instance_size(instance_ip):
    instances = ec2.describe_instances(Filters=[{'Name': 'private-ip-address', 'Values': [instance_ip]}])
    instance_type = instances['Reservations'][0]['Instances'][0]['InstanceType']
    return instance_type

# Chat Response to get user permissions
def get_user_permissions(user_name):
    policies = iam.list_attached_user_policies(UserName=user_name)
    return [policy['PolicyName'] for policy in policies['AttachedPolicies']]

# Initialize Langchain with OpenAI
llm = OpenAI(api_key=openai_api_key)

# Chat Response to process text with Langchain
def process_text_with_langchain(text):
    chain = LLMChain(llm=llm)
    return chain.run(text)

# Example usage for chatbot commands
if __name__ == "__main__":
    public_buckets = list_public_buckets()
    print("Public S3 Buckets:")
    print(public_buckets)

    # You can add more commands below.



