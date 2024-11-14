from setuptools import setup, find_packages

setup(
    name="RiskLab-2",  
    version="1.0.0",  
    description="Creating a Model to find correlation with ESG announcements and Stock Price",
    author="Michael Plaza",  
    author_email="mplaza0627@gmail.com", 
    packages=find_packages(),
    install_requires=[
        'pandas==2.2.3',
        'openpyxl==3.1.5'
    ],  # The required dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
