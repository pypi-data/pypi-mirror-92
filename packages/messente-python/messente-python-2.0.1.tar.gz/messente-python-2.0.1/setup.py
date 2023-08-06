# -*- coding: utf-8 -*-

import re

from setuptools import setup

VERSION_PATTERN = ".*==[^\\s]+"

with open("requirements.txt") as prod_requirements_file:
    PROD_REQUIREMENTS = re.findall(
        VERSION_PATTERN, prod_requirements_file.read()
    )

with open('README.md') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name="messente-python",
    version="2.0.1",
    packages=["messente.api.sms", "messente.api.sms.api"],
    install_requires=PROD_REQUIREMENTS,
    author="Messente",
    author_email="messente@messente.com",
    description="Messente SMS API",
    license="Apache-2.0",
    keywords=["messente", "sms", "verification", "2FA", "pincode"],
    url="https://github.com/messente/messente-python",
    python_requires="~=3.6",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown'
)
