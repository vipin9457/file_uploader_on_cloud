import os
import pytest
from file_uploader.file_uploader import FileUploader

# Fixture for creating a temporary directory with test files


@pytest.fixture
def temp_directory(tmpdir):
    """
    Create a temporary directory with sample test files.

    Args:
        tmpdir (py._path.local.LocalPath): Pytest fixture for temporary directories.

    Returns:
        str: Path to the temporary directory.
    """
    source_dir = tmpdir.mkdir("test_files")
    # Create test files within the temporary directory
    open(source_dir.join("image1.png"), "a").close()
    open(source_dir.join("audio1.mp3"), "a").close()
    open(source_dir.join("document1.pdf"), "a").close()
    return str(source_dir)


def test_get_file_type():
    """
    Test the get_file_type method's ability to determine file types based on extensions.
    """
    uploader = FileUploader(None, None, None, None, None, None)

    # Test various file types
    assert uploader.get_file_type("image.jpg") == "image"
    assert uploader.get_file_type("audio.mp3") == "audio"
    assert uploader.get_file_type("document.pdf") == "document"
    assert uploader.get_file_type("unknown.xyz") is None


def test_upload_to_s3(temp_directory, monkeypatch):
    """
    Test the upload_to_s3 method by mocking the upload_to_s3 function and verifying behavior.

    Args:
        temp_directory (str): Temporary directory path.
        monkeypatch (_pytest.monkeypatch.MonkeyPatch): Pytest fixture for monkeypatching.
    """
    uploader = FileUploader(
        "aws_access_key", "aws_secret_key", "s3_bucket", None, None, {"image": "s3"}
    )

    def mock_upload_to_s3(file_path, aws_s3_bucket, filename):
        assert aws_s3_bucket == "s3_bucket"
        assert os.path.basename(file_path) == filename

    monkeypatch.setattr(uploader, "upload_to_s3", mock_upload_to_s3)

    uploader.upload_files(temp_directory)


def test_upload_to_gcs(temp_directory, monkeypatch):
    """
    Test the upload_to_gcs method by mocking the upload_to_gcs function and verifying behavior.

    Args:
        temp_directory (str): Temporary directory path.
        monkeypatch (_pytest.monkeypatch.MonkeyPatch): Pytest fixture for monkeypatching.
    """
    uploader = FileUploader(
        None, None, None, "gcs_credentials.json", "gcs_bucket", {"document": "gcs"}
    )

    def mock_upload_to_gcs(file_path, filename):
        assert os.environ["GOOGLE_APPLICATION_CREDENTIALS"] == "gcs_credentials.json"
        assert filename in ["document1.pdf"]

    monkeypatch.setattr(uploader, "upload_to_gcs", mock_upload_to_gcs)
    uploader.upload_files(temp_directory)
