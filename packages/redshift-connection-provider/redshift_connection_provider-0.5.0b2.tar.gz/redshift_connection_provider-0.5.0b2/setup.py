import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="redshift_connection_provider",
    version="0.5.0b2",
    description="An opinionated class to retrieve a Redshift connection object compatible with psycopg2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Andrea Amorosi",
    url="https://github.com/dreamorosi/redshift-connection-provider",
    packages=setuptools.find_packages(),
    install_requires=[
        "boto3~=1.16.57",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
