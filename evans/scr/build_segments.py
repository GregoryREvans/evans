import os
import pathlib
import subprocess


def execute_shell_command(cmd, work_dir):
    pipe = subprocess.Popen(cmd, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    print(out, error)
    pipe.wait()

def git_add(file_path, repo_dir):
    cmd = 'git add ' + file_path
    execute_shell_command(cmd, repo_dir)

def git_commit(commit_message, repo_dir):
    cmd = 'git commit -am "%s"' % commit_message
    execute_shell_command(cmd, repo_dir)

def git_push(repo_dir):
    cmd = 'git push '
    execute_shell_command(cmd, repo_dir)

print("Building Scores ...")
ignores = ("archive", "guerrero", "trio", "onkos")
build_path = pathlib.Path("/Users/evansdsg2/Scores")
for score in build_path.iterdir():
    if not score.is_dir():
        continue
    if score.name in ignores:
        continue
    print(f"Now building {score.name} ...")
    segments_path = score / score.name / "Segments"
    for x in segments_path.iterdir():
        if x.name.startswith("_"):
            continue
        print(f"Building {x} ...")
        os.system(f"python {x}/definition.py")
    os.system(f"black {score}")
    score = str(score)
    print("git adding ...")
    git_add(file_path=score, repo_dir=score)
    print("git committing ...")
    git_commit(commit_message="Rerendered Segments.", repo_dir=score)
    print("git pushing ...")
    git_push(score)
