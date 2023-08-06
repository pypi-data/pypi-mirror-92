import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_log_read_access import __version__


try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretix-log-read-access",
    version=__version__,
    description="This plugin logs any access to extended information (e.g. question answers) of a specific order, as well as all export jobs. No warranty for completeness given.",
    long_description=long_description,
    url="https://github.com/pretix-unofficial/pretix-log-read-access",
    author="pretix team",
    author_email="support@pretix.eu",
    license="Apache",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_log_read_access=pretix_log_read_access:PretixPluginMeta
""",
)
