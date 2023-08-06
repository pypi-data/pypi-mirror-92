import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as requirements:
    REQUIREMENTS = requirements.readlines()

setuptools.setup(
    name="citibox-tracer",  # Replace with your own username
    version="0.1.3-rc3",  # Will change overtime
    author="Citibox",
    description="Citibox Google tracing tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://citibox.com",
    packages=setuptools.find_namespace_packages(include=["citibox.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=REQUIREMENTS
)
