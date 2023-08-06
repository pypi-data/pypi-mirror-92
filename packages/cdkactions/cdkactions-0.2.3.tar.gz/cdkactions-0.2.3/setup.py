import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdkactions",
    "version": "0.2.3",
    "description": "Cloud Development Kit for GitHub Actions",
    "license": "Apache-2.0",
    "url": "https://github.com/ArmaanT/cdkactions.git",
    "long_description_content_type": "text/markdown",
    "author": "Armaan Tobaccowalla<armaan@tobaccowalla.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/ArmaanT/cdkactions.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdkactions",
        "cdkactions._jsii"
    ],
    "package_data": {
        "cdkactions._jsii": [
            "cdkactions@0.2.3.jsii.tgz"
        ],
        "cdkactions": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "constructs>=3.2.109, <4.0.0",
        "jsii>=1.17.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
