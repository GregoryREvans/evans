from evans.general_tools.human_keys import human_sorted_keys

voice_dict_list = {
    "voice 6 key": "voice 6 item",
    "voice 10 key": "voice 10 item",
    "voice 1 key": "voice 1 item",
}

item_list = [x for x in voice_dict_list]

item_list.sort(key=human_sorted_keys)


sorted_voice_dict = {_: voice_dict_list[_] for _ in item_list}
