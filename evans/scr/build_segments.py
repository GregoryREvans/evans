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
build_path = pathlib.Path(__file__).parent
full_build_path = pathlib.Path(build_path).absolute()
scores = [f.path for f in os.scandir(build_path) if f.is_dir()]
for score in scores:
    if score[2:] == "__pycache__":
        continue
    elif score[2:] == "archive":
        continue
    elif score[2:] == "guerrero":
        continue
    elif score[2:] == "trio":
        continue
    elif score[2:] == "onkos":
        continue
    else:
        print(f"Now building {score[2:]} ...")
        segments_path = (build_path / score / score[2:] / "Segments").resolve()
        segments = [f.path for f in os.scandir(segments_path) if f.is_dir()]
        for x in segments:
            if x[-11:] == "__pycache__":
                segments.remove(x)
            else:
                print(f"Building {x} ...")
                os.system(f"python {x}/definition.py")
        score_path = f"{(full_build_path / score).resolve()}"
        os.system(f"black {score_path}")
        print("git adding ...")
        git_add(file_path=score_path, repo_dir=score_path)
        print("git committing ...")
        git_commit(commit_message="Rerendered Segments.", repo_dir=score_path)
        print("git pushing ...")
        git_push(score_path)
