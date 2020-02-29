import abjad
import evans


# map = [
#     evans.e_dovan_cycle(n=3, iters=85, first=3, second=5, modulus=5),
#     evans.e_dovan_cycle(n=2, iters=85, first=2, second=3, modulus=5),
#     evans.e_dovan_cycle(n=2, iters=85, first=1, second=1, modulus=4),
# ]
#
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.4],projection='3d')
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x where n=3, first=3, and second=5 at modulus 5')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y where n=2, first=2, and second=3 at modulu 5')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[2]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_title('values of z where n=2, first=1, and second=1 at modulus 4')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0][:80], map[1][:80], map[2][:80], color='black',lw=1,label='Evolution(t)')
# ax4.set_title('three simultneous padovan cycles up to 80 iterations')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# fig.savefig('e_dovan_cycles.png')
#####
#####
#####
#####
#####
# chord_1 = [-24, -20, -15, -14, -4, 5, 11, 19, 26, 37, 39, 42]
# chord_2 = [-24, -16, -9, 2, 4, 7, 13, 17, 22, 23, 33, 42]
# chord_3 = [-24, -21, -19, -8, -1, 7, 13, 22, 32, 33, 38, 42]
#
# chord_1 = evans.reproportion_chord(base=1, chord=chord_1, round=True)
# chord_2 = evans.reproportion_chord(base=1, chord=chord_2, round=True)
# chord_3 = evans.reproportion_chord(base=1, chord=chord_3, round=True)
#
# instrument_one_range_lowest = abjad.NumberedPitch(abjad.Violin().pitch_range.start_pitch)
# instrument_one_range_highest = abjad.NumberedPitch(abjad.Violin().pitch_range.stop_pitch)
#
# violin_1_chord_1 = [
#     _
#     for _ in chord_1
#     if instrument_one_range_lowest <= _ <= instrument_one_range_highest
# ]
# violin_1_chord_2 = [
#     _
#     for _ in chord_2
#     if instrument_one_range_lowest <= _ <= instrument_one_range_highest
# ]
# violin_1_chord_3 = [
#     _
#     for _ in chord_3
#     if instrument_one_range_lowest <= _ <= instrument_one_range_highest
# ]
#
# violin_1_rotated_chord_1 = evans.rotate(violin_1_chord_1, 18)
# violin_1_mirrored_chord_1 = evans.mirror(violin_1_rotated_chord_1, sequential_duplicates=False)
#
# violin_1_rotated_chord_2 = evans.rotate(violin_1_chord_2, 18)
# violin_1_mirrored_chord_2 = evans.mirror(violin_1_rotated_chord_2, sequential_duplicates=False)
#
# violin_1_rotated_chord_3 = evans.rotate(violin_1_chord_3, 18)
# violin_1_mirrored_chord_3 = evans.mirror(violin_1_rotated_chord_3, sequential_duplicates=False)
#
#
# map = [
#     evans.random_walk(random_seed=2, length=100, step_list=[1, 2, 1], mapped_list=violin_1_mirrored_chord_1),
#     evans.random_walk(random_seed=3, length=100, step_list=[2, 2, 1], mapped_list=violin_1_mirrored_chord_2),
#     evans.random_walk(random_seed=4, length=100, step_list=[1, 2, 2], mapped_list=violin_1_mirrored_chord_3),
# ]
#
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.4],projection='3d')
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x where random_seed=2 and step_list=[1, 2, 1]')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y where random_seed=3 and step_list=[2, 2, 1]')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[2]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_title('values of z where random_seed=4 and step_list=[1, 2, 2]')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0], map[1], map[2], color='black',lw=1,label='Evolution(t)')
# ax4.set_title('three simultneous random walks up to 100 iterations')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# fig.savefig('random_walks.png')
####
###Normalized Lorenz###
# map = evans.lorenz()
# m0 = evans.normalize_to_indices(map[0])
# m1 = evans.normalize_to_indices(map[1])
# m2 = evans.normalize_to_indices(map[2])
# map = [m0, m1, m2]
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.4],projection='3d')
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[2]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_title('values of z')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0], map[1], map[2], color='black',lw=1,label='Evolution(t)')
# ax4.set_title('lorenz map normalized to indices')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# fig.savefig('normalized_lorenz.png')
###
###Normalized roessler###
# map = evans.roessler(t_fin=(32 * (3.14)))
# m0 = evans.normalize_to_indices(map[0])
# m1 = evans.normalize_to_indices(map[1])
# m2 = evans.normalize_to_indices(map[2])
# map = [m0, m1, m2]
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.4],projection='3d')
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[2]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_title('values of z')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0], map[1], map[2], color='black',lw=1,label='Evolution(t)')
# ax4.set_title('roessler map normalized to indices')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# fig.savefig('normalized_roessler.png')
####
# chen
# map = evans.chen()
# m0 = evans.normalize_to_indices(map[0])
# m1 = evans.normalize_to_indices(map[1])
# m2 = evans.normalize_to_indices(map[2])
# map = [m0, m1, m2]
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.4],projection='3d')
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[2]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_title('values of z')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0], map[1], map[2], color='black',lw=1,label='Evolution(t)')
# ax4.set_title('chen map normalized to indices')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# fig.savefig('normalized_chen.png')
####
# lu chen
# map = evans.lu_chen()
# m0 = evans.normalize_to_indices(map[0])
# m1 = evans.normalize_to_indices(map[1])
# m2 = evans.normalize_to_indices(map[2])
# map = [m0, m1, m2]
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.4, 0.2])
# ax2 = fig.add_axes([0.1, 0.4, 0.4, 0.2])
# ax3 = fig.add_axes([0.1, 0.1, 0.4, 0.2])
# ax4 = fig.add_axes([0.55, 0.25, 0.35, 0.4],projection='3d')
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax3.plot([_ for _ in range(len(map[2]))], map[2], color='blue',lw=1,label='z(t)')
# ax3.set_title('values of z')
# ax3.set_xlabel('t')
# ax3.set_ylabel('z(t)')
# ax3.legend()
# ax3.axis((0, len(map[2]), min(map[2]), max(map[2])))
#
# ax4.plot(map[0], map[1], map[2], color='black',lw=1,label='Evolution(t)')
# ax4.set_title('lu-chen map normalized to indices')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# ax4.set_zlabel('z(t)')
# fig.savefig('normalized_lu_chen.png')
# henon
# map = evans.henon(iters=400)
# m0 = evans.normalize_to_indices(map[0])
# m1 = evans.normalize_to_indices(map[1])
# map = [m0, m1]
# from matplotlib import *
# from pylab import figure, show, setp
# from mpl_toolkits.mplot3d import Axes3D
# fig = figure(figsize=(20, 20))
# ax1 = fig.add_axes([0.1, 0.7, 0.8, 0.2])
# ax2 = fig.add_axes([0.1, 0.45, 0.8, 0.2])
# ax4 = fig.add_axes([0.1, 0.1, 0.8, 0.3])
#
# ax1.plot([_ for _ in range(len(map[0]))], map[0], color='red',lw=1,label='x(t)')
# ax1.set_title('values of x')
# ax1.set_xlabel('t')
# ax1.set_ylabel('x(t)')
# ax1.legend()
# ax1.axis((0, len(map[0]), min(map[0]), max(map[0])))
#
# ax2.plot([_ for _ in range(len(map[1]))], map[1], color='green',lw=1,label='y(t)')
# ax2.set_title('values of y')
# ax2.set_xlabel('t')
# ax2.set_ylabel('y(t)')
# ax2.legend()
# ax2.axis((0, len(map[1]), min(map[1]), max(map[1])))
#
# ax4.scatter(map[0], map[1], color='black',lw=1,label='Evolution(t)', s=0.5)
# ax4.set_title('henon map normalized to indices')
# ax4.set_xlabel('x(t)')
# ax4.set_ylabel('y(t)')
# fig.savefig('normalized_henon.png')
