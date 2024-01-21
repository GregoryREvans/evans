### FROM https://github.com/sraaphorst/dispersive-flies-optimization
# A S(t, k, v) Steiner system is a set of k-sets from a v-set such that every t-set appears in exactly one k-set. A simple example is S(2, 3, 7), the Steiner triple system of order 7, also denoted STS(7). Let {0, ..., 6} be the v-set.
import sys
from math import factorial
from itertools import combinations
import numpy as np


def discrete_clamper(dmin, dmax, fly):
    """
    A value adjuster that constrains the value to the dmin and dmax given, and then picks the closest discrete
    value in the range.
    """
    return np.maximum(dmin, np.minimum(dmax, np.round(fly)))


def identity(_1, _2, fly):
    return fly


def manhattan_metric(f1, f2):
    """
    The Manhattan metric for fly distances.
    """
    return np.linalg.norm(f1 - f2, ord=1)


def euclidean_metric(f1, f2):
    """
    The Euclidean metric for fly distances.
    """
    return np.linalg.norm(f1 - f2)


class DispersiveFlies:
    """
    An implementation of the Dispersive Flies Optimization algorithm.
    It requires very few parameters, namely:
    1. A dimension D for the space in which the flies inhabit.
    2. A fly fitness evaluation function, which should operate on a 1D array numpy array of length D.
    3. The maximum number of non-zero entries that a randomly generated fly should have.
    4. Stopping value: stops if this value is achieved, assuming that it is the best fitness
       Default is None, meaning never stop and simply complete all rounds.
    5. The disturbance threshold, i.e. the probability a fly's coordinate is reset.
       Default is 0.025. TODO: Play with this.
    Note: values in the array are constrained to [min,max): this is why we use 2 instead of 1 for max.
    6. A numpy array to provide minimum values for each dimension.
       Default: all dimensions have minimum 0.
    7. A numpy array to provide maximum values for each dimension.
       Default: all dimensions are 2.
    8. True if the solution space is discrete, and false otherwise.
       Default: True
    9. The distance norm for finding neighbour flies.
       Default: manhattan_metric
    10. An adjustment function for values in each dimension.
        Default is discrete_clamper.
        Use the identity if you do not want any adjustment.
    11. The number of flies. Default is 500.
    12. At the end of a round, if this is not None, call this function with the flies.
    13. The number of ticks (time units / rounds) to try. Default is 300,000.
    """

    class Statistics:
        def __init__(self):
            self._rounds = 0

    def __init__(self,
                 dimensions,
                 fitness,
                 block_size=None,
                 stop_value=None,
                 disturbance_threshold=0.025,
                 dim_min=None,
                 dim_max=None,
                 discrete=True,
                 metric=manhattan_metric,
                 adjustment=discrete_clamper,
                 flies=50,
                 max_ticks=10,
                 end_round=None,
                 debug=False):
        self._dimensions = dimensions
        self._fitness = fitness
        self._block_size = self._dimensions if block_size is None else block_size
        self._stop_value = stop_value

        self._disturbance_threshold = disturbance_threshold

        self._dim_min = np.zeros(dimensions) if dim_min is None else dim_min
        self._dim_max = np.full(dimensions, 2) if dim_max is None else dim_max
        self._discrete = discrete
        self._metric = metric

        self._adjustment = adjustment
        self._flies = flies
        self._max_ticks = max_ticks
        self._end_round = end_round
        self._flypos = None
        self._debug = debug

    def _produce_random_dimension(self, d):
        value = np.random.random() * (self._dim_max[d] - self._dim_min[d]) + self._dim_min[d]
        return int(value) if self._discrete else value

    def _produce_random_fly(self):
        # Constrain the number of non-zero entries to the stop value.
        # fly = np.random.rand(self._dimensions) * (self._dim_max - self._dim_min) + self._dim_min
        positions = np.random.random_integers(0, self._dimensions, self._block_size)
        fly = np.array([(np.random.random() * (self._dim_max[i] - self._dim_min[i]) + self._dim_min[i]
                         if i in positions else 0)
                        for i in range(self._dimensions)])
        return fly.astype(int) if self._discrete else fly

    def run(self):
        s = DispersiveFlies.Statistics()

        for t in range(self._max_ticks):
            print(t)
            best_fly = self.run_round()
            if self._stop_value and self._fitness(self._flypos[best_fly]) == self._stop_value:
                s.ticks = t
                return s, True, self._flypos[best_fly]

        # If we reach this point, we have run out of ticks.
        # Get and return the best fly.
        evaluations = np.array([self._fitness(fly) for fly in self._flypos])
        best_fly = np.argmax(evaluations)
        s.ticks = self._max_ticks
        return s, False, self._flypos[best_fly]

    def run_round(self):
        if self._flypos is None:
            # Create the flies randomly.
            self._flypos = np.array([self._produce_random_fly() for _ in range(self._flies)])

        # Shuffle the flies to randomize tie-breaking.
        np.random.shuffle(self._flypos)

        # Evaluate the flies and find the best.
        # evaluations = self._fitness(flies)
        evaluations = np.array([self._fitness(fly) for fly in self._flypos])
        best_fly = np.argmax(evaluations)
        if self._debug:
            print("Best: {}".format(evaluations[best_fly]))

        # Initialize the array of new fly positions.
        new_flies = np.zeros((self._flies, self._dimensions))

        # Create one new fly at a time.
        for f in range(self._flies):
            # First, find the nearest neighbour fly. Skip over this fly, obviously, and adjust appropriately
            # if the nearest neighbour is after this fly.
            nbr = np.argmin([self._metric(self._flypos[f], fp) for n, fp in enumerate(self._flypos) if n != f])
            if nbr >= f:
                nbr += 1

            for d in range(self._dimensions):
                # Calculation is as follows:
                # Nearest nbr + U(0,1) * (best fly - this fly)
                new_fly = self._flypos[nbr] +\
                          np.random.rand(self._dimensions) * (self._flypos[best_fly] - self._flypos[f])

                # For each coordinate, we check if we replace it randomly.
                # We use a list comprehension instead of np.vectorize due to problems with vectorize.
                # where doesn't seem to work well here.
                # random_matrix = np.random.rand(self._dimensions)
                # random_fly = self._produce_random_fly()
                # new_fly_adj = np.where(random_matrix < self._disturbance_threshold, random_fly, new_fly)
                new_fly_adj = np.array([self._produce_random_dimension(d)
                                        if np.random.random() < self._disturbance_threshold
                                        else value
                                        for d, value in enumerate(new_fly)])
                new_flies[f] = self._adjustment(self._dim_min, self._dim_max, new_fly_adj)

        self._flypos = new_flies

        if self._end_round is not None:
            self._end_round(self._flypos)
        return best_fly


