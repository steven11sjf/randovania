from __future__ import annotations

import logging
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel

try:
    from pyqt_distutils.build_ui import build_ui
except ModuleNotFoundError:
    build_ui = None


class BuildPyCommand(build_py):
    def run(self):
        self.run_command("build_ui")
        super().run()


class BDistWheelCommand(bdist_wheel):
    def run(self):
        self.run_command("build_ui")
        super().run()


def version_scheme(version):
    import setuptools_scm
    from dulwich.repo import Repo

    assert isinstance(version, setuptools_scm.version.ScmVersion)
    assert isinstance(version.config, setuptools_scm.Configuration)

    git_repo = Repo(version.config.absolute_root)
    full_git_hash = repr(git_repo.head().decode("ascii"))
    try:
        git_hash = repr(bytes.fromhex(version.node[1:9]))
    except ValueError:
        logging.exception("Unable to get git hash from version %s", str(version.node))
        git_hash = None

    # We want to save the git hash to a file, so we can easily access it in frozen runtime, where git is not available.
    #
    Path(version.config.absolute_root).joinpath("randovania/version_hash.py").write_text(
        f"""# coding: utf-8
# file generated by setuptools_scm + setup.py
# don't change, don't track in version control
git_hash = {git_hash}
full_git_hash = {full_git_hash}
git_branch = {version.branch!r}
dirty = {version.dirty}
"""
    )

    if version.exact:
        result = setuptools_scm.version.guess_next_simple_semver(
            version, retain=setuptools_scm.version.SEMVER_LEN, increment=False
        )
    else:
        if version.branch != "stable":
            retain = setuptools_scm.version.SEMVER_MINOR
        else:
            retain = setuptools_scm.version.SEMVER_PATCH
        result = version.format_next_version(setuptools_scm.version.guess_next_simple_semver, retain=retain)
    return result


setup(
    use_scm_version={
        "version_scheme": version_scheme,
        "local_scheme": "no-local-version",
        "write_to": "randovania/version.py",
        "git_describe_command": [
            "git",
            "describe",
            "--dirty",
            "--tags",
            "--long",
            "--match",
            "v[0-9]*",
        ],
    },
    cmdclass={
        "build_ui": build_ui,
        "build_py": BuildPyCommand,
        "bdist_wheel": BDistWheelCommand,
    },
)
