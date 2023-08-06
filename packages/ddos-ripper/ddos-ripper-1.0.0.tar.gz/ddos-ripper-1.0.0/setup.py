from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ddos-ripper',
    packages=find_packages(),
    include_package_data=True,
    version='1.0.0',
    author='Palahsu',
    author_email='jk3502072@gmail.com',
    url='https://github.com/palahsu/DDoS-Ripper',
    download_url='https://github.com/palahsu/DDoS-Ripper.git',
    description="DDos Ripper a Distributable Denied-of-Service (DDOS) attack server that cuts off targets or surrounding infrastructure in a flood of Internet traffic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MPL",
    keywords=['DDoS-Ripper', 'ddos-ripper', 'DDOS', 'DOS', 'ddosripper',
              "dos-attacks", "denial-of-service", "palahsu", "http", 
    "exploit", "dos-tool", "hacker-scripts", "hacking-tool", "hacking", "vulnerability", "slow-requests",
    "cybersecurity", "cyber-security", "information-security", "security"
              'Denial of Service'],
    install_requires=[
        '',
        'queue',
        'sys',
        'time',
        'optparse',
        'setuptools',
        'socket',
        'threading',
        'logging',
        'urllib.request',
        'random'
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
],

)
