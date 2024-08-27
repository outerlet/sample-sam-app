def try_download_s3_file(s3_client, bucket_name, file_name, download_filepath):
    try:
        s3_client.download_file(
            Bucket=bucket_name,
            Key=file_name,
            Filename=download_filepath,
        )
    except Exception as e:
        print(e)


def upload_s3_file(s3_client, local_filepath, bucket_name, file_name):
    try:
        s3_client.upload_file(
            Filename=local_filepath,
            Bucket=bucket_name,
            Key=file_name,
        )

        return True
    except Exception as e:
        print(e)

        return False
