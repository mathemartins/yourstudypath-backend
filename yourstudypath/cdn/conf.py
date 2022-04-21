import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = 'yourstudypath'
AWS_S3_ENDPOINT_URL = "https://yourstudypath.s3.us-west-2.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read"
}
AWS_LOCATION = "us-west-2"
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = "yourstudypath.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE = 'yourstudypath.cdn.backends.StaticRootS3BotoStorage'
