from distutils.core import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cutoml',
    packages=['cutoml'],
    version='0.0.4',
    license='gpl-3.0',
    description='A lightweight automl framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Omkar Udawant',
    author_email='omkarudawant97@gmail.com',
    url='https://github.com/omkarudawant/CutoML',
    download_url='https://github.com/omkarudawant/CutoML/archive/0.0.4.tar.gz',
    keywords=[
        'automl',
        'pipeline optimization',
        'hyperparameter optimization',
        'data science',
        'machine learning',
    ],
    install_requires=[
        'scipy==1.6.0',
        'numpy==1.19.5',
        'scikit-learn==0.24.1',
        'pydantic==1.6.1',
        'xgboost==1.3.2'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: GNU Lesser General Public License v3 ('
        'LGPLv3)',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
