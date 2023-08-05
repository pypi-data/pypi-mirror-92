from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='wsit',
      version='1.0.14',
      author='VMS Software, Inc.',
      description='Web Services Integration Toolkit',
      long_description=long_description,
      url="https://vmssoftware.com/products/web-services-integration-toolkit/",
      license='MIT',
      long_description_content_type="text/markdown",
      packages=find_packages(),
      include_package_data=False,
      zip_safe=False, install_requires=['wsit-interface', 'numpy', 'pytest'])

