# IBM Cloud Transit Gateway Script

## Overview
This repository contains a Python script (`regreso.py`) for automating IBM Cloud Transit Gateway configurations. It uses the IBM Cloud CLI to manage prefix filters and update routes.

## Prerequisites
- Python 3.9 or later
- IBM Cloud CLI installed with the `tg` plugin
- An IBM Cloud API key

## Environment Variables
Ensure the following environment variables are set before running the script:

- `IBM_CLOUD_API_KEY`: Your IBM Cloud API key
- `REGION`: IBM Cloud region (default: `us-south`)
- `RESOURCE_GROUP`: Resource group name (default: `Unique`)
- `TG_ID`: Transit Gateway ID
- `PREFIX_FILTER_DENY_ID`: ID for the deny prefix filter
- `PREFIX_FILTER_PERMIT_ID`: ID for the permit prefix filter
- `PREFIX_DENY_RULE_ID`: Rule ID for denying the prefix
- `PREFIX_PERMIT_RULE_ID`: Rule ID for permitting the prefix
- `PREFIX`: IP prefix to manage (default: `172.20.19.0/29`)

## Usage

### Build the Docker Image
To build the Docker image:
```bash
docker build -t ibmcloud-transit-gateway .
