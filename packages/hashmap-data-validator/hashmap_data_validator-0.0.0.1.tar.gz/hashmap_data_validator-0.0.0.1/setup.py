import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hashmap_data_validator",
    version="0.0.0.1",
    author="Hashmap, Inc",
    author_email="accelerators@hashmapinc.com",
    description="A Python Package designed to validate data sources and sinks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hashmapinc/ctso/accelerators/data-engineering/hashmap_data_suite/hashmap-data-validator",
    packages=setuptools.find_packages(),
    package_data={
        "hdv": ["configurations/default_hdv_profiles.yml"],
    },
    install_requires=[
        'pyarrow==0.17.1',
        'pandas==1.1.4',
        'pyyaml==5.3.1',
        'snowflake-connector-python==2.3.6',
        'ipython==7.19.0',
        'jupyter==1.0.0',
        'snowflake-sqlalchemy==1.2.4',
        'SQLAlchemy==1.3.20',
        'jinjasql==0.1.8'

    ],
    entry_points={
        'console_scripts': [
            'hdv = hdv:cli_validate'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.7',
)