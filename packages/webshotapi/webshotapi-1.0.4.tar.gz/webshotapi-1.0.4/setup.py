from setuptools import setup, find_packages
from webshotapi import version
with open('README.md','r') as r:
    long_description = r.read()

setup(
    name='webshotapi', 
    version=version.__version__,
    packages=find_packages(),
    author="WebShotApi.com",
    author_email="contact@webshotapi.com",
    description="Api client for WebShotApi.com. \
        Website screenshot api client, \
        extract html from rendered website \
        extract words with coordinates from website, \
        extract styles from HTML selectors(elements)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://webshotapi.com/clients/python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/webshotapi/website-screenshot-python-client/issues",
        "Documentation": "https://webshotapi.com/docs/python/",
        "Source Code": "https://github.com/webshotapi/website-screenshot-python-client",
    },
    licence="MIT",
    install_requires=[
        x.strip()
        for x in open('requirements.txt').readlines()
        if x and not x.startswith('#')
    ],
    python_requires='>=3.6',
)