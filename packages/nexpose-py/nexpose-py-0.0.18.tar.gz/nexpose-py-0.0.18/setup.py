import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nexpose-py",
    version="0.0.18",
    author="Noah Birnel",
    author_email="noah.birnel@coalfire.com",
    description="Python3 bindings and CLI tools for Nexpose API version 3",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/coalfire/nexpose-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: System :: Networking",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.6",
    scripts = [
        "bin/nsc-delete-user",
        "bin/nsc-engine-pools",
        "bin/nsc-exporter",
        "bin/nsc-janitor",
        "bin/nsc-make-exporter-privileges",
        "bin/nsc-remove-old-reports",
        "bin/nsc-remove-old-sites",
        "bin/nsc-users",
    ],
    install_requires=[
        "urllib3>=1.10.0",
        "requests>=2.6.0",
        "wheel",
        "configargparse",
        "prometheus_client",
    ],
    setup_requires=[
        "wheel",
    ],
    data_files=[
        ('etc/default', ['extras/nexpose-exporter.env']),
        ('etc/systemd/system', ['extras/nexpose-exporter.service']),
        ('etc/default', ['extras/nexpose-janitor.env']),
        ('etc/systemd/system', ['extras/nexpose-janitor.service']),
    ],
)
