"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

def free_bacon(opponent_score):
    if(opponent_score >= 10):
        first_digit = opponent_score//10
        second_digit = opponent_score - first_digit * 10
        return max(first_digit, second_digit) + 1
    elif(opponent_score < 10):
        return opponent_score + 1

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    point = 0
    one_is_rolled = False
    while num_rolls != 0:
        dice_outcome = dice()
        num_rolls = num_rolls - 1
        if dice_outcome == 1:
            one_is_rolled = True
        else:
            point += dice_outcome
    ### Pig Out Rule ###
    if(one_is_rolled == True):
        point = 1
    return point

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE"
    if(num_rolls == 0):
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    dice = six_sided
    if (score + opponent_score) % 7 == 0:
        dice = four_sided
    return dice

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0
    "*** YOUR CODE HERE ***"
    while score < goal and opponent_score < goal:
        dice = select_dice(score, opponent_score)
        if who == 0:
            score += take_turn(strategy0(score,opponent_score),opponent_score,dice)
        elif who == 1:
            opponent_score += take_turn(strategy1(opponent_score,score),score,dice)
        who = other(who)
        
        ### Swine Swap Rule ###
        if(opponent_score == 2*score or 2*opponent_score == score):
            score, opponent_score = opponent_score, score
    return score, opponent_score # You may wish to change this line.

#######################
# Phase 2: Strategies #
#######################

# Basic Strategy


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def average(*args):
        total = 0
        for number in range(num_samples):
            total += fn(*args)
        return total/num_samples
    return average

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    "*** YOUR CODE HERE ***"
    highest = 0
    for dice_outcome in range(1,11):
        this_roll_outcome = make_averaged(roll_dice)(dice_outcome,dice)
        print(dice_outcome, 'dice scores', this_roll_outcome, 'on average')
        if(this_roll_outcome > highest):
            highest = dice_outcome
    return highest

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    if free_bacon(opponent_score) >= margin:
        return 0
    else:
        return num_rolls

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    expected_score = free_bacon(opponent_score) + score
    if expected_score == (opponent_score/2):
        return 0
    elif expected_score >= margin and expected_score < opponent_score:
        return 0
    else:
        return num_rolls

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    First break up the strategy based on whether you're rolling 4 or 6 sided dice.
    Then find if you have the opportunity to take advantage of the swine swap, hog wild,
    or free bacon rules.
    If you do, take advantage by rolling the optimal number of dice (the one that will
        most probably achieve the "strategy" to occur).
    """
    "*** YOUR CODE HERE ***"

    total_score = score + opponent_score
    
    if (total_score % 7 == 0): #Rolling 4-sided dice
        if (opponent_score == (2*(score + 1))): #Checks for Swine Swap rule
            return 10
        elif (opponent_score == 2*(score + free_bacon(opponent_score))):  #Swine Swap
            return 0
        elif (7 - (score + opponent_score) % 7 == 1): #Hog Wild
            return 10
        elif (total_score + free_bacon(opponent_score)) % 7 == 0: #Hog Wild
            return 0
        elif (free_bacon(opponent_score) > 6): #Abuses free bacon
            return 0
        else: #1/4 chance of rolling a 1, so we roll fewer dice to reduce that chance
            return 3
    else: # Rolling 6-sided dice
        if (opponent_score == (2 * (score + 1))): #Swine swap
            return 10
        elif (opponent_score == 2 * (score + free_bacon(opponent_score))): #swine swap
            return 0
        elif (total_score + free_bacon(opponent_score)) % 7 == 0: #hog wild
            return 0
        elif (free_bacon(opponent_score) > 8): #Free bacon if it will give us optimal score
            return 0
        return 6 #optimal number of dice to roll

##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