def steiner(t, k, v):
    # Yes, there is some redundancy here.
    # I still like to have all the conditions explicitly listed.
    if not (1 < t < k):
        raise ValueError("Must have 1 < t < k")
    if not (t < k < v):
        raise ValueError("Must have t < k < v")
    if not (v > k):
        raise ValueError("Must have v > k")

    # Check feasibility.
    vCt = factorial(v) // factorial(t) // factorial(v - t)
    kCt = factorial(k) // factorial(t) // factorial(k - t)
    if vCt % kCt != 0:
        raise ValueError("Necessary condition vCt / kCt failed")
    v1Ct1 = factorial(v - 1) // factorial(t - 1) // factorial(v - t)
    k1Ct1 = factorial(k - 1) // factorial(t - 1) // factorial(k - t)
    if v1Ct1 % k1Ct1 != 0:
        raise ValueError("Necessary condition (v-1)C(t-1) / (k-1)C(t-1) failed")

    # Formulate the problem. The number of dimensions is the number of blocks.
    total_blocks = factorial(v) // factorial(k) // factorial(v - k)

    # We need the fitness function.
    # Precalculate the list of t-sets that come from k-sets. Our score will be the number of t-sets that are
    # covered, with a score of zero if a t-set is not covered.
    tset_lookup = {tset: num for num, tset in enumerate(combinations(range(v), t))}
    ksets = list(enumerate(combinations(range(v), k)))

    # Since flies will be incidence vectors of t-sets, we want a map of k-sets to t-sets they cover.
    # The stopping point will be when score is the number of tsets.
    kset_dict = {num: [tset_lookup[tset] for tset in combinations(kset, t)] for num, kset in ksets}

    def fitness(vector):
        # Figure out what we have covered.
        coverage = [tsetnum for ksetnum, kincidence in enumerate(vector)
                    for tsetnum in kset_dict[ksetnum] if kincidence == 1]

        # If we have covered any t-set multiple times, the score drops to 0 as it is an infeasible solution.
        # Otherwise, it is the number of covered t-sets.
        size = len(coverage)
        # return len(set(coverage))
        if len(set(coverage)) == size:
            return size
        else:
            return 0

    # Instantiate the problem.
    dimensions = len(ksets)
    block_size = (factorial(v) // factorial(t) // factorial(v - t)) //\
                 (factorial(k) // factorial(t) // factorial(k - t))
    solution_size = len(tset_lookup)
    print("Solution size is {}".format(solution_size))
    problem = DispersiveFlies(dimensions, fitness, block_size, solution_size, flies=100, debug=True)

    stats, finished, solution = problem.run()
    return stats, fitness(solution) == solution_size, solution



# if len(sys.argv) != 4:
#     print("Usage: {} t k v".format(sys.argv[0]))
#     sys.exit(1)
# t, k, v = map(int, sys.argv[1:])

def do_steiner(t, k, v):

    stats, finished, solution = steiner(t, k, v)
    ksets = list(combinations(range(v), k))
    readable_solution = [ksets[i] for i, value in enumerate(solution) if value == 1]

    if finished:
        for b in readable_solution:
            print(b)
        # sys.exit(0)
    else:
        print("Could not finish. Best solution has size {}:".format(len([i for i in solution if i])))
        for b in readable_solution:
            print(b)
        # sys.exit(2)

# t, k, v
# t = subsets of this size are contained in exactly 1 returned group
# k = number of elements in each returned group
# v = number of possible elements (and ideally number of returned groups)
# NECESSARY CONDITION: (v-1)C(t-1) / (k-1)C(t-1)
do_steiner(2, 3, 13)
# for triples: 6k+1 or 6k + 3 for some k
# there are two STS(13)s, 80 STS(15)s, and 11,084,874,829 STS(19)s
# 2, 3, 7
# 2, 3, 9
# projective plane: S(2, q + 1, q2 + q + 1)
# affine plane: S(2, q, q2)
# S(3,4,n) is that n ≡ 2 or 4 (mod 6)
# S(4,5,n) is that n ≡ 3 or 5 (mod 6) and n ≢ 4 (mod 5) [11, 23, 35, 47, 71, 83, 107, 131, 167 and 243]

# AUTOMORPHISM GROUPS
# The Mathieu group M11 is the automorphism group of a S(4,5,11) Steiner system
# The Mathieu group M12 is the automorphism group of a S(5,6,12) Steiner system
# The Mathieu group M22 is the unique index 2 subgroup of the automorphism group of a S(3,6,22) Steiner system
# The Mathieu group M23 is the automorphism group of a S(4,7,23) Steiner system
# The Mathieu group M24 is the automorphism group of a S(5,8,24) Steiner system.
