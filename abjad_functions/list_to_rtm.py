nested_list = [1, 1, [1, [1, 1]], 1]

def nested_list_to_rtm(nested_list):
    out_string = ''
    for item in str(nested_list):
        if item == '[':
            out_string += '('
        if item == ']':
            out_string += ')'
        if str.isdigit(item):
            out_string += item
        if item == ' ':
            out_string += item
    return out_string

print(nested_list_to_rtm(nested_list))
