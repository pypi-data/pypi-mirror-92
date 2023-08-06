import pathlib
from setuptools import setup  # type: ignore


setup(
    name="dynamo-dao",
    version="0.0.7",
    description="Dynamo Dao",
    author="Quinn Weber",
    author_email="quinn@quinnweber.com",
    maintainer="Quinn Weber",
    maintainer_email="quinn@quinnweber.com",
    url="https://github.com/qsweber/dynamo-dao",
    license="MIT",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"dynamo_dao": ["py.typed"]},
    packages=["dynamo_dao"],
    package_dir={"": "src"},
    install_requires=["Boto3"],
)
