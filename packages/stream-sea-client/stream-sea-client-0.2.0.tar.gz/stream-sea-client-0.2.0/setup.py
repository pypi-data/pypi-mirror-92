import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stream-sea-client",
    version="0.2.0",
    author="Sergei Patiakin",
    author_email="sergei@portchain.com",
    description="Stream-sea client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Portchain/stream-sea-client-python",
    packages=['stream_sea_client'],
    license='Proprietary',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests~=2.24',
        'websockets~=8.1',
    ]
)
