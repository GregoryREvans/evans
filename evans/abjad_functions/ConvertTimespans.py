import abjad
import abjadext.rmakers
import os
import pathlib
import time
from tsmakers.PerformedTimespan import PerformedTimespan
from evans.AttachmentHandlers.CyclicList import CyclicList
from evans.AttachmentHandlers.RhythmHandler import RhythmHandler
from evans.abjad_functions.talea_timespan import timespan_functions
from collections import defaultdict
from evans.general_tools.sorted_keys import sorted_keys
from evans.abjad_functions.timespan_human_keys import human_sorted_keys


silence_maker = abjadext.rmakers.stack(
    abjadext.rmakers.NoteRhythmMaker(),
    abjadext.rmakers.force_rest(abjad.select().leaves(pitched=True)),
)

silence_maker = RhythmHandler(rmaker=silence_maker, name="silence maker")


class ConvertTimespans:
    def __init__(
        self,
        materials,
        ts_list,
        bounds,
        persist=False,
        segment_name=None,
        current_directory=None,
        fill_gaps=True,
    ):
        self.materials = materials
        self.ts_list = ts_list
        self.bounds = bounds
        self.persist = persist
        self.segment_name = segment_name
        self.current_directory = current_directory
        self.fill_gaps = fill_gaps

    def __call__(self):
        self.convert_timespans(self.materials, self.ts_list, self.bounds)

    def convert_timespans(
        materials,
        ts_list,
        bounds,
        segment_name,
        current_directory,
        add_silence=True,
        fill_gaps=True,
        split=False,
        is_global=False,
    ):

        cyclic_materials = CyclicList(materials, continuous=True)

        master_list = []

        groups = [timespan.voice_name for timespan in ts_list]
        input = [(span, group) for span, group in zip(ts_list, groups)]
        res = defaultdict(list)
        for v, k in input:
            res[k].append(v)
        voice_dict_list = [
            {"voice": k, "items": abjad.TimespanList(v)} for k, v in res.items()
        ]

        item_list = [x["voice"] for x in voice_dict_list]
        item_list.sort(key=sorted_keys)
        sorted_voice_dict_list = []
        for key in item_list:
            for span_dict in voice_dict_list:
                if span_dict["voice"] == key:
                    sorted_voice_dict_list.append(span_dict)

        for i, timespan_dict in enumerate(sorted_voice_dict_list):
            ts_list = abjad.TimespanList()
            for timespan in timespan_dict["items"]:
                if isinstance(timespan, abjad.AnnotatedTimespan):
                    if is_global is False:
                        timespan.annotation = timespan_functions.TimespanSpecifier(
                            voice_name=f"Voice {i}", handler=cyclic_materials(r=1)[0]
                        )
                        ts_list.append(timespan)
                    else:
                        timespan.annotation = timespan_functions.TimespanSpecifier(
                            voice_name=f"Global Context", handler=cyclic_materials(r=1)[0]
                        )
                        ts_list.append(timespan)
                elif isinstance(timespan, PerformedTimespan):
                    if is_global is False:
                        timespan = abjad.AnnotatedTimespan(
                            start_offset=timespan.start_offset,
                            stop_offset=timespan.stop_offset,
                            annotation=timespan_functions.TimespanSpecifier(
                                voice_name=f"Voice {i}", handler=cyclic_materials(r=1)[0]
                            ),
                        )
                        ts_list.append(timespan)
                    else:
                        timespan = abjad.AnnotatedTimespan(
                            start_offset=timespan.start_offset,
                            stop_offset=timespan.stop_offset,
                            annotation=timespan_functions.TimespanSpecifier(
                                voice_name=f"Global Context", handler=cyclic_materials(r=1)[0]
                            ),
                        )
                        ts_list.append(timespan)
                else:
                    if fill_gaps is True:
                        if add_silence is True:
                            timespan.annotation = timespan_functions.TimespanSpecifier(
                                voice_name=f"Voice {i}", handler=silence_maker
                            )
                            ts_list.append(timespan)
                        else:
                            timespan.annotation = timespan_functions.TimespanSpecifier(
                                voice_name=f"Voice {i}",
                                handler=cyclic_materials(r=1)[0],
                            )
                            ts_list.append(timespan)
                    else:
                        continue
            ts_list.sort()
            master_list.append(ts_list)

        showable_list = abjad.TimespanList()
        for x in master_list:
            for y in x:
                new_span = abjad.AnnotatedTimespan(
                    start_offset=y.start_offset,
                    stop_offset=y.stop_offset,
                    annotation=y.annotation.voice_name,
                )
                showable_list.append(new_span)

        if split is True:
            split_timespans = [
                timespan_functions.make_split_list(x, bounds) for x in master_list
            ]
        else:
            split_timespans = [x for x in master_list]

        master_list = split_timespans

        master_length = len(master_list)
        if is_global is False:
            voices = [f"Voice {i + 1}" for i in range(master_length)]
        else:
            voices = ["Global Context"]
        final_timespan_dict = {
            voice: timespan_list for voice, timespan_list in zip(voices, master_list)
        }
        # if add_silence is True:
        #     silence_specifier = timespan_functions.TimespanSpecifier(
        #         handler=silence_maker
        #     )
        # else:
        #     silence_specifier = timespan_functions.TimespanSpecifier(
        #         handler=cyclic_materials(r=1)[0]
        #     )
        # timespan_functions.add_silences_to_timespan_dict(
        #     final_timespan_dict, silence_specifier
        # )
        if add_silence is True:
            silence_specifier = timespan_functions.TimespanSpecifier(
                handler=silence_maker
            )
            timespan_functions.add_silences_to_timespan_dict(
                final_timespan_dict, silence_specifier
            )

        directory = (current_directory).resolve()
        pdf_path = f"""{directory}/{segment_name}.pdf"""
        path = pathlib.Path(f"""{segment_name}.pdf""")
        if path.exists():
            print(f"Removing {pdf_path} ...")
            path.unlink()
        time_1 = time.time()
        print(f"Persisting {pdf_path} ...")
        result = abjad.persist(showable_list).as_pdf(
            pdf_path, scale=0.70, key="annotation", sort_callable=human_sorted_keys
        )
        print(result[0])
        print(result[1])
        print(result[2])
        success = result[3]
        if success is False:
            print("LilyPond failed!")
        time_2 = time.time()
        total_time = time_2 - time_1
        print(f"Total time: {total_time} seconds")
        if path.exists():
            print(f"Opening {pdf_path} ...")
            os.system(f"open {pdf_path}")

        return final_timespan_dict
