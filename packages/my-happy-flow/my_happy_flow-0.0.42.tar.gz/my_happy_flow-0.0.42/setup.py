import pathlib
from setuptools import setup, find_packages

import versioneer

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

install_requires = [
            'ray>=1.1.0',
            'modin>=0.8.3'
        ]

from happy_python_utils import version

setup(
  name="my_happy_flow",
  version=versioneer.get_version(),
  description="From data to information. Peformance first with easy use.",
  long_description=README,
  long_description_content_type="text/markdown",
  license="A",
  url="https://github.com/ggservice007/my-happy-flow",
  author="ggservice007",
  author_email="ggservice007@126.com",
  packages=find_packages(include=["src"], exclude=[""]),
  install_requires=install_requires,
  include_package_data=True,
  zip_safe=False
)
