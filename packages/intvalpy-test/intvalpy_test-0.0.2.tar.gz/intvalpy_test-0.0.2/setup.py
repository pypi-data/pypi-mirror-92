import io
import os
from setuptools import setup, find_packages

os.environ['CVXOPT_BUILD_GLPK'] = '1'

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with io.open(readme_file, mode='r', encoding='utf-8') as f:
    README = f.read()

INSTALL_REQUIRES = [
    'joblib',
    'matplotlib',
    'numpy',
    'scipy'
]

setup(
    name='intvalpy_test',
    version='0.0.2',
    description='Interval library in Python using classical interval ' + \
                'arithmetic + Kahan division in some functions',
    long_description=README,
    author='Андросов Артем Станиславович',
    author_email='artem.androsov@gmail.com',
    url='https://github.com/AndrosovAS/intvalpy',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES
)
