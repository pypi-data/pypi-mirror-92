import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudenv", # Replace with your own username
    version="0.1.1",
    author="Lucas Carlson",
    author_email="lucas@carlson.net",
    description="Keep Your Environmental Variables Secure And In Sync",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cloudenvhq/cloudenv-python/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
