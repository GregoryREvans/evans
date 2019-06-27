lines = open("/Users/evansdsg2/evans/general_tools/test_file.txt").readlines()
open("/Users/evansdsg2/evans/general_tools/new_file.txt", "w").writelines(lines[1:-1])
