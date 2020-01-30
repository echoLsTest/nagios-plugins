# nagios-plugins

Check current event logs information from the AWS Service Health Dashboard

The endpoint for the AWS Health API is: https://health.us-east-1.amazonaws.com (provides event data for all regions)
source: https://docs.aws.amazon.com/health/latest/ug/getting-started-api.html

usage: 
check_aws_events.py -s <EC2 or RDS> -r <us-east-1 or us-west-1 or us-west-2>
