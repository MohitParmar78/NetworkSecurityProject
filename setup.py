from setuptools import find_packages,setup
from typing import List

def get__requirements()->List[str]:
    """
    This function will return list of requirements
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #read lines from the file
            lines=file.readlines();
            #process each lne
            for line in lines:
                requirement=line.strip();
                #ignore empty lines and  -e.
                if requirement and requirement !='-e .':
                    requirement_lst.append(requirement)
    
    except FileNotFoundError:
        print("requirements.txt file not found")
        
    return requirement_lst 

setup(
    name="Network Security",
    version="0.0.1",
    author="mohit",
    author_email="mohitrajput61678@gmail.com",
    packages=find_packages(),
    install_requires=get__requirements()
)
                       