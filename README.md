# 🛡️ ASCN LangChain AWS Account Configuration

## 📋 Overview

This project provides intelligent AWS account configuration and information retrieval using LangChain agents. The solution integrates directly with AWS APIs to pull requested information through automated Python scripts with natural language processing capabilities.

## 🚀 Features

- **🤖 Intelligent AWS Agent**: LangChain-powered agent for natural AWS API interactions
- **📊 Multi-Service Support**: S3, EC2, Route53, and IAM integration
- **📤 Automated Reporting**: CSV export and ZIP archiving of findings
- **🔍 Comprehensive Queries**: Natural language to AWS command translation
- **⚡ Real-time Results**: Immediate AWS data retrieval and analysis

## 📋 Prerequisites

Before you start, ensure you have the following:

| Requirement | Version/Details |
|-------------|-----------------|
| **AWS Account** | Valid AWS account with necessary permissions |
| **AWS SDK for Python** | Boto3 library |
| **LangChain Library** | Latest stable version |
| **OpenAI API** | Valid API key and configuration |
| **Operating System** | Windows 11 |
| **Python** | Version 3.13.9 |

## 🔧 Installation & Setup

### Step 1: Environment Setup
Open Git Bash terminal within Visual Studio Code on Windows.

### Step 2: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 3: Configure AWS Credentials

Create or update your AWS credentials file (`~/.aws/credentials`):

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-2
```

> **📝 Note**: Credentials can also be configured via `.env` file based on your preference.

### Step 4: Set Up Environment Variables

Create a local `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key  
REGION_NAME=us-east-2
```

> **⚠️ Security Notice**: The `.env` file is excluded from Git via `.gitignore` to protect sensitive credentials.

## 🎯 Usage

### Option 1: Direct AWS API Script
Run the traditional boto3-based script for direct AWS API interactions:

```bash
python pull-info-from-aws-acct.py
```

### Option 2: Intelligent AWS Agent (Recommended)
Execute the LangChain-powered AWS agent for enhanced natural language processing and automated reporting:

```bash
python ascn-aws-agent.py
```

#### 📊 Output Features
- **Real-time Results**: Immediate console output of AWS findings
- **CSV Export**: Structured data export to `aws_findings.csv`
- **ZIP Archive**: Compressed findings in `aws_findings_report.zip`
- **Timestamped Records**: All findings include execution timestamps

## 🏗️ Architecture

The AWS Agent supports the following services:
- **🪣 S3**: Bucket listing and content analysis
- **🖥️ EC2**: Instance information and sizing
- **🌐 Route53**: Hosted zone management
- **👤 IAM**: User permissions and policy analysis

## 📈 Sample Output

The agent generates comprehensive reports including:
- Service-specific findings
- Query execution timestamps
- Success/failure status
- Detailed result data
- Error handling and logging

## 🤝 Support & Maintenance

**Created and Maintained by**: A Cloud Security Ninja LLC

**📞 Contact & Consultation**: 
- Website: [acloudsec.ninja](https://www.acloudsec.ninja/booking-calendar/free-15-minute-consultation)
- Free 15-minute consultation available

---

*🔒 Security-focused cloud solutions for modern infrastructure*