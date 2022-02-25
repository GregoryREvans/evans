import datetime
import pathlib

import abjad
import evans
import quicktions

###
###
###


def sort_voices(nested_input_list, voice_dict, prefill=True):
    def helper(values):
        already_used = []
        out = {}
        for value in values:
            out[values[0][1][0][0]] = values[0][0]
            already_used.append(values[0][1][0][0])
            values.remove(values[0])
            for value_ in values:
                for term in value_[1]:
                    if term[0] in already_used:
                        value_[1].remove(term)
            if 1 < len(values):
                values = sorted(values, key=lambda _: _[1][1])
            else:
                out[values[0][1][0][0]] = values[0][0]
        return out

    for i in range(len(voice_dict)):
        voice_dict[f"voice {i + 1}"].append(nested_input_list[0][i])

    for chord in nested_input_list[1:]:
        ratio_closeness_values = []
        for ratio in chord:
            temp_vals = [
                (voice, abs(voice_dict[voice][-1] - ratio)) for voice in voice_dict
            ]
            sorted_temp_vals = sorted(temp_vals, key=lambda _: _[1])
            ratio_closeness_values.append((ratio, sorted_temp_vals))
        sorted_ratio_closeness_values = sorted(
            ratio_closeness_values, key=lambda _: _[1][1]
        )
        distribution_dict = helper(sorted_ratio_closeness_values)
        for key in distribution_dict.keys():
            voice_dict[key].append(distribution_dict[key])

    return voice_dict


def _extract_voice_info(score):
    score_pitches = []
    score_durations = []
    for voice in abjad.Selection(score).components(abjad.Voice):
        pitches = []
        durations = []
        for tie in abjad.Selection(voice).logical_ties():
            dur = abjad.get.duration(tie)
            durations.append(str(dur))
            if isinstance(tie[0], abjad.Rest):
                sub_pitches = ["Rest()"]
            else:
                if abjad.get.annotation(tie[0], "ratio"):
                    sub_pitches = [abjad.get.annotation(tie[0], "ratio")]
                else:
                    sub_pitches = [p.hertz for p in abjad.get.pitches(tie[0])]
            if 1 < len(sub_pitches):
                pitches.append([str(s) for s in sub_pitches])
            elif 0 == len(sub_pitches):
                pitches.append("Rest()")
            else:
                pitches.append(str(sub_pitches[0]))
        score_pitches.append(pitches)
        score_durations.append(durations)
    return [_ for _ in zip(score_pitches, score_durations)]


def make_sc_file(score, tempo, current_directory):

    info = _extract_voice_info(score)
    lines = "s.boot;\ns.quit;\n\n("

    for i, voice in enumerate(info):
        lines += f"\n\t// voice {i + 1}\n\t\tPbind(\n\t\t\t\\freq, Pseq(\n"

        lines += "\t\t\t\t[\n"
        for chord in voice[0]:
            lines += "\t\t\t\t\t[\n"
            if isinstance(chord, list):
                for _ in chord:
                    if _ == "Rest()":
                        lines += f"\t\t\t\t\t\t{_},\n"
                    else:
                        if _[0] == "[":
                            lines += f"\t\t\t\t\t\t{_[2:-2]},\n"
                        else:
                            lines += f"\t\t\t\t\t\t{_},\n"
            else:
                if chord == "Rest()":
                    lines += f"\t\t\t\t\t\t{chord},\n"
                else:
                    if chord[0] == "[":
                        lines += f"\t\t\t\t\t\t{chord[2:-2]},\n"
                    else:
                        lines += f"\t\t\t\t\t\t{chord},\n"
            lines += "\t\t\t\t\t],\n"
        lines += "\t\t\t\t],\n"
        lines += "\t\t\t),\n"
        lines += "\t\t\t\\dur, Pseq(\n\t\t\t\t[\n"
        for dur in voice[1]:
            lines += f"\t\t\t\t\t{quicktions.Fraction(dur) * 4} * {quicktions.Fraction(60, tempo[-1])},\n"
        lines += "\t\t\t\t]\n"
        lines += "\t\t\t,1),\n"
        lines += f"\t\t\t\\amp, {1 / len(info)},\n"
        lines += "\t\t\t\\legato, 1,\n\t\t).play;"

    lines += ")"

    with open(
        f'{current_directory}/voice_to_sc_{str(datetime.datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")}.scd',
        "w",
    ) as fp:
        fp.writelines(lines)


