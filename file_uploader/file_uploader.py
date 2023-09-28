import os
import mimetypes
import boto3
from botocore.exceptions import NoCredentialsError,FileNotFoundError
from google.cloud import storage

class FileUploader:
    def __init__(
        self,
        aws_access_key,
        aws_secret_key,
        aws_s3_bucket,
        gcs_credentials_file,
        gcs_bucket,
        config,
    ):
        """
        Initialize the FileUploader with necessary parameters.

        Args:
            aws_access_key (str): AWS Access Key.
            aws_secret_key (str): AWS Secret Key.
            aws_s3_bucket (str): AWS S3 Bucket name.
            gcs_credentials_file (str): Google Cloud Storage credentials file path.
            gcs_bucket (str): Google Cloud Storage Bucket name.
            config (dict): Configuration mapping file types to destinations.
        """
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_s3_bucket = aws_s3_bucket
        self.gcs_credentials_file = gcs_credentials_file
        self.gcs_bucket = gcs_bucket
        self.config = config

    def upload_files(self, source_dir):
        """
        Upload files from the source directory to the specified destinations.

        Args:
            source_dir (str): Source directory path.
        """
        for root, _, files in os.walk(source_dir):
            for filename in files:
                file_path = os.path.join(root, filename)
                file_type = self.get_file_type(file_path)
                destination = self.config.get(file_type)

                if destination:
                    if destination == "s3":
                        self.upload_to_s3(file_path, filename)
                    elif destination == "gcs":
                        self.upload_to_gcs(file_path, filename)

    def get_file_type(self, file_path):
        """
        Determine the file type based on MIME type.
        Args:
            file_path (str): File path.
        Returns:
            str or None: File type or None if not recognized.
        """
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            file_extension = mimetypes.guess_extension(mime_type)
            if file_extension in ['jpg', 'png', 'svg','webp']:
                return "image"
            elif file_extension in ['mp3', \
                'mp4', 'mpeg4', 'wmv', '3gp', 'webm']:
                return "audio"
            elif file_extension in ["doc", "docx", "csv",  "pdf"]:
                return "document"
            else :
                return mime_type.split("/")[0]
        except Exception as e:
            return None

    def upload_to_s3(self, file_path, filename):
        """
        Upload a file to AWS S3.

        Args:
            file_path (str): File path.
            filename (str): Destination filename on S3.
        """
        s3 = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            )
        try:
            # Create a file stream to read and upload the file in chunks
            with open(file_path, "rb") as file_stream:
                s3.upload_fileobj(file_stream, self.aws_s3_bucket, filename)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except NoCredentialsError:
            print("AWS credentials not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def upload_to_gcs(self, file_path, filename):
        """
        Upload a file to Google Cloud Storage.

        Args:
            file_path (str): File path.
            filename (str): Destination filename on GCS.
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.gcs_credentials_file
        try:
            client = storage.Client()
            bucket = client.bucket(self.gcs_bucket)
            blob = bucket.blob(filename)
            # Upload the file from the specified file path
            with open(file_path, "rb") as file_stream:
                blob.upload_from_file(file_stream)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    aws_access_key = "your_aws_access_key"
    aws_secret_key = "your_aws_secret_key"
    aws_s3_bucket = "your_s3_bucket"
    gcs_credentials_file = "your_gcs_credentials_file.json"
    gcs_bucket = "your_gcs_bucket"
    config = {
        "image": "s3",
        "audio": "s3",
        "document": "gcs",
    }
    source_dir = "your_source_directory"
    uploader = FileUploader(
        aws_access_key,
        aws_secret_key,
        aws_s3_bucket,
        gcs_credentials_file,
        gcs_bucket,
        config,
    )
    uploader.upload_files(source_dir)

if __name__ == "__main__":
    main()