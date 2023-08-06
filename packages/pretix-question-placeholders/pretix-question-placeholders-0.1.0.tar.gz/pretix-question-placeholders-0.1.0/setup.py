import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_question_placeholders import __version__


try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ""


class CustomBuild(build):
    def run(self):
        try:
            management.call_command("compilemessages", verbosity=1)
        except Exception:
            pass
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretix-question-placeholders",
    version=__version__,
    description="Add content to your emails based on the questions the customer answered, and the answer they gave.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/rixx/pretix-question-placeholders",
    author="Tobias Kunze",
    author_email="r@rixx.de",
    license="Apache",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_question_placeholders=pretix_question_placeholders:PretixPluginMeta
""",
)
