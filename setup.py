from setuptools import setup, find_packages
setup(
    name = "salesman",
    version = "0.0.1",
    description = "Automatic Link Checker",
    author = "Kyle Conroy",
    author_email = "kyle.j.conroy@gmail.com",
    url = "http://github.com/derferman/salesman/",
    keywords = ["http","checker"],
    install_requires = ["restkit", "lxml", "gevent"],
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'salesman = salesman.cmd_line:main',
            ]
        },
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    long_description = "Traveling Salesman")
