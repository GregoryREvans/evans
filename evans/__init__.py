"""
Evans API

The personal Abjad library of Gregory Rowland Evans.
"""
from .commands import (
    Command,
    HandlerCommand,
    RhythmCommand,
    attach,
    call,
    detach,
    duplicate,
    replace,
)
from .consort import (
    LogicalTieCollection,
    RatioPartsExpression,
    TimespanCollection,
    TimespanSimultaneity,
    iterate_nwise,
)
from .handlers import (
    ArticulationHandler,
    BendHandler,
    BisbigliandoHandler,
    BowAngleHandler,
    ClefHandler,
    CompositeHandler,
    DynamicHandler,
    GettatoHandler,
    GlissandoHandler,
    GraceHandler,
    IntermittentVoiceHandler,
    NoteheadHandler,
    OnBeatGraceHandler,
    PitchHandler,
    RhythmHandler,
    SlurHandler,
    TempoSpannerHandler,
    TextSpanHandler,
    TrillHandler,
)
from .metmod import (
    calculate_metric_modulation,
    calculate_tempo_modulated_duration,
    compare_speed,
    metric_modulation,
    mixed_number,
)
from .pitch import (
    JIPitch,
    combination_tones,
    herz_combination_tone_ratios,
    return_cent_markup,
    return_vertical_moment_ties,
    to_nearest_eighth_tone,
    to_nearest_quarter_tone,
    to_nearest_sixth_tone,
    to_nearest_third_tone,
    to_nearest_twelfth_tone,
    tonnetz,
    tune_to_ratio,
)
from .rtm import (
    RTMMaker,
    RhythmTreeQuantizer,
    funnel_inner_tree_to_x,
    funnel_tree_to_x,
    nested_list_to_rtm,
    rotate_tree,
)
from .segmentmaker import NoteheadBracketMaker, SegmentMaker, beam_meter
from .sequence import (
    CyclicList,
    MarkovChain,
    PitchClassSegment,
    PitchClassSet,
    PitchSegment,
    PitchSet,
    Ratio,
    RatioClassSegment,
    RatioClassSet,
    RatioSegment,
    RatioSet,
    Sequence,
    cyc,
    flatten,
    julia_set,
)
from .spanners import (
    BowAnglePoint,
    StringDampComponent,
    StringDampSequence,
    bow_angle_spanner,
)
from .timespan import (
    SilentTimespan,
    TimespanMaker,
    TimespanSpecifier,
    add_silences_to_timespan_dict,
    add_silences_to_timespan_lists,
    add_silent_timespans,
    collect_offsets,
    human_sorted_keys,
    intercalate_silences,
    make_showable_list,
    make_split_list,
    sorted_keys,
    talea_timespans,
    to_digit,
)

__all__ = [
    "ArticulationHandler",
    "BendHandler",
    "BisbigliandoHandler",
    "BowAngleHandler",
    "BowAnglePoint",
    "ClefHandler",
    "Command",
    "CompositeHandler",
    "CyclicList",
    "DynamicHandler",
    "GettatoHandler",
    "GlissandoHandler",
    "GraceHandler",
    "HandlerCommand",
    "IntermittentVoiceHandler",
    "JIPitch",
    "LogicalTieCollection",
    "MarkovChain",
    "NoteheadBracketMaker",
    "NoteheadHandler",
    "OnBeatGraceHandler",
    "PitchClassSegment",
    "PitchClassSet",
    "PitchHandler",
    "PitchSegment",
    "PitchSet",
    "RTMMaker",
    "Ratio",
    "RatioClassSegment",
    "RatioClassSet",
    "RatioPartsExpression",
    "RatioSegment",
    "RatioSet",
    "RhythmCommand",
    "RhythmHandler",
    "RhythmTreeQuantizer",
    "SegmentMaker",
    "Sequence",
    "SilentTimespan",
    "SlurHandler",
    "StringDampComponent",
    "StringDampSequence",
    "TempoSpannerHandler",
    "TextSpanHandler",
    "TimespanCollection",
    "TimespanMaker",
    "TimespanSimultaneity",
    "TimespanSpecifier",
    "TrillHandler",
    "add_silences_to_timespan_dict",
    "add_silences_to_timespan_lists",
    "add_silent_timespans",
    "attach",
    "beam_meter",
    "bow_angle_spanner",
    "calculate_metric_modulation",
    "calculate_tempo_modulated_duration",
    "call",
    "collect_offsets",
    "combination_multiples",
    "combination_tones",
    "compare_speed",
    "cyc",
    "detach",
    "duplicate",
    "flatten",
    "funnel_inner_tree_to_x",
    "funnel_tree_to_x",
    "herz_combination_tone_ratios",
    "human_sorted_keys",
    "intercalate_silences",
    "iterate_nwise",
    "julia_set",
    "make_showable_list",
    "make_split_list",
    "metric_modulation",
    "mixed_number",
    "nested_list_to_rtm",
    "relative_ratios",
    "replace",
    "return_cent_markup",
    "return_vertical_moment_ties",
    "rotate_tree",
    "sorted_keys",
    "talea_timespans",
    "to_digit",
    "to_nearest_eighth_tone",
    "to_nearest_quarter_tone",
    "to_nearest_sixth_tone",
    "to_nearest_third_tone",
    "to_nearest_twelfth_tone",
    "tonnetz",
    "tune_to_ratio",
]
