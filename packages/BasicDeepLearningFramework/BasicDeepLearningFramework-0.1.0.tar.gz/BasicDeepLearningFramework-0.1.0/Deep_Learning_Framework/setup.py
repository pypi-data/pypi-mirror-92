from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='DeepLearningFramework',
    version='0.0.1',
    description='A Deep learning framework can be used to build deep learning models and CNNS',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Omar Hatem',
    author_email='omarhatem221@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='deep learning framework',
    packages=find_packages["Deep-Learning-Framework"],
    install_requires=['numpy', 'pandas', 'matplotlib', 'Pillow']
)