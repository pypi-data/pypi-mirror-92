from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

setup(
    name="netack",
    version="0.2.0",
    description="python library for basic network attacks",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author="Akash Sharma and Akshat Sharma",
    License="MIT",
    classifiers= classifiers,
    keywords="network security",
    packages=find_packages(),
    install_requires=['scapy']
)
