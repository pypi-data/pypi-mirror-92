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
    version="2.0.0",
    packages=["messente.api.sms", "messente.api.sms.api"],
    install_requires=PROD_REQUIREMENTS,
    author="Messente.com",
    author_email="support@messente.com",
    description="Official Messente.com API library",
    license="Apache License, Version 2",
    keywords="messente sms verification 2FA pincode",
    url="http://messente.com/documentation/",
    test_suite="messente.api.sms.test",
    python_requires="==3.6.*",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown'
)
