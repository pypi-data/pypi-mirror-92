import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="aio2b2t",
    version="1.0",
    author="DTOG",
    author_email="arstotzkanlool@gmail.com",
    description="aio2b2t is a modern, async, API wrapper for https://2b2t.dev and https://2b2t.io.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['aiohttp'],
    url="https://github.com/DontTreadOnGerman/aio2b2t",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)