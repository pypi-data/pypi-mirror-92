# automate-insurance-pricing

## Introduction
Library gathering a bunch of modules aiming at speeding up usual tasks dealing with data prep, visualization, profitability analysis and risk modelling in insurance field.


# Getting Started

## 1.	Installation process

To install use pip: pip install automate-insurance-pricing

Alternatively, install directly from github: pip install git+https://github.com/nassmim/automate-insurance-pricing

* Note: This package requires Python 3.7 and later.* 


## 2.	Sub modules and functions

This library is composed of several modules families: 
* data exploration
* data preprocessing
* profitability analysis
* risk modelling
* results exportation
* other functions less specific

To import all modules from the family taks abc: from automate_insurance_pricing import abc

To import a specific module def from the family taks abc: from automate_insurance_pricing.abc import def

To import all functions from a specific module def within the family abc : from automate_insurance_pricing.abc.def import *


## 3.	Software/Libraries dependencies

Several libraries will be automatically installed when you install our library. Below is a non-exhaustive list of the packages that will be installed.

* *pandas~=1.0*
* *numpy~=1.18*
* *scikit-learn~=0.22*
* *scipy~=1.4*
* *chainladder~=0.7*
* *hyperopt~=0.2*
* *joypy~=0.2*
* *matplotlib~=3.1*
* *openpyxl~=3.0*
* *seaborn~=0.10*
* *statsmodels~=0.11*
* *xlrd~=1.2*
* *XlsxWriter~=1.2*
* *xlwings~=0.19*

If some packages are not installed automatically, please do it manually.

## 4.	Warnings
Reports module is too specific and cannot be reused as it is. Will be re-worked to be more general. 


# Contribute
Anyone willing to make this library more exhaustive, more generic and efficient. 
