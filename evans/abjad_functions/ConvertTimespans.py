import time
from collections import defaultdict

import abjad
import abjadext.rmakers
from evans.AttachmentHandlers.CyclicList import CyclicList
from evans.AttachmentHandlers.RhythmHandler import RhythmHandler
from evans.abjad_functions import timespan_functions
from evans.abjad_functions.timespan_human_keys import human_sorted_keys
from evans.general_tools.sorted_keys import sorted_keys
from tsmakers.PerformedTimespan import PerformedTimespan

silence_maker_ = abjadext.rmakers.stack(
    abjadext.rmakers.NoteRhythmMaker(),
    abjadext.rmakers.force_rest(abjad.select().leaves(pitched=True)),
)

silence_maker = RhythmHandler(rmaker=silence_maker_, name="silence maker")


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

    @staticmethod
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
        time_1 = time.time()

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
                            voice_name="Global Context",
                            handler=cyclic_materials(r=1)[0],
                        )
                        ts_list.append(timespan)
                elif isinstance(timespan, PerformedTimespan):
                    if is_global is False:
                        timespan = abjad.AnnotatedTimespan(
                            start_offset=timespan.start_offset,
                            stop_offset=timespan.stop_offset,
                            annotation=timespan_functions.TimespanSpecifier(
                                voice_name=f"Voice {i}",
                                handler=cyclic_materials(r=1)[0],
                            ),
                        )
                        ts_list.append(timespan)
                    else:
                        timespan = abjad.AnnotatedTimespan(
                            start_offset=timespan.start_offset,
                            stop_offset=timespan.stop_offset,
                            annotation=timespan_functions.TimespanSpecifier(
                                voice_name="Global Context",
                                handler=cyclic_materials(r=1)[0],
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
        pdf_path = abjad.Path(f"""{directory}/{segment_name}.pdf""")
        if pdf_path.exists():
            print(f"Removing {pdf_path.trim()} ...")
            pdf_path.unlink()
        print(f"Persisting {pdf_path.trim()} ...")
        result = abjad.persist(showable_list).as_pdf(
            pdf_path, scale=0.70, key="annotation", sort_callable=human_sorted_keys
        )
        print(result[0])
        print(round(result[1]))
        print(round(result[2]))
        success = result[3]
        if success is False:
            print("LilyPond failed!")
        time_2 = time.time()
        total_time = round(time_2 - time_1)
        unit = abjad.String("second").pluralize(total_time)
        print(f"Total time: {total_time} {unit}")
        if pdf_path.exists():
            print(f"Opening {pdf_path.trim()} ...")

        return final_timespan_dict
