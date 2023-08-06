from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='BasicDeepLearningFramework',
    version='0.1.0',
    description='A Deep learning framework can be used to build deep learning models and CNNS',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Omar Hatem',
    author_email='omarhatem221@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='deep learning framework',
    packages=["Deep_Learning_Framework"],
    install_requires=['numpy', 'pandas', 'matplotlib', 'Pillow']
)