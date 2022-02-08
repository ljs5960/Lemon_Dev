from storages.backends.s3boto3 import S3Boto3Storage

# AWS Media Files
class MediaStorage(S3Boto3Storage):
  location = 'media'
  file_overwrite = False


# AWS Static Files
class StaticStorage(S3Boto3Storage):
  location = 'static'
  file_overwrite = False