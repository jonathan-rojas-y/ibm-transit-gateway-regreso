import os
import subprocess

def run_command(command, sleep_time=0):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        if sleep_time > 0:
            time.sleep(sleep_time)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}\nExit code: {e.returncode}\nOutput: {e.output}\nError: {e.stderr}")

# Load environment variables
IBM_CLOUD_API_KEY = os.getenv("IBM_CLOUD_API_KEY")
REGION = os.getenv("REGION", "us-south")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP", "Unique")
TG_ID = os.getenv("TG_ID")
PREFIX_FILTER_DENY_ID = os.getenv("PREFIX_FILTER_DENY_ID")
PREFIX_FILTER_PERMIT_ID = os.getenv("PREFIX_FILTER_PERMIT_ID")
PREFIX_DENY_RULE_ID = os.getenv("PREFIX_DENY_RULE_ID")
PREFIX_PERMIT_RULE_ID = os.getenv("PREFIX_PERMIT_RULE_ID")
PREFIX = os.getenv("PREFIX", "172.20.19.0/29")

# Validate required environment variables
required_vars = ["IBM_CLOUD_API_KEY", "TG_ID", "PREFIX_FILTER_DENY_ID", "PREFIX_FILTER_PERMIT_ID", "PREFIX_DENY_RULE_ID", "PREFIX_PERMIT_RULE_ID"]
missing_vars = [var for var in required_vars if not globals()[var]]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Validate IBM Cloud login
run_command(f"ibmcloud login --apikey {IBM_CLOUD_API_KEY} -r '{REGION}' -g '{RESOURCE_GROUP}' -q")

# Step 1: Deny traffic from 172.20.19.0/29 to DAL12
run_command(f"ibmcloud tg prefix-filter-update {TG_ID} {PREFIX_FILTER_DENY_ID} {PREFIX_DENY_RULE_ID} --prefix {PREFIX} --action deny", sleep_time=15)

# Step 2: Allow traffic from 172.20.19.0/29 to DAL10
run_command(f"ibmcloud tg prefix-filter-update {TG_ID} {PREFIX_FILTER_PERMIT_ID} {PREFIX_PERMIT_RULE_ID} --prefix {PREFIX} --action permit", sleep_time=15)

# Step 3: Update Transit Gateway routes
run_command(f"ibmcloud tg rrs {TG_ID}", sleep_time=30)

# Step 4: Deny traffic from 172.20.19.0/29 to DAL10
run_command(f"ibmcloud tg prefix-filter-update {TG_ID} {PREFIX_FILTER_PERMIT_ID} {PREFIX_PERMIT_RULE_ID} --prefix {PREFIX} --action deny", sleep_time=15)

# Step 5: Allow traffic from 172.20.19.0/29 to DAL10 again
run_command(f"ibmcloud tg prefix-filter-update {TG_ID} {PREFIX_FILTER_PERMIT_ID} {PREFIX_PERMIT_RULE_ID} --prefix {PREFIX} --action permit", sleep_time=15)

# Step 6: Update Transit Gateway routes again
run_command(f"ibmcloud tg rrs {TG_ID}", sleep_time=20)
