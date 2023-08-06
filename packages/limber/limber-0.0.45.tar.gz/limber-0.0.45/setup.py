'''
setup.py - a setup script
Copyright (C) 2020 Stijn Zanders
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Authors:
    Stijn Zanders <zandersstijn@gmail.com>
'''

import setuptools

with open ("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="limber",
    version="0.0.45",
    entry_points={
            'console_scripts': ['limber=limber.__main__:cli'],
        },
    scripts=[],
    install_requires=[
        "pyyaml==5.3.1",
        "click==7.1.2",
        "python-dotenv==0.15.0",
        "google-cloud-pubsub==2.2.0",
        "google-cloud==0.34.0",
        "mergedeep==1.3.1",
    ],
    author="Stijn Zanders",
    author_email="zandersstijn@gmail.com",
    description="Serverless DAGs orchestrated via Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StijnZanders/limber",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ]
)
