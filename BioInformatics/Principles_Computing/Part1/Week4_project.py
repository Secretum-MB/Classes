# principles of computing
# week 4: project
# permutations and combinations: Yahtzee


"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
	"""
	Compute the maximal score for a Yahtzee hand according to the
	upper section of the Yahtzee score card.
	hand: full yahtzee hand
	Returns an integer score
	"""
	scores = set()
	for die in hand:
		current_count = 0
		for die_for_counting in hand:
			if die_for_counting == die:
				current_count += 1
		scores.add(die * current_count)
	return max(scores)


def expected_value(held_dice, num_die_sides, num_free_dice):
	"""
	Compute the expected value based on held_dice given that there
	are num_free_dice to be rolled, each with num_die_sides.
	held_dice: dice that you will hold
	num_die_sides: number of sides on each die
	num_free_dice: number of dice to be rolled
	Returns a floating point expected value
	"""
	die_results = list(side for side in range(1, num_die_sides + 1))
	possible_rolls = gen_all_sequences(die_results, num_free_dice)

	possible_hands = set()
	for each_roll in possible_rolls:
		possible_hands.add(tuple(list(held_dice) + list(each_roll)))

	possible_scores = []
	for hand in possible_hands:
		possible_scores.append(score(hand))
	return float(sum(possible_scores) / len(possible_scores))


def gen_all_holds(hand):
	"""
	Generate all possible choices of dice from hand to hold.
	hand: full yahtzee hand
	Returns a set of tuples, where each tuple is dice to hold
	"""
	def find_all_combinations(hand, length):
		"generates all unique hand combinations of specified length"
		answer_set = set([()])
		for dummy_idx in range(length):
			temp_set = set()
			for partial_sequence in answer_set:
				for item in hand:
					new_sequence = list(partial_sequence)
					new_sequence.append(item)
					temp_set.add(tuple(sorted(new_sequence)))
			answer_set = temp_set
		return answer_set


	return find_all_combinations(hand, 2)




print(gen_all_holds(tuple((2,3,3,3,4))))
print(gen_all_holds(tuple((1,1,1,5,6))))




def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.
    hand: full yahtzee hand
    num_die_sides: number of sides on each die
    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    return (0.0, ())


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, \
		  "with expected score", hand_score)


#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)








