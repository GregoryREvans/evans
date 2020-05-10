import pathlib
import subprocess
from return_directories import return_directories


def execute_shell_command(cmd, work_dir):
    pipe = subprocess.Popen(
        cmd, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (out, error) = pipe.communicate()
    print(out, error)
    pipe.wait()


def git_add(file_path, repo_dir):
    cmd = "git add " + file_path
    execute_shell_command(cmd, repo_dir)


def git_commit(commit_message, repo_dir):
    cmd = 'git commit -am "%s"' % commit_message
    execute_shell_command(cmd, repo_dir)


def git_push(repo_dir):
    cmd = "git push "
    execute_shell_command(cmd, repo_dir)


def push_scores():
    print("Pushing Scores ...")
    for score in return_diretories():
        score = str(score)
        print("git adding ...")
        git_add(file_path=score, repo_dir=score)
        print("git committing ...")
        git_commit(commit_message="Rerendered Segments.", repo_dir=score)
        print("git pushing ...")
        git_push(score)
