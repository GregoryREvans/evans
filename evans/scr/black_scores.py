import os
from return_directories import return_directories


print("Formatting Scores ...")


def black_scores():
    for score in return_directories():
        os.system(f"black {score}")
