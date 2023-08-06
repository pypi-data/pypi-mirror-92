import sys
import os
from setuptools import setup
from setuptools import find_packages

m_version = '1.1'

if sys.argv[1] == "publish":
    os.system("python3 setup.py sdist")
    os.system("python3 setup.py bdist_wheel")
    os.system("twine upload dist/*{}*".format(m_version))
else:
    setup(
        name='ylogger',
        version=m_version,
        author='Z-Z Ma',
        description="a logger, see https://github.com/xxmawhu/zlogger",
        packages=find_packages(),
        license="GPL",
        project_urls={
            'Source': 'https://github.com/xxmawhu/zlogger',
        },
    )
