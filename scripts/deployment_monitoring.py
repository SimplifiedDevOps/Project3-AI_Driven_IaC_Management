# scripts/deployment_monitoring.py
import boto3
import time

# Initialize AWS CloudWatch and SNS clients
def initialize_aws_clients():
    cloudwatch = boto3.client("cloudwatch", region_name="us-west-2")
    sns = boto3.client("sns", region_name="us-west-2")
    return cloudwatch, sns

# Create a CloudWatch alarm for EC2 instance monitoring
def create_cloudwatch_alarm(instance_id, sns_topic_arn):
    cloudwatch, sns = initialize_aws_clients()

    alarm_name = f"EC2-Instance-{instance_id}-High-CPU-Alarm"
    response = cloudwatch.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Statistic="Average",
        Period=300,
        EvaluationPeriods=2,
        Threshold=80.0,
        ComparisonOperator="GreaterThanThreshold",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        AlarmActions=[sns_topic_arn],
        AlarmDescription="Alarm when EC2 instance CPU exceeds 80%",
        ActionsEnabled=True,
    )
    return response

# Function to monitor and report the status of the deployment
def monitor_ec2_instance(instance_id):
    cloudwatch, _ = initialize_aws_clients()
    metric_data = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=time.time() - 600,
        EndTime=time.time(),
        Period=300,
        Statistics=["Average"]
    )
    for point in metric_data["Datapoints"]:
        print(f"Time: {point['Timestamp']}, CPU Utilization: {point['Average']}%")

# Set up SNS Topic and subscribe to alerts
def setup_sns_topic(email):
    sns = boto3.client("sns", region_name="us-west-2")
    topic_name = "DeploymentAlerts"
    topic_response = sns.create_topic(Name=topic_name)
    sns_topic_arn = topic_response["TopicArn"]

    # Subscribe an email to the SNS topic
    sns.subscribe(TopicArn=sns_topic_arn, Protocol="email", Endpoint=email)
    print(f"Subscription confirmation email sent to {email}. Please confirm to receive alerts.")
    return sns_topic_arn

if __name__ == "__main__":
    # Example instance_id and email for alerting
    instance_id = "i-0abcd1234efgh5678"
    alert_email = "your-email@example.com"

    # Set up SNS for alerting
    sns_topic_arn = setup_sns_topic(alert_email)

    # Create and enable CloudWatch alarm
    alarm_response = create_cloudwatch_alarm(instance_id, sns_topic_arn)
    print("CloudWatch Alarm Response:\n", alarm_response)

    # Monitor EC2 instance CPU utilization
    monitor_ec2_instance(instance_id)
