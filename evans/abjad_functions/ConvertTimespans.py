import abjad
import abjadext.rmakers
import os
import pathlib
import time
from tsmakers.PerformedTimespan import PerformedTimespan
from evans.AttachmentHandlers.CyclicList import CyclicList
from evans.abjad_functions.talea_timespan import timespan_functions
from collections import defaultdict
from evans.general_tools.sorted_keys import sorted_keys
from evans.abjad_functions.timespan_human_keys import human_sorted_keys

silence_maker = abjadext.rmakers.NoteRhythmMaker(
    division_masks=[abjadext.rmakers.SilenceMask(pattern=abjad.index([0], 1))]
)


class ConvertTimespans:
    def __init__(self, materials, ts_list, bounds, persist=False):
        self.materials = materials
        self.ts_list = ts_list
        self.bounds = bounds
        self.persist = persist

    def __call__(self):
        self.convert_timespans(self.materials, self.ts_list, self.bounds)

    def convert_timespans(materials, ts_list, bounds):

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
                    timespan.annotation = timespan_functions.TimespanSpecifier(
                        voice_name=f"Voice {i}", handler=cyclic_materials(r=1)[0]
                    )
                    ts_list.append(timespan)
                elif isinstance(timespan, PerformedTimespan):
                    timespan = abjad.AnnotatedTimespan(
                        start_offset=timespan.start_offset,
                        stop_offset=timespan.stop_offset,
                        annotation=timespan_functions.TimespanSpecifier(
                            voice_name=f"Voice {i}", handler=cyclic_materials(r=1)[0]
                        ),
                    )
                    ts_list.append(timespan)
                else:
                    timespan.annotation = timespan_functions.TimespanSpecifier(
                        voice_name=f"Voice {i}", handler=silence_maker
                    )
                    ts_list.append(timespan)
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

        split_timespans = [
            timespan_functions.make_split_list(x, bounds) for x in master_list
        ]

        master_list = split_timespans

        master_length = len(master_list)
        voices = [f"Voice {i + 1}" for i in range(master_length)]
        rhythm_timespans = {
            voice: timespan_list for voice, timespan_list in zip(voices, master_list)
        }
        silence_specifier = timespan_functions.TimespanSpecifier(handler=silence_maker)
        timespan_functions.add_silences_to_timespan_dict(
            rhythm_timespans, silence_specifier
        )
        return rhythm_timespans

        # persist timespan_list
        if self.persist is True:
            current_directory = pathlib.Path(__file__).parent
            directory = (
                current_directory / ".." / ".." / ".." / "Segments/Segment_I"
            ).resolve()
            pdf_path = f"{directory}/Segment_I_rhythm_timespans.pdf"
            path = pathlib.Path("Segment_I_rhythm_timespans.pdf")
            if path.exists():
                print(f"Removing {pdf_path} ...")
                path.unlink()
            time_1 = time.time()
            print(f"Persisting {pdf_path} ...")
            result = abjad.persist(showable_list).as_pdf(
                pdf_path, scale=0.5, key="annotation", sort_callable=human_sorted_keys
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
        else:
            pass
