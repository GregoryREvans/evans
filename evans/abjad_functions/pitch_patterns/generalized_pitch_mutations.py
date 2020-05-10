import abjad


def adjacent_combinations(l=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], count=2):
    combination_list = []
    for i, _ in enumerate(l):
        start = i
        stop = i + count
        group = l[start:stop]
        if len(group) == count:
            combination_list.append(group)
    return combination_list


for n in range(2, 13):
    score = abjad.Score([])
    for combination_group in adjacent_combinations(
        l=[0, 5, 7, 1, 4, 11, 3, 2, 10, 8, 9, 6], count=n
    ):
        staff_group1 = abjad.StaffGroup([])
        for rotation in range(len(combination_group)):
            staff_group2 = abjad.StaffGroup([])
            p = abjad.PitchClassSegment(combination_group).rotate(
                n=0 - rotation, stravinsky=False
            )
            i = p.invert()
            p_values = [item.number for item in p.items]
            i_values = [item.number for item in i.items]
            p_list = [p.transpose(_) for _ in i_values]
            p_staff = abjad.Staff()
            i_list = [i.transpose(_) for _ in p_values]
            i_staff = abjad.Staff()
            r_list = [_.retrograde() for _ in p_list]
            r_staff = abjad.Staff()
            ri_list = [_.retrograde() for _ in i_list]
            ri_staff = abjad.Staff()
            for _ in p_list:
                numbers = [n.number for n in _]
                l = []
                for note in numbers:
                    leaf = abjad.Note()
                    leaf.written_pitch = note
                    l.append(leaf)
                p_staff.extend(l)
            for _ in i_list:
                numbers = [n.number for n in _]
                l = []
                for note in numbers:
                    leaf = abjad.Note()
                    leaf.written_pitch = note
                    l.append(leaf)
                i_staff.extend(l)
            for _ in r_list:
                numbers = [n.number for n in _]
                l = []
                for note in numbers:
                    leaf = abjad.Note()
                    leaf.written_pitch = note
                    l.append(leaf)
                r_staff.extend(l)
            for _ in ri_list:
                numbers = [n.number for n in _]
                l = []
                for note in numbers:
                    leaf = abjad.Note()
                    leaf.written_pitch = note
                    l.append(leaf)
                ri_staff.extend(l)
            staff_group2.append(p_staff)
            staff_group2.append(i_staff)
            staff_group2.append(r_staff)
            staff_group2.append(ri_staff)
            staff_group1.append(staff_group2)
        score.append(staff_group1)
    sig = abjad.TimeSignature((n, 4))
    first_leaf = abjad.select(score).leaves()[0]
    abjad.attach(sig, first_leaf)
    abjad.persist(score).as_ly(
        f"/Users/evansdsg2/evans/evans/abjad_functions/pitch_patterns/divisions_of_{n}.ly"
    )
