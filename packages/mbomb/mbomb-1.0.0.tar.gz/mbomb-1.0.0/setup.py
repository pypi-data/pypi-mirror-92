from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mbomb',
    packages=find_packages(),
    include_package_data=True,
    version='1.0.0',
    author='Palahsu',
    author_email='jk3502072@gmail.com',
    url='https://github.com/palahsu/MBomb',
    download_url='https://github.com/palahsu/MBomb.git',
    description="MBomb(Gmail To Gmail) Mail Bombing! Send Unlimited Bombing on Inbox!",
    long_description=long_description,
    license="LGPLv3",
    long_description_content_type="text/markdown",
    keywords=["mbomb", "mail-bomb", "mail-bombing", "palahsu", "bombing", 
    "exploit", "tool", "unlimited-message", "message", "hacker-scripts", "hacking-tool", "hacking", "vulnerability", "bomber",
    "cybersecurity", "cyber-security", "information-security", "security"
              "messages"],
    install_requires=[
        '',
        'os'
        'random'
        'smtplib'
        'sys'
        'getpass'
        'time'
        'tqdm'
        'colorama'
        'urllib.request',
        'random'
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
],

)