###
###
###

# trio 1
voices = {
    "voice 1": [],
    "voice 2": [],
    "voice 3": [],
}

s = evans.RatioSegment(["1/1", "6/5", "3/2"])

instructions = ["3/2", "4/5", "3/2", "4/5", "3/2", "4/5", "3/2", "4/5"]

out = [s]

for i in instructions:
    new = out[-1].multiply(i)
    out.append(new)

out_ = []
for sub_list in out:
    out_.append(list(sub_list))

voicewise_ratios = sort_voices(out_, voices)

handlers = []
fundamentals = ["c,", "c", "c'"]
voice_length = 0
for fundamental, voice in zip(fundamentals, voicewise_ratios):
    handlers.append(
        evans.PitchHandler(
            [evans.JIPitch(fundamental, ratio) for ratio in voicewise_ratios[voice]],
            forget=False,
        )
    )
    voice_length = len(voicewise_ratios[voice])

handlers.reverse()

fundamentals = ["c'1", "c1", "c,1"]

group = abjad.StaffGroup(
    [
        abjad.Staff(
            [abjad.Voice([abjad.Note(fundamentals[i_]) for i in range(voice_length)])]
        )
        for i_, voice in enumerate(voicewise_ratios)
    ]
)
abjad.attach(abjad.Clef("bass"), group[-1][0][0])

for handler, staff in zip(handlers, group):
    handler(staff)


# trio 2
voices = {
    "voice 1": [],
    "voice 2": [],
    "voice 3": [],
}

s = evans.RatioSegment(["1/1", "7/6", "3/2"])

instructions = ["2/3", "5/4", "2/3", "5/4", "2/3", "5/4", "2/3", "5/4"]

out = [s]

for i in instructions:
    new = out[-1].multiply(i)
    out.append(new)

out_ = []
for sub_list in out:
    out_.append(list(sub_list))

voicewise_ratios = sort_voices(out_, voices)

handlers = []
fundamentals = ["c", "c'", "c'"]
voice_length = 0
for fundamental, voice in zip(fundamentals, voicewise_ratios):
    handlers.append(
        evans.PitchHandler(
            [evans.JIPitch(fundamental, ratio) for ratio in voicewise_ratios[voice]],
            forget=False,
        )
    )
    voice_length = len(voicewise_ratios[voice])

handlers.reverse()

fundamentals = ["c'1", "c1", "c,1"]

group_2 = abjad.StaffGroup(
    [
        abjad.Staff(
            [abjad.Voice([abjad.Note(fundamentals[i_]) for i in range(voice_length)])]
        )
        for i_, voice in enumerate(voicewise_ratios)
    ]
)
abjad.attach(abjad.Clef("bass"), group_2[-1][0][0])
abjad.attach(abjad.Clef("bass"), group_2[-2][0][0])

for handler, staff in zip(handlers, group_2):
    handler(staff)

score = abjad.Score([group, group_2])
moment = "#(ly:make-moment 1 25)"
abjad.setting(score).proportional_notation_duration = moment

block = abjad.Block(name="score")
block.items.append(score)

style = '"dodecaphonic"'
layout = abjad.Block(name="layout")
layout.items.append(rf"\accidentalStyle {style}")

file = abjad.LilyPondFile(
    items=[
        r'\include "/Users/gregoryevans/abjad/abjad/_stylesheets/ekmelos-ji-accidental-markups.ily"',
        layout,
        block,
    ]
)

abjad.show(file)

make_sc_file(
    score=score,
    tempo=((1, 4), 10),
    current_directory=pathlib.Path(__file__).parent,
)
