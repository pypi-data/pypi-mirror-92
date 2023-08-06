import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='python_llk_model',
    version='0.0.1',
    description='it is a test!',
    maintainer='llk',
    maintainer_email='2838132019@qq.com',
    license='Apache-2.0',
    url='http://iwhynot.com',
    packages=setuptools.find_packages(),
    zip_safe=False,
    long_description="",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)