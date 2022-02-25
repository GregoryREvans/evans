# import abjad
# import evans
# from abjadext import microtones
#
# ###
# ###
# ###
#
#
# def sort_voices(nested_input_list):
#
#     voices = {
#         f"voice {_}": [nested_input_list[0][_]]
#         for _ in range(len(nested_input_list[0]))
#     }
#
#     for l in out_[1:]:
#         already_used = []
#         for ratio in l:
#             temp_vals = [(i, abs(voice[-1] - ratio)) for i, voice in ennumerate(voices)]
#             sorted_temp_vals = sorted(temp_vals, key=lambda _: _[1])
#             smallest = sorted_temp_vals[0]
#             selected_voice = f"voice {smallest[0]}"
#             if selected_voice in already_used:
#                 for pair in sorted_temp_vals:
#                     if pair[0][-1] == pair[0]:
#                         sorted_temp_vals.remove(pair)
#                 # sort_voices(sorted_temp_vals)
#
#             else:
#                 voices[selected_voice].append(ratio)
#                 already_used.append(selected_voice)
#
#
# ###
# ###
# ###
#
# s = evans.RatioSegment(["1/1", "6/5", "3/2"])
# instructions = ["3/2", "4/5", "3/2", "4/5", "3/2", "4/5", "3/2", "4/5"]
# out = [s]
# for i in instructions:
#     new = out[-1].multiply(i)
#     out.append(new)
#
# out_ = []
# for l in out:
#     out_.append(list(l))
#
# voicewise_ratios = sort_voices(out_)
