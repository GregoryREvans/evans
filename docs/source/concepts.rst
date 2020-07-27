Core concepts
=============

Perllan and trees.
------------------

`Perllan` is a welsh word for "orchard."
When object modelling music notation, it becomes clear that most models take the graph form of a tree.
The ``Perllan`` network of ``Python`` packages which wrap ``Abjad`` represents a location and a set of tools designed for the purpose of cultivating these trees.

An analysis of a score tree can help in understanding the implications of parameter parentage. Traditional Western music notation is rooted firmly in Medieval formal architectures. Pitch notation is resolutely diatonic, non-power-of-two-denominator durations can only be represented with the assistance of a prolating tuplet bracket or time signature, and duration chains of prime-number-numerator durations greater than 3 can only be notated via tie-chained notes.

A parent score can hold children as staves or staff-groups, staves hold children as voices. Staff groups may hold staves as well. A staff may hold one or more voices, but a voice, while not distinctly notated with unique symbols, is always implied. A voice may hold children as tuplet-prolated containers or (explicit or implied) tie-chained duration events. Tuplet-prolated containers may also hold tie-chained events. ``Abjad`` refers to these tie-chained events as `Logical Ties`. Logical ties may hold children as single-symbol (prime-number-numerator durations less than 3) leaves. While a pitch value persists through the duration of a logical tie, the notation of pitch is represented through the positioning of the note head of a leaf and when applicable, the affixing of an accidental symbol preceding the initial leaf of a logical tie. Since the positioning of note heads is required on a leaf-by-leaf basis within a logical tie, it can be implied that within the tree-structure of a musical score, the pitch value of a given note is not at the same depth as the duration value, rather pitch is a child of duration or at least a subordinate sibling. Another form of parentage increases the child-like nature of the pitch parameter. In abjad, leaves are object-modelled with an abstract base class ``abjad.Leaf()`` which has duration but no pitch. The classes which inherit from leaf are ``abjad.Skip()``, ``abjad.Rest()``, and ``abjad.Note()``. ``Note`` is the only class which carries a pitch attribute. Since the child class has an attribute which the parent class does not have, this attribute is a child of the parent class.

There are several ramifications of this structure:

-   A voice (explicit or implied) is always present as the lowest level of context containers, even in abstract manipulations of structures like pitch and duration.

-   Regardless of when it is conceived by the composer, the tree of a score must be populated in a top-down fashion, gradually filling each parent with its children. Therefore, logical tie and leaf values must exist before pitch values can be affixed within a score.

``Perllan`` interfaces to pitch transforms require a selection of logical ties in order to apply pitch values. Not only is this consistent with the parentage model described above, the decoupling of parameters allows for a greater number of transformational possibilities, including those which would be possible if pitch and rhythm were not decoupled.

Pitch rounding.
---------------

The pitch utilities in ``abjad-ext-microtones`` do not coerce number rounding.
The ``et`` package only models scales of `eighth`, `tenth`, and `twelfth` divisions of the octave.
The ``ji`` package only models `23-limit` interval ratios.
It is the composer's responsibility to round pitch numbers before deployment.

Personal libraries.
-------------------
Personal libraries such as ``evans`` can provide users with useful programming solutions, while holding a slightly less officially published quality.
