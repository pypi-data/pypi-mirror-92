import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agron_load",
    version="1.0.3",
    author="Ali Akhtari",
    author_email="hi@aliakh.me",
    description="Loader module for Agron data collection microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akhtariali/agron_load",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dotenv',
        'requests',
        'boto3'
    ],
    python_requires='>=3.8',
)
