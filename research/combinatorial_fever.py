import itertools

import abjad
import evans


def add_subgroups(
    input_list=[1, 1, 1, 1],
    index_list=[0, 1, 2, 3],
    subgroup_list=[[1], [1, 1], [1, 1, 1], [1, 1, 1, 1]],
):
    new_list_from_input = [_ for _ in input_list]
    for index, group in zip(index_list, subgroup_list):
        new_list_from_input[index] = [new_list_from_input[index], list(group[:])]
    new_list_from_input = [1, new_list_from_input]
    return new_list_from_input


def make_tableaux_chart(fundamental_patterns, subdivisions):
    print("instantiating parser, staff group, and patterns ...")
    parser = abjad.rhythmtrees.RhythmTreeParser()
    print("beginning loop ...")
    for i, fundamental_pattern in enumerate(fundamental_patterns):
        print(fundamental_pattern)
        print("gathering pattern ...")
        print("permuting pattern ...")
        for permutation in list(
            set([_ for _ in itertools.permutations(fundamental_pattern)])
        ):
            permutation = list(permutation)
            print(permutation)
            title = fr"Mutations of {permutation}"
            final_patterns = []
            parsed_patterns = abjad.Staff(lilypond_type="RhythmicStaff")
            for num_indices in range(len(permutation) + 1):
                print("gathing number of possible dividable beats ...")
                if num_indices == 0:
                    print("do not subdivide!")
                    print("converting to string ...")
                    subgrouped_permutation = (
                        f"(1 {evans.nested_list_to_rtm(permutation)})"
                    )
                    print("gathing number of rotatable positions ...")
                    l_ = -1
                    for symbol in subgrouped_permutation:
                        if symbol.isdigit():
                            l_ = l_ + 1
                    for y in range(l_):
                        print("rotating ...")
                        rotation = evans.rotate_tree(
                            rtm_string=subgrouped_permutation, n=y
                        )
                        print(rotation)
                        print("funneling rotation to 1 ...")
                        for funnel in evans.funnel_inner_tree_to_x(
                            rtm_string=rotation, x=1
                        ):
                            print("caching funnel ...")
                            print(funnel)
                            final_patterns.append(funnel)
                else:
                    print("subdivide!")
                    print("gathering possible subdivisions ...")
                    for division_group in itertools.combinations_with_replacement(
                        subdivisions, num_indices
                    ):
                        division_group = list(division_group)
                        print("gathering possible subdivision locations ...")
                        possible_indices = [_ for _ in range(len(permutation))]
                        for index_group in itertools.combinations(
                            possible_indices, num_indices
                        ):
                            index_group = list(index_group)
                            print("adding subgroups ...")
                            subdivided_permutation = add_subgroups(
                                input_list=permutation,
                                index_list=index_group,
                                subgroup_list=division_group,
                            )
                            print("converting to string ...")
                            subgrouped_permutation = evans.nested_list_to_rtm(
                                subdivided_permutation
                            )
                            print(subgrouped_permutation)
                            print("gathing number of rotatable positions ...")
                            l_ = -1
                            for symbol in subgrouped_permutation:
                                if symbol.isdigit():
                                    l_ = l_ + 1
                            for y in range(l_):
                                print("rotating ...")
                                rotation = evans.rotate_tree(
                                    rtm_string=subgrouped_permutation, n=y
                                )
                                print(rotation)
                                print("funneling rotation to 1 ...")
                                for funnel in evans.funnel_inner_tree_to_x(
                                    rtm_string=rotation, x=1
                                ):
                                    print("caching funnel ...")
                                    print(funnel)
                                    final_patterns.append(funnel)
            print("parsing cached funnels ...")
            for pattern in final_patterns:
                print(pattern)
                pair = (1, 2)
                time_signature = abjad.TimeSignature(pair)
                rhythm_tree_list = parser(pattern)
                rhythm_tree_container = rhythm_tree_list[0]
                r = rhythm_tree_container(pair)
                m = abjad.Markup(fr"\markup {pattern}", direction=abjad.Up)
                abjad.attach(m, abjad.select(r).leaves()[0])
                abjad.attach(time_signature, abjad.select(r).leaves()[0])
                print("adding parsed funnel to staff ...")
                parsed_patterns.extend(r)
            print("adding staff to staff group ...")
            score = abjad.Score([parsed_patterns])
            scheme = abjad.SchemeMoment((1, 50))
            abjad.setting(score).proportional_notation_duration = scheme
            new_brackets = evans.NoteheadBracketMaker()
            for staff in abjad.select(score).components(abjad.Staff):
                new_brackets(staff)
            abjad.override(score).TupletBracket.bracket_visibility = True
            print("rendering staff group ...")
            file = abjad.LilyPondFile(
                items=[score, abjad.Block(name="layout"), abjad.Block(name="header")],
                includes=["/Users/evansdsg2/abjad/docs/source/_stylesheets/abjad.ily"],
                global_staff_size=14,
                default_paper_size=("11x17landscape", "portrait"),
            )
            file.layout_block.items.append("indent = 0")
            file.header_block.items.append("tagline = ##f")
            file.header_block.items.append(f'title = "{title}"')
            abjad.show(file)


fundamental_patterns = [
    [3, 3, 2],
]

subdivisions = [
    [3, 1],
    [1, 1],
]

make_tableaux_chart(fundamental_patterns, subdivisions)


fundamental_patterns = [
    [
        3,
        1,
        2,
        2,
    ],
]

subdivisions = [
    [2, 1],
    [1, 3],
]

make_tableaux_chart(fundamental_patterns, subdivisions)


# fundamental_patterns = [
#     [3, 3, 2],
#     [1, 2, 1, 1, 1, 2],
# ]

# subdivisions = [
#     [1, 1, 1, 1],
#     [1, 1, 1, -1],
#     [1, 1, -1, 1],
#     [1, -1, 1, 1],
#     [-1, 1, 1, 1],
#     [1, 1, -2],
#     [1, -2, 1],
#     [-2, 1, 1],
#     [3, 1],
#     [1, -3],
#     [-3, 1],
#     [-1, 3],
#     [3, -1],
#     [1, 1, 1],
#     [1, 1, -1],
#     [1, -1, 1],
#     [-1, 1, 1],
#     [1, -2],
#     [-2, 1],
#     [1, 1],
#     [1, -1],
#     [-1, 1],
# ]
