from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="file_uploader_on_cloud",
    version="1.0.0",
    description="A file uploader library",
    author="Vipin Kumar Tripathi",
    packages=find_packages(),
    install_requires=requirements,
)
