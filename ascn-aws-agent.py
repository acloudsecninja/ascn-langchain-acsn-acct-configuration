# Import required libraries to ensure the Agent works properly.
import os
import boto3
import csv
import zipfile
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_core.runnables import RunnablePassthrough

# Load environment variables from .env file which includes AWS Creds and OPENAI Key.
# Need the billing setup for OpenAI for the agent to work.
load_dotenv()

# Fetch credentials from environment variables locally using the OS imported python package.
aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_KEY')
region_name = os.getenv('REGION_NAME')

# Create AWS service clients to ensure the agent knows what its doing.
ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id, 
                   aws_secret_access_key=aws_secret_access_key, region_name=region_name)
route53 = boto3.client('route53', aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key, region_name=region_name)
iam = boto3.client('iam', aws_access_key_id=aws_access_key_id, 
                   aws_secret_access_key=aws_secret_access_key, region_name=region_name)


## Defined Tools being used for the Agent and how they are working within itself.
@tool
def aws_cli_command(command: str) -> str:
    """Execute AWS CLI commands for interacting with AWS services"""
    import subprocess
    try:
        # Set AWS environment variables so the Agent knows what AWS account its logging into.
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        env['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        env['AWS_DEFAULT_REGION'] = region_name
        
        # Execute AWS CLI command using the credentials the AWS Agent will use.
        result = subprocess.run(['aws'] + command.split(), 
                              capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error executing AWS command: {str(e)}"


## What the Agent will be able to do running the AWS Cli and the credentials that is being used.

###START###
@tool
def list_route53_hosted_zones() -> str:
    """List all Route 53 hosted zones in the AWS account"""
    try:
        response = route53.list_hosted_zones()
        hosted_zones = [zone['Name'] for zone in response['HostedZones']]
        return f"Route 53 Hosted Zones: {hosted_zones}"
    except Exception as e:
        return f"Error listing Route 53 hosted zones: {str(e)}"

@tool
def get_ec2_instance_size(instance_ip: str) -> str:
    """Get the instance type/size of an EC2 instance by its private IP address"""
    try:
        instances = ec2.describe_instances(Filters=[{'Name': 'private-ip-address', 'Values': [instance_ip]}])
        if instances['Reservations']:
            instance_type = instances['Reservations'][0]['Instances'][0]['InstanceType']
            return f"EC2 instance {instance_ip} is of type: {instance_type}"
        else:
            return f"No EC2 instance found with IP address: {instance_ip}"
    except Exception as e:
        return f"Error getting EC2 instance size: {str(e)}"

@tool
def get_user_permissions(user_name: str) -> str:
    """Get all attached IAM policies for a specific IAM user"""
    try:
        policies = iam.list_attached_user_policies(UserName=user_name)
        policy_names = [policy['PolicyName'] for policy in policies['AttachedPolicies']]
        return f"IAM user '{user_name}' has these policies: {policy_names}"
    except Exception as e:
        return f"Error getting user permissions: {str(e)}"

@tool
def list_s3_buckets() -> str:
    """List all S3 buckets in the AWS account"""
    try:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key, region_name=region_name)
        response = s3.list_buckets()
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        return f"S3 Buckets: {bucket_names}"
    except Exception as e:
        return f"Error listing S3 buckets: {str(e)}"

###END###

# Determine which LLM model the Agent will be using and which credentails to use from OpenAI.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Define the prompt template so the agent will know what to do and how to get the answers.
prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant that can interact with AWS services. You have access to the following tools:

Available tools:
- aws_cli_command: Execute any AWS CLI command
- list_route53_hosted_zones: List all Route 53 hosted zones
- get_ec2_instance_size: Get EC2 instance type by private IP address
- get_user_permissions: Get IAM user policies by username
- list_s3_buckets: List all S3 buckets

User request: {input}

Your response:
""")

# Create the chain which will be used to process the user's request, but in this case python is running the script and the outputs.
chain = prompt | llm


### Export to CSV and ZIP Files. ###
def export_findings_to_csv(findings_data, filename="aws_findings.csv"):
    """Export AWS findings to CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'service', 'query', 'result', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for finding in findings_data:
                writer.writerow(finding)
        
        print(f"\n✅ Findings exported to {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error exporting to CSV: {str(e)}")
        return None

def create_zip_file(csv_file, zip_filename="aws_findings_report.zip"):
    """Create a zip file containing the CSV findings"""
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_file)
        
        print(f"✅ Findings zipped to {zip_filename}")
        return zip_filename
    except Exception as e:
        print(f"❌ Error creating zip file: {str(e)}")
        return None


### Test the Agent and how it works and determine if the outputs (answers) are correct. ###
def test_aws_agent():
    """Test the AWS agent with various AWS operations and export findings"""
    test_queries = [
        "List all S3 buckets in my AWS account",
        "List all Route 53 hosted zones", 
        "Get the size of EC2 instance with IP 10.0.1.112",
        "Get permissions for IAM user take-home-coding"
    ]
    
    findings_data = []
    
    for query in test_queries:
        try:
            print(f"\n{'='*50}")
            print(f"Query: {query}")
            print('='*50)
            
            # Get LLM response
            result = chain.invoke({"input": query})
            print("Agent response:")
            print(result.content)
            
            # Execute relevant tool based on query
            aws_result = "No tool executed"
            service = "Unknown"
            status = "Success"
            
            if "s3" in query.lower() and "bucket" in query.lower():
                print("\nExecuting S3 bucket listing...")
                aws_result = list_s3_buckets.invoke({})
                service = "S3"
                print("Result:", aws_result)
            elif "route 53" in query.lower() or "hosted zone" in query.lower():
                print("\nExecuting Route 53 hosted zones listing...")
                aws_result = list_route53_hosted_zones.invoke({})
                service = "Route53"
                print("Result:", aws_result)
            elif "ec2" in query.lower() and "10.0.1.112" in query:
                print("\nGetting EC2 instance size...")
                aws_result = get_ec2_instance_size.invoke({"instance_ip": "10.0.1.112"})
                service = "EC2"
                print("Result:", aws_result)
            elif "iam" in query.lower() and "take-home-coding" in query.lower():
                print("\nGetting IAM user permissions...")
                aws_result = get_user_permissions.invoke({"user_name": "take-home-coding"})
                service = "IAM"
                print("Result:", aws_result)
            
            # Collect findings data
            finding = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'service': service,
                'query': query,
                'result': aws_result,
                'status': status
            }
            findings_data.append(finding)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            # Log error findings
            error_finding = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'service': service,
                'query': query,
                'result': f"Error: {str(e)}",
                'status': "Failed"
            }
            findings_data.append(error_finding)
    
    # Export findings to CSV
    if findings_data:
        csv_file = export_findings_to_csv(findings_data)
        if csv_file:
            # Create zip file
            zip_file = create_zip_file(csv_file)
            if zip_file:
                print(f"\n🎉 AWS findings export complete!")
                print(f"📁 CSV file: {csv_file}")
                print(f"📦 Zip file: {zip_file}")
    
    return findings_data

if __name__ == "__main__":
    print("Testing Enhanced AWS Agent...")
    test_aws_agent()
