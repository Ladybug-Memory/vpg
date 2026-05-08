from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.bdist_wheel import bdist_wheel

ROOT = Path(__file__).resolve().parent
PY_LIBRARY = ROOT / "build" / "libvpg_python.so"


class BuildPy(build_py):
    def run(self) -> None:
        subprocess.run(["make", "python-lib"], cwd=ROOT, check=True)
        super().run()

        target_dir = Path(self.build_lib) / "vpg"
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PY_LIBRARY, target_dir / "libvpg_python.so")


cmdclass = {"build_py": BuildPy}


class BinaryWheel(bdist_wheel):
    def finalize_options(self) -> None:
        super().finalize_options()
        self.root_is_pure = False


cmdclass["bdist_wheel"] = BinaryWheel


setup(cmdclass=cmdclass)
