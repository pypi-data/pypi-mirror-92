from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='shaizae_fp',
    version='0.0.1',
    description='a grate machine learning tool for beginners and dummies :)',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='shai zaedman',
    author_email='shaizae10@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='machine learning',
    packages=find_packages(),
    install_requires=['sklearn', 'scipy', 'imblearn', 'pandas', 'xgboost', 'matplotlib']
)
