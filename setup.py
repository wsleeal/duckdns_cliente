from setuptools import setup

setup(
    name="duckdns",
    version="0.0.12",
    url="https://github.com/wsleeal/duckdns_cliente",
    license="MIT",
    author="William Leal",
    author_email="wsleal@yahoo.com",
    description="Atualiza DuckDNS",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    long_description_content_type="text/markdown",
    keywords=["ddns"],
    packages=["duckdns"],
    include_package_data=True,
    package_data={"": ["favicon.ico"]},
    install_requires=[
        "pytz==2021.3",
        "requests==2.26.0",
        "pystray==0.19.1",
    ],
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": [
            "duckdns=duckdns:show",
        ],
    },
)
