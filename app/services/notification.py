import boto3

def send_notification(email: str, subject: str, message: str):
    sns = boto3.client("sns")
    response = sns.publish(
        TopicArn="tu_topic_arn",
        Subject=subject,
        Message=message,
    )
    print(f"Notificación enviada: {response}")
