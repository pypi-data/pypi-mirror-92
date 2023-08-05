import setuptools

PYTHON_VERSION="3.7"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automate-insurance-pricing", 
    version="1.0.4",
    author="Nassim Ezzakraoui",
    author_email="nassmim972@gmail.com",
    description="Bunch of functions for insurance pricing purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nassmim/automate-insurance-pricing",
    packages=setuptools.find_packages(),
    install_requires =[
        'chainladder~=0.7',
        'hyperopt~=0.2',
        'joypy~=0.2',
        'matplotlib~=3.1',
        'numpy~=1.18',
        'openpyxl~=3.0',
        'pandas~=1.0',
        'scikit-learn~=0.22',
        'scipy~=1.4',
        'seaborn~=0.10',
        'statsmodels~=0.11',
        'xlrd~=1.2',
        'XlsxWriter~=1.2',
        'xlwings~=0.19',        
        'docx-mailmerge~=0.5',        
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=' + PYTHON_VERSION,
)