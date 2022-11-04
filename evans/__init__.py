"""
Evans API

The personal Abjad library of Gregory Rowland Evans.
"""
from .commands import (
    Attachment,
    Callable,
    Command,
    HandlerCommand,
    MusicCommand,
    RewriteMeterCommand,
    RhythmCommand,
    Skeleton,
    accelerando,
    attach,
    bcp,
    call,
    detach,
    duplicate,
    even_division,
    hairpin,
    make_rtm,
    make_tied_notes,
    music,
    note,
    replace,
    slur,
    talea,
    text_span,
    text_spanner,
    trill,
    tuplet,
    vibrato_spanner,
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
    ScordaturaHandler,
    SlurHandler,
    TempoSpannerHandler,
    TextSpanHandler,
    TranspositionHandler,
    TrillHandler,
)
from .layout import (
    Breaks,
    Page,
    System,
    join_time_signature_lists,
    reduce_fermata_measures,
)
from .metmod import (
    calculate_metric_modulation,
    calculate_tempo_modulated_duration,
    compare_speed,
    metric_modulation,
    mixed_number,
)
from .pitch import (
    ArtificialHarmonic,
    ETPitch,
    JIPitch,
    annotate_concurrent_ratios,
    annotate_hertz,
    clean_cent_markup,
    combination_tones,
    force_accidentals,
    herz_combination_tone_ratios,
    loop,
    reduce_list_by_prime_limit,
    reduce_list_to_contain_sole_prime,
    reduced_spectrum,
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
from .preprocess import make_preprocessor
from .rtm import (
    RTMMaker,
    RhythmTreeQuantizer,
    flatten_tree_level,
    funnel_inner_tree_to_x,
    funnel_tree_to_x,
    helianthated_rtm,
    nested_list_to_rtm,
    rotate_tree,
)
from .segmentmaker import (
    NoteheadBracketMaker,
    SegmentMaker,
    annotate_leaves,
    annotate_time,
    beam_meter,
    beautify_tuplets,
    extract_class_name,
    get_top_level_components_from_leaves,
    global_to_voice,
    make_sc_file,
    make_score_template,
    sort_voices,
)
from .select import (
    select_all_but_final_leaf,
    select_all_first_leaves,
    select_alternate_divisions_final_leaves,
    select_alternate_leaves,
    select_divisions_final_leaves,
    select_measures,
    select_outer_ties,
    select_periodic_ties,
    select_periodic_tuplets,
    select_runs_first_leaves,
    select_ties_final_leaves,
    select_untupleted_leaves,
)
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
    BendBefore,
    DurationLine,
    Lyrics,
    make_fancy_gliss,
    make_multi_trill,
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
from .verticalmoment import VerticalMoment, iterate_vertical_moments_by_logical_tie

__all__ = [
    "ArtificialHarmonic",
    "Attachment",
    "BendBefore",
    "BendHandler",
    "BisbigliandoHandler",
    "BowAngleHandler",
    "Breaks",
    "Callable",
    "ClefHandler",
    "Command",
    "CompositeHandler",
    "CyclicList",
    "DurationLine",
    "bcp",
    "hairpin",
    "DynamicHandler",
    "ETPitch",
    "GettatoHandler",
    "GlissandoHandler",
    "GraceHandler",
    "HandlerCommand",
    "IntermittentVoiceHandler",
    "JIPitch",
    "LogicalTieCollection",
    "Lyrics",
    "trill",
    "vibrato_spanner",
    "text_span",
    "MarkovChain",
    "MusicCommand",
    "NoteheadBracketMaker",
    "NoteheadHandler",
    "OnBeatGraceHandler",
    "Page",
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
    "RewriteMeterCommand",
    "RhythmCommand",
    "RhythmHandler",
    "RhythmTreeQuantizer",
    "ScordaturaHandler",
    "SegmentMaker",
    "Sequence",
    "SilentTimespan",
    "Skeleton",
    "SlurHandler",
    "System",
    "TempoSpannerHandler",
    "TextSpanHandler",
    "TimespanCollection",
    "TimespanMaker",
    "TimespanSimultaneity",
    "TimespanSpecifier",
    "TranspositionHandler",
    "TrillHandler",
    "VerticalMoment",
    "accelerando",
    "add_silences_to_timespan_dict",
    "add_silences_to_timespan_lists",
    "add_silent_timespans",
    "annotate_concurrent_ratios",
    "annotate_leaves",
    "annotate_time",
    "annotate_hertz",
    "attach",
    "beam_meter",
    "beautify_tuplets",
    "calculate_metric_modulation",
    "calculate_tempo_modulated_duration",
    "call",
    "clean_cent_markup",
    "collect_offsets",
    "combination_tones",
    "compare_speed",
    "cyc",
    "detach",
    "duplicate",
    "even_division",
    "extract_class_name",
    "flatten",
    "flatten_tree_level",
    "force_accidentals",
    "funnel_inner_tree_to_x",
    "funnel_tree_to_x",
    "get_top_level_components_from_leaves",
    "global_to_voice",
    "hairpin",
    "helianthated_rtm",
    "herz_combination_tone_ratios",
    "human_sorted_keys",
    "intercalate_silences",
    "iterate_nwise",
    "iterate_vertical_moments_by_logical_tie",
    "join_time_signature_lists",
    "julia_set",
    "loop",
    "make_fancy_gliss",
    "make_multi_trill",
    "make_preprocessor",
    "make_rtm",
    "make_sc_file",
    "make_score_template",
    "make_showable_list",
    "make_split_list",
    "make_tied_notes",
    "metric_modulation",
    "mixed_number",
    "music",
    "nested_list_to_rtm",
    "note",
    "reduce_fermata_measures",
    "reduce_list_by_prime_limit",
    "reduce_list_to_contain_sole_prime",
    "reduced_spectrum",
    "relative_ratios",
    "replace",
    "return_cent_markup",
    "return_vertical_moment_ties",
    "rotate_tree",
    "slur",
    "select_all_but_final_leaf",
    "select_all_first_leaves",
    "select_alternate_divisions_final_leaves",
    "select_alternate_leaves",
    "select_divisions_final_leaves",
    "select_measures",
    "select_outer_ties",
    "select_periodic_ties",
    "select_periodic_tuplets",
    "select_runs_first_leaves",
    "select_ties_final_leaves",
    "select_untupleted_leaves",
    "sort_voices",
    "sorted_keys",
    "talea",
    "talea_timespans",
    "text_spanner",
    "to_digit",
    "to_nearest_eighth_tone",
    "to_nearest_quarter_tone",
    "to_nearest_sixth_tone",
    "to_nearest_third_tone",
    "to_nearest_twelfth_tone",
    "tonnetz",
    "tune_to_ratio",
    "tuplet",
    "ArticulationHandler",
]
