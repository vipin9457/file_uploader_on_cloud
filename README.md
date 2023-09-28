# upload_files_on_cloud
Upload media  Files on S3 and Document files on Google Cloud Strorage
# File Uploader Module
File Uploader is a Python module that allows you to upload files to AWS S3 and Google Cloud Storage based on their file types.

## Installation

To install the module, use pip:
pip install file_uploader_on_cloud
or 
we can run the module with the following command 
python3 install -r requirements.txt
python3 setup.py install

## Usage

Here's an example of how to use the module:

```python
from file_uploader.file_uploader import FileUploader
aws_access_key = 'your_aws_access_key'
aws_secret_key = 'your_aws_secret_key'
aws_s3_bucket = 'your_s3_bucket'
gcs_credentials_file = 'your_gcs_credentials_file.json'
gcs_bucket = 'your_gcs_bucket'
config = {
    'image': 's3',
    'audio': 's3',
    'document': 'gcs',
}
source_dir = 'your_source_directory'
uploader = FileUploader(aws_access_key, aws_secret_key, aws_s3_bucket, gcs_credentials_file, gcs_bucket, config)
uploader.upload_files(source_dir)

