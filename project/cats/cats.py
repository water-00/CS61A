"""Typing test implementation"""
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    i = 0
    for p in paragraphs:
        if select(p) and i == k:
            return p
        elif select(p):
            i += 1
        
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def has_word(str):
        str = remove_punctuation(lower(str))
        sp = split(str)
        for t in topic:
            for s in sp:
                if t == s:
                    return True
        return False
    return has_word
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    right, wrong = 0, 0
    if typed_words == [] or reference_words == []:
        return 0.0
    i = 0
    if len (typed_words) > len(reference_words):
        wrong += len(typed_words) - len(reference_words)

        
    while i < min(len(typed_words), len(reference_words)):
        if typed_words[i] == reference_words[i]:
            right += 1
        else:
            wrong += 1
        i += 1
    return right / (right + wrong) * 100
    
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed) * 12 / elapsed
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # 首先看valid_words中有没有user_word，如果有直接返回user_word即可
    # 如果没有，如果diff_function's return <= limit(说明可以更正)，返回valid_words中diff最小的单词
    # 如果存在diff相同的单词，返回先在valid_words中出现的
    lowest_diff = 999
    lowest_idx = -1
    for i in range(0, len(valid_words)):
        if user_word == valid_words[i]:
            return user_word
        
        diff = diff_function(user_word, valid_words[i], limit)
        if diff <= limit and diff < lowest_diff:
            lowest_diff = diff
            lowest_idx = i

    if lowest_idx != -1:
        return valid_words[lowest_idx]
    else:
        return user_word
        
    
    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    diff_num = abs(len(start) - len(goal))
    def helper(start, goal, diff_num):
        if start == '' or goal == '':
            return diff_num
        if start[0] != goal[0]:
            diff_num += 1
        if diff_num > limit:
            return limit + 1
        else:
            return helper(start[1:], goal[1:], diff_num)
    return helper(start, goal, diff_num)
    
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def add_ch(start, goal, diff):
        # 将goal[0]添加到start开头
        if diff == limit:
            return start, goal, limit + 1 # impossible
        else:
            start = goal[0] + start
            return start, goal, diff + 1
        
    def remove_ch(start, goal, diff):
        # 移去start[0]
        if diff == limit:
            return start, goal, limit + 1 # impossible
        else:
            start = start[1:]
            return start, goal, diff + 1
        
    def substitute_ch(start, goal, diff):
        # 将start[0]替换为goal[0]
        if diff == limit:
            return start, goal, limit + 1 # impossible
        else:
            start = goal[0] + start[1:]
            return start, goal, diff + 1

    def helper(start, goal, diff):    
        while True:
            if diff > limit:
                return limit + 1
            if start == goal:
                return diff
            if start == '' and goal != '':
                start, goal, diff = add_ch(start, goal, diff)
                continue
            elif start != '' and goal == '':
                start, goal, diff = remove_ch(start, goal, diff)
                continue
            elif start[0] == goal[0]:
                start, goal = start[1:], goal[1:]
                continue
            else:
                str1, str2, add_diff = add_ch(start, goal, diff)
                str3, str4, remove_diff = remove_ch(start, goal, diff)
                str5, str6, substitute_diff = substitute_ch(start, goal, diff)
                if add_diff == limit + 1 and remove_diff == limit + 1 and substitute_diff == limit:
                    # all impossible
                    return limit + 1
                else:
                    return min(helper(str1, str2, add_diff), helper(str3, str4, remove_diff), helper(str5, str6, substitute_diff))
    
    return helper(start, goal, 0)
    # END PROBLEM 7



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    total_words = len(prompt)
    correct_words = 0
    for i in range(0, len(typed)):
        if typed[i] == prompt[i]:
            correct_words += 1
        else:
            break
    progress = correct_words / total_words
    d = {'id': user_id, 'progress': progress}
    send(d)
    return progress
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    # len(times_per_player)个玩家打len(words)单词, 每个单词花费的时间
    times = [[times_per_player[k][i+1] - times_per_player[k][i] for i in range(len(words))] for k in range(len(times_per_player))]
    return game(words, times)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    fastest = [[] for _ in player_indices]
    for i in word_indices:
        min_idx = -1 # 拥有这个word的最小时间的player的idx
        min_time = 999
        for j in player_indices:
            if min_time > time(game, j, i):
                min_time = time(game, j, i)
                min_idx = j
        fastest[min_idx].append(word_at(game, i))
    return fastest
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)