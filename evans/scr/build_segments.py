import os
from return_directories import return_directories


def build_segments():
    print("Building Scores ...")
    for score in return_directories():
        print(f"Now building {score.name} ...")
        segments_path = score / score.name / "Segments"
        for segment in segments_path.iterdir():
            if segment.name.startswith("_"):
                continue
            if segment.name.startswith("."):
                continue
            print(f"Building {segment} ...")
            os.system(f"python {segment}/definition.py")
