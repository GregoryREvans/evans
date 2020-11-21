import pathlib


def return_directories(p="/Users/evansdsg2/Scores", ignores=("archive", ".mypy_cache")):
    build_path = pathlib.Path(p)
    returns = []
    for score in sorted(build_path.iterdir()):
        if not score.is_dir():
            continue
        if score.name in ignores:
            continue
        else:
            returns.append(score)
    return returns
