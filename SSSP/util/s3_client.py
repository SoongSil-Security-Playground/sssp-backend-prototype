from SSSP.config import s3
import boto3

s3_client = boto3.client(
    "s3",
    region_name=s3.AWS_REGION,
    aws_access_key_id=s3.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=s3.AWS_SECRET_ACCESS_KEY,
)
