
"""
This script is a setup file typically used in Python projects to define metadata and configuration for the package. 
It is used to specify details such as the package name, version, author, dependencies, and other relevant information. 
The setup file is essential for packaging and distributing the project, making it easier for others to install and use.

# Why setup file is used:
# The setup file is used to automate the installation process, manage dependencies, and provide metadata about the project. 
# It ensures that the package can be easily shared and installed in a consistent manner.
"""
from setuptools import find_packages, setup
from typing import List

def get_requiremnts()->List(str):
    ## this function will return the list of requirements
    try:
        with open("requirements.txt","r") as f:
            lines=f.readlines()
            for line in lines:
                requirement=line.strip()
                # ignore empty lines and comments
                if requirement and requirement!="-e .":
                    requirement_lst.append(requirement) 
    except FileNotFoundError:
        print("requirements.txt file not found")

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Akhilesh",
    author_email="akhileshkovelakuntla@gmail.com",
    packages=find_packages(),
    install_requires=get_requiremnts(),
)