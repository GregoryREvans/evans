"""
Evans API

The personal Abjad library of Gregory Rowland Evans.
"""
from . import baca_rhythm
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
    auto_staff_change,
    bcp,
    call,
    cross_staff,
    cross_staff_copy,
    detach,
    duplicate,
    even_division,
    figure,
    fitted_obgc,
    hairpin,
    imbricate,
    long_beam,
    make_anchor_skips_from_voices,
    make_rtm,
    make_tied_notes,
    music,
    note,
    replace,
    replace_rests_with_skips,
    simple_hairpin,
    slur,
    subdivided_ties,
    sustain_pedal,
    talea,
    text_span,
    text_spanner,
    trill,
    tuplet,
    unsicthbare_farben,
    vibrato_spanner,
    wrap_in_repeats,
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
    Lapidary,
    annotate_concurrent_ratios,
    annotate_hertz,
    clean_cent_markup,
    combination_tones,
    contour,
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
from .quantizer import fuse_durations, subdivide_durations, unity_capsule_rhythms
from .rtm import (
    AfterGraceContainer,
    BeforeGraceContainer,
    RTMMaker,
    RTMNode,
    RTMTree,
    RhythmTreeQuantizer,
    after_grace_container,
    before_grace_container,
    exponential_leaf_maker,
    flatten_tree_level,
    funnel_inner_tree_to_x,
    funnel_tree_to_x,
    helianthated_rtm,
    make_exponential_leaves,
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
    select_ties_below_written_pitch,
    select_ties_final_leaves,
    select_untupleted_leaves,
)
from .sequence import (
    CompoundMelody,
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
    combine_ts_lists,
    cyc,
    flatten,
    intersect_time_signature_lists,
    julia_set,
    make_time_signatures_from_ts_list,
)
from .spanners import (
    BendBefore,
    DurationLine,
    Lyrics,
    annotate_tuplet_duration,
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
    "AfterGraceContainer",
    "ArticulationHandler",
    "ArtificialHarmonic",
    "Attachment",
    "BeforeGraceContainer",
    "BendBefore",
    "BendHandler",
    "BisbigliandoHandler",
    "BowAngleHandler",
    "Breaks",
    "Callable",
    "ClefHandler",
    "Command",
    "CompositeHandler",
    "CompoundMelody",
    "CyclicList",
    "DurationLine",
    "DynamicHandler",
    "ETPitch",
    "GettatoHandler",
    "GlissandoHandler",
    "GraceHandler",
    "HandlerCommand",
    "IntermittentVoiceHandler",
    "JIPitch",
    "Lapidary",
    "LogicalTieCollection",
    "Lyrics",
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
    "RTMNode",
    "RTMTree",
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
    "after_grace_container",
    "annotate_concurrent_ratios",
    "annotate_hertz",
    "annotate_leaves",
    "annotate_time",
    "annotate_tuplet_duration",
    "attach",
    "auto_staff_change",
    "bcp",
    "beam_meter",
    "beautify_tuplets",
    "before_grace_container",
    "calculate_metric_modulation",
    "calculate_tempo_modulated_duration",
    "call",
    "clean_cent_markup",
    "collect_offsets",
    "combination_tones",
    "combine_ts_lists",
    "compare_speed",
    "contour",
    "cross_staff",
    "cross_staff_copy",
    "cyc",
    "detach",
    "duplicate",
    "even_division",
    "exponential_leaf_maker",
    "extract_class_name",
    "figure",
    "fitted_obgc",
    "flatten",
    "flatten_tree_level",
    "force_accidentals",
    "funnel_inner_tree_to_x",
    "funnel_tree_to_x",
    "fuse_durations",
    "get_top_level_components_from_leaves",
    "global_to_voice",
    "hairpin",
    "hairpin",
    "helianthated_rtm",
    "herz_combination_tone_ratios",
    "human_sorted_keys",
    "imbricate",
    "intercalate_silences",
    "intersect_time_signature_lists",
    "iterate_nwise",
    "iterate_vertical_moments_by_logical_tie",
    "join_time_signature_lists",
    "julia_set",
    "long_beam",
    "loop",
    "make_anchor_skips_from_voices",
    "make_exponential_leaves",
    "make_fancy_gliss",
    "make_multi_trill",
    "make_preprocessor",
    "make_rtm",
    "make_sc_file",
    "make_score_template",
    "make_showable_list",
    "make_split_list",
    "make_tied_notes",
    "make_time_signatures_from_ts_list",
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
    "replace_rests_with_skips",
    "return_cent_markup",
    "return_vertical_moment_ties",
    "rotate_tree",
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
    "select_ties_below_written_pitch",
    "select_ties_final_leaves",
    "select_untupleted_leaves",
    "simple_hairpin",
    "slur",
    "sort_voices",
    "sorted_keys",
    "subdivide_durations",
    "subdivided_ties",
    "sustain_pedal",
    "talea",
    "talea_timespans",
    "text_span",
    "text_spanner",
    "to_digit",
    "to_nearest_eighth_tone",
    "to_nearest_quarter_tone",
    "to_nearest_sixth_tone",
    "to_nearest_third_tone",
    "to_nearest_twelfth_tone",
    "tonnetz",
    "trill",
    "tune_to_ratio",
    "tuplet",
    "unity_capsule_rhythms",
    "unsicthbare_farben",
    "vibrato_spanner",
    "wrap_in_repeats",
]
