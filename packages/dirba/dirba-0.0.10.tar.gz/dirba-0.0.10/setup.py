import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dirba",
    version="0.0.10",
    author="Mansur Izert",
    author_email="izertmi@uriit.ru",
    description="Small ML boilerplate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://git2.uriit.local/CIAS/dirba.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests',
                      'fastapi>=0.61.0',
                      'pydantic>=1.4',
                      'python-multipart>=0.0.5',
                      'uvicorn>=0.11.3',
                      'aiokafka>=0.6.0',
                      'pandas>=1.0.1',
                      'aiomisc',
                      'aiohttp',
                      'orjson',
                      'scikit-learn'],
)
