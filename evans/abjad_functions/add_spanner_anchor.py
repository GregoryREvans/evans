import abjad


def _calc_anchor(leaf, anchor_dur=None, anchor_leaf=None):
    if anchor_leaf is not None:
        anchor_dur = anchor_leaf.written_duration
        durs = [leaf.written_duration]
    else:
        durs = [leaf.written_duration, anchor_dur]
    container = abjad.Container()
    pre_mult = leaf.written_duration - anchor_dur
    mult = pre_mult / leaf.written_duration
    if isinstance(leaf, abjad.Chord):
        pitches = [abjad.NamedPitch(_) for _ in abjad.inspect(leaf).pitches()]
    elif isinstance(leaf, abjad.Note):
        pitches = [abjad.NamedPitch(_) for _ in abjad.inspect(leaf).pitches()]
        pitches = pitches[0]
    else:
        pass
    maker = abjad.LeafMaker()
    new_leaves = [l for l in maker([pitches], durs)]
    new_leaf = new_leaves[0]
    indicators = abjad.inspect(leaf).indicators()
    for indicator in indicators:
        abjad.attach(indicator, new_leaf)
    new_leaf.multiplier = mult
    leaf.multiplier = mult
    if anchor_leaf is not None:
        anchor = anchor_leaf
        l = [_ for _ in abjad.inspect(leaf).pitches()]
        anchor.written_pitch = l[0]
    else:
        anchor = new_leaves[1]
    abjad.attach(abjad.LilyPondLiteral(r"""\abjad-invisible-music""", format_slot="before"), anchor)
    abjad.annotate(anchor, "type", "spanner anchor")
    container.append(new_leaf)
    container.append(anchor)
    return container

def _add_anchor(leaf, anchor_dur=None, anchor_leaf=None):
    abjad.mutate(leaf).replace(_calc_anchor(leaf, anchor_dur, anchor_leaf))

def add_spanner_anchor(leaf, anchor_dur=None, anchor_leaf=None):
    if abjad.inspect(leaf).leaf(1) is not None:
        next_leaf = abjad.inspect(leaf).leaf(1)
        if abjad.inspect(next_leaf).annotation("type") != "spanner anchor":
            _add_anchor(leaf, anchor_dur, anchor_leaf)
        else:
            pass
    else:
        _add_anchor(leaf, anchor_dur, anchor_leaf)

# #DEMO 1#
# staff = abjad.Staff("cs'4")
# add_spanner_anchor(leaf=staff[0], anchor_dur=abjad.Duration(1, 16))
# add_spanner_anchor(leaf=staff[0], anchor_dur=abjad.Duration(1, 16))
# abjad.f(staff)
#
# #DEMO 2#
# staff = abjad.Staff("cs'4")
# a_leaf = abjad.Note("c'16")
# add_spanner_anchor(leaf=staff[0], anchor_leaf=a_leaf)
# abjad.f(staff)
#
#DEMO 3#
staff = abjad.Staff("c'4 c'4 c'4 r4 c'4 c'4 r8 c'8 c'4 r1")
selections = abjad.select(staff[:])
for run in abjad.select(selections).runs():
    print("RUN")
    print(run)
    ties = abjad.select(run).logical_ties()
    print("FINAL LEAF PARENTAGE")
    print(abjad.inspect(ties[-1][-1]).parentage())
    print("FOLLOWING LEAF")
    print(abjad.inspect(ties[-1][-1]).leaf(1))
    add_spanner_anchor(leaf=ties[-1][-1], anchor_dur=abjad.Duration(1, 16))

for run in abjad.select(selections).runs():
    print("POST ANCHOR RUN")
    print(run)
    # print("POST ANCHOR TIES")
    # predicate = abjad.inspect().annotation("type")
    # ties = abjad.select(run).logical_ties().filter(predicate)
    # print(ties)
    print("POST ANCHOR FOLLOWING LEAF")
    print(abjad.inspect(ties[-1][-1]).leaf(1))
    print("POST ANCHOR FINAL LEAF PARENTAGE")
    print(abjad.inspect(ties[-1][-1]).parentage())
    print("")

abjad.f(staff)

for run in abjad.select(staff).runs():
    print(run)

#ADDING SPANNER ANCHOR REMOVES LEAVES FROM SELECTION AND DOES NOT REPLACE
#FIND A WAY TO RESELECT?
