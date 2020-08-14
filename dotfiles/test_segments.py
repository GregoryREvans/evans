import difflib
import os
import pathlib
import shutil
import subprocess
import sys

import abjad
import pytest

test_path = pathlib.Path(__file__).parent
travis_build_dir = os.environ.get("TRAVIS_BUILD_DIR")
assert isinstance(travis_build_dir, str)
wrapper = pathlib.Path(travis_build_dir)
segments_dir = wrapper / wrapper.name / "segments"
segments = []
for path in sorted(segments_dir.iterdir()):
    if not path.is_dir():
        continue
    if path.name == "__pycache__":
        continue
    segments.append(path)


@pytest.mark.parametrize("segment", segments)
def test_segments_01(segment):
    # write ls to log
    log = f"/tmp/{segment.name}.before.log"
    command = f"ls --full-time {segment}"
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True,
    )
    with open(log, "w") as pointer:
        pointer.write(process.stdout)
    #
    ly = f"{segment}/illustration.ly"
    ly_old = f"{segment}/illustration.old.ly"
    if os.path.exists(ly):
        shutil.copyfile(ly, ly_old)
    log = f"/tmp/{segment.name}.log"
    command = f"python {segment}/definition.py"
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True,
    )
    with open(log, "w") as pointer:
        pointer.write(process.stdout)
    # write ls to log
    log = f"/tmp/{segment.name}.after.log"
    command = f"ls --full-time {segment}"
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        shell=True,
    )
    with open(log, "w") as pointer:
        pointer.write(process.stdout)
    #
    # if exit_code != 0:
    #     sys.exit(exit_code)
    if not os.path.exists(ly_old):
        return
    assert os.path.exists(ly)
    assert os.path.exists(ly_old)
    if not abjad.iox.compare_files(ly_old, ly):
        ly_old_text = open(ly_old, "r")
        ly_old_text = ly_old_text.read()
        ly_text = open(ly, "r")
        ly_text = ly_text.read()
        print("".join(difflib.ndiff(ly_old_text, ly_text)))
        sys.exit(1)
