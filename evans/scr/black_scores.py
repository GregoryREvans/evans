import os
from return_directories import return_directories


def black_scores():
    print("Formatting Scores ...")
    for score in return_directories():
        os.system(f"black {score}")
