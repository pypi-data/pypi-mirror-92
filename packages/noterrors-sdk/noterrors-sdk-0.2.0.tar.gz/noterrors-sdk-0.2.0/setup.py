import setuptools


setuptools.setup(
     name='noterrors-sdk',
     version='0.2.0',
     author="noterrors",
     author_email="jarod@ukr.net",
     description="NotErrors SDK for Python",
     long_description=open("README.md").read(),
     long_description_content_type="text/markdown",
     url="https://github.com/jarodut/noterrors-sdk",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
