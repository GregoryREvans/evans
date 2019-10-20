import abjad
import evans
import pathlib
import abjadext.rmakers as rmakers
from tsmakers.TaleaTimespanMaker import TaleaTimespanMaker
from hamon_shu.Materials.rhythm.Segment_I.rhythm_handlers import *
from hamon_shu.Materials.score_structure.instruments import instruments
from collections import OrderedDict
from hamon_shu.Materials.score_structure.Segment_I.rhythm_material_pattern import (
    rhythm_material_list,
)
from hamon_shu.Materials.score_structure.Segment_I.pitch_material_pattern import (
    pitch_material_list,
)
from hamon_shu.Materials.score_structure.Segment_I.dynamic_material_pattern import (
    dynamic_material_list,
)
from hamon_shu.Materials.score_structure.Segment_I.articulation_material_pattern import (
    articulation_material_list,
)
from hamon_shu.Materials.score_structure.Segment_I.time_signatures import bounds

# padovan_1 = evans.e_dovan_cycle(n=3, iters=85, first=3, second=5, modulus=5)
# padovan_2 = evans.e_dovan_cycle(n=2, iters=85, first=2, second=3, modulus=5)
# padovan_3 = evans.e_dovan_cycle(n=2, iters=85, first=1, second=1, modulus=4)

pitch_padovan_1 = evans.e_dovan_cycle(n=3, iters=5, first=3, second=5, modulus=5)

music_specifiers = OrderedDict(
    [(f"Voice {i+1}", None) for i, name in enumerate(instruments)]
)
#
# ########
# # rhythm#
# ########
# rhythm_target_timespan = abjad.Timespan(0, 22)
# # 1, 3, 2
# rhythm_timespan_maker = TaleaTimespanMaker(
#     initial_silence_talea=rmakers.Talea(counts=([0, 3, 2, 0]), denominator=8),
#     # synchronize_step=True, #goes down voices instead of across? maybe not consistent...
#     # synchronize_groupings=True, #goes down voices instead of across? maybe not consistent...
#     playing_talea=rmakers.Talea(counts=(padovan_1), denominator=4),
#     playing_groupings=(
#         padovan_3
#     ),  # smashes timespans together without intermittent silence
#     silence_talea=rmakers.Talea(counts=(padovan_2), denominator=4),
#     # fuse_groups=False, #turns groups from multiple timespans into one large timespan
# )
#
# rhythm_timespan_list = rhythm_timespan_maker(
#     music_specifiers=music_specifiers, target_timespan=rhythm_target_timespan
# )

#######
# pitch#
#######
pitch_target_timespan = abjad.Timespan(0, 22)

pitch_timespan_maker = TaleaTimespanMaker(
    # initial_silence_talea=rmakers.Talea(counts=([0, 5, 3, 6, 2]), denominator=8),
    # synchronize_step=True, #goes down voices instead of across? maybe not consistent...
    # synchronize_groupings=True, #goes down voices instead of across? maybe not consistent...
    playing_talea=rmakers.Talea(counts=(pitch_padovan_1), denominator=2),
    # playing_groupings=(
    #     [1, 2, 3, 2]
    # ),  # smashes timespans together without intermittent silence
    silence_talea=rmakers.Talea(counts=([0]), denominator=4),
    # fuse_groups=False, #turns groups from multiple timespans into one large timespan
)

pitch_timespan_list = pitch_timespan_maker(
    music_specifiers=music_specifiers, target_timespan=pitch_target_timespan
)

# #########
# # dynamic#
# #########
# dynamic_target_timespan = abjad.Timespan(0, 27)
#
# dynamic_timespan_maker = TaleaTimespanMaker(
#     # initial_silence_talea=rmakers.Talea(counts=([0, 5, 3, 6, 2]), denominator=8),
#     # synchronize_step=True, #goes down voices instead of across? maybe not consistent...
#     # synchronize_groupings=True, #goes down voices instead of across? maybe not consistent...
#     playing_talea=rmakers.Talea(counts=(padovan_2), denominator=2),
#     # playing_groupings=(
#     #     [1, 2, 3, 2]
#     # ),  # smashes timespans together without intermittent silence
#     silence_talea=rmakers.Talea(counts=([0]), denominator=4),
#     # fuse_groups=False, #turns groups from multiple timespans into one large timespan
# )
#
# dynamic_timespan_list = dynamic_timespan_maker(
#     music_specifiers=music_specifiers, target_timespan=dynamic_target_timespan
# )

# ##############
# # articulation#
# ##############
# articulation_target_timespan = abjad.Timespan(0, 27)
#
# articulation_timespan_maker = TaleaTimespanMaker(
#     # initial_silence_talea=rmakers.Talea(counts=([0, 5, 3, 6, 2]), denominator=8),
#     # synchronize_step=True, #goes down voices instead of across? maybe not consistent...
#     # synchronize_groupings=True, #goes down voices instead of across? maybe not consistent...
#     playing_talea=rmakers.Talea(counts=(padovan_3), denominator=2),
#     # playing_groupings=(
#     #     [1, 2, 3, 2]
#     # ),  # smashes timespans together without intermittent silence
#     silence_talea=rmakers.Talea(counts=([0]), denominator=4),
#     # fuse_groups=False, #turns groups from multiple timespans into one large timespan
# )
#
# articulation_timespan_list = dynamic_timespan_maker(
#     music_specifiers=music_specifiers, target_timespan=articulation_target_timespan
# )


#
# ########
# # rhythm#
# ########
# rhythm_mat = rhythm_material_list
#
# segment_I_rhythm_timespans = evans.ConvertTimespans.convert_timespans(
#     materials=rhythm_mat,
#     ts_list=rhythm_timespan_list,
#     bounds=bounds,
#     segment_name="Segment_I_rhythm_timespans",
#     current_directory=pathlib.Path(__file__).parent,
#     add_silence=True,
# )

#######
# pitch#
#######
pitch_mat = pitch_material_list

segment_I_pitch_timespans = evans.ConvertTimespans.convert_timespans(
    materials=pitch_mat,
    ts_list=pitch_timespan_list,
    bounds=bounds,
    segment_name="Segment_I_pitch_timespans",
    current_directory=pathlib.Path(__file__).parent,
    add_silence=False,
)
#
# #########
# # dynamic#
# #########
# dynamic_mat = dynamic_material_list
#
# segment_I_dynamic_timespans = evans.ConvertTimespans.convert_timespans(
#     materials=dynamic_mat,
#     ts_list=dynamic_timespan_list,
#     bounds=bounds,
#     segment_name="Segment_I_dynamic_timespans",
#     current_directory=pathlib.Path(__file__).parent,
#     add_silence=False,
# )
#
# ##############
# # articulation#
# ##############
# articulation_mat = articulation_material_list
#
# segment_I_articulation_timespans = evans.ConvertTimespans.convert_timespans(
#     materials=articulation_mat,
#     ts_list=articulation_timespan_list,
#     bounds=bounds,
#     segment_name="Segment_I_articulation_timespans",
#     current_directory=pathlib.Path(__file__).parent,
#     add_silence=False,
# )
