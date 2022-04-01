"""CSC108/A08: Fall 2021 -- Assignment 1: unscramble

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Michelle Craig, Anya Tafliovich.

"""

# Valid moves in the game.
SHIFT = 'S'
SWAP = 'W'
CHECK = 'C'


# We provide a full solution to this function as an example.
def is_valid_move(move: str) -> bool:
    """Return True if and only if move is a valid move. Valid moves are
    SHIFT, SWAP, and CHECK.
    >>> is_valid_move('C')
    True
    >>> is_valid_move('S')
    True
    >>> is_valid_move('W')
    True
    >>> is_valid_move('R')
    False
    >>> is_valid_move('')
    False
    >>> is_valid_move('NOT')
    False
    """
    return move == CHECK or move == SHIFT or move == SWAP

def get_section_start(sec_number: int, sec_length: int) -> int:
    """Return the index of the first character in the specified section,
    given by the section number sec_number and the section length sec_length.
    precondition: sec_number and sec_length >= 1
    >>> get_section_start(1, 4)
    0
    >>> get_section_start(2, 4)
    4
    >>> get_section_start(3, 3)
    6
    """
    return (sec_number-1) * sec_length

def get_section(state_of_game: str, sec_number: int, sec_length: int) -> str:
    """Return the section with section length sec_length of the string
    state_of_game starting at section number sec_number.
    >>> get_section('csca08fun', 2, 3)
    'a08'
    >>> get_section('csca08fun', 1, 3)
    'csc'
    >>> get_section('csca08fun', 3, 3)
    'fun'
    """
    index = get_section_start(sec_number, sec_length)
    return state_of_game[index: index + sec_length]

def is_valid_section(game_state: str, sec_number: int, sec_length: int) -> bool:
    """Return True if and only if it is possible to divide up the given state
    string game_state into sections of the length sec_length and the section
    number sec_number, which refer to one of the resulting sections.
    >>> is_valid_section('csca08fall2021', 2, 3)
    False
    >>> is_valid_section('csca08fall2021', 4, 2)
    True
    >>> is_valid_section('csca08fall2021', 8, 2)
    False
    >>> is_valid_section('csca08fun', 2, 3)
    True
    >>> is_valid_section('csca08fun', 1, 9)
    True
    >>> is_valid_section('csca08fun', 2, 9)
    False
    """
    gam_length = len(game_state)
    not_out_of_bounds = gam_length / sec_length >= sec_number
    return gam_length % sec_length == 0 and not_out_of_bounds

def swap(game_state: str, start_index: int, end_index: int) -> str:
    """Return a swapped string which is the result of applying a swap operation
    to the section of given state string game_state between start index
    start_index (inclusive) and the end index end_index (exclusive).
    precondition: start_index > end_index - 1
    >>> swap('computerscience', 0, 8)
    'romputecscience'
    >>> swap('computerscience', 6, 10)
    'computcrseience'
    >>> swap('computerscience', 8, 10)
    'computercsience'
    """
    swap_sec = game_state[end_index - 1]
    swap_sec = swap_sec + game_state[start_index + 1:end_index - 1]
    swap_sec = swap_sec + game_state[start_index]
    return game_state[0:start_index] + swap_sec + game_state[end_index:]

def shift(game_state: str, start_index: int, end_index: int) -> str:
    """Return shifted string which is the result of applying a shift operation
    to the section of the given state string game_state between the start index
    start_index (inclusive) and the end index end_index (exclusive).
    precondition: start_index < end_index - 1
    >>> shift('computerscience', 0, 8)
    'omputercscience'
    >>> shift('computerscience', 6, 10)
    'computrsceience'
    """
    shifted = game_state[start_index + 1: end_index] + game_state[start_index]
    return game_state[0:start_index] + shifted + game_state[end_index:]

def check(game_state: str, start_index: int, end_index: int, ans: str) -> bool:
    """Return True if and only if the part of the state string game_state
    between start_index (inclusive) and the end_index (exclusive) is equal to
    the correct answer ans.
    precondition: start_index >= end_index; ans is a valid correct answer.
    >>> check('ccsa80fun', 6, 9, 'csca08fun')
    True
    >>> check('ccsa80fun', 0, 3, 'csca08fun')
    False
    """
    return game_state[start_index:end_index] == ans[start_index:end_index]

def check_section(gam_state: str, num: int, length: int, ans: str) -> bool:
    """Return True if and only if the section of the state string gam_state with
    the specfied section number num and section length length is equal to the
    correct answer ans.
    precondition: sec_num and sec_len and ans are valid.
    >>> check_section('ccsa80fun', 3, 3, 'csca08fun')
    True
    >>> check_section('ccsa80fun', 1, 3, 'csca08fun')
    False
    """
    return get_section(gam_state, num, length) == get_section(ans, num, length)

def change_section(gam_state: str, gam_move: str, num: int, length: int) -> str:
    """Return a new game state string which results from applying the given game
    move gam_move on the section of the state string gam_state with the section
    number num and section length length.
    precondition: num and length are valid for the given state string,and
    gam_move is a valid game move.
    >>> change_section('computerscience', 'W', 2, 5)
    'compucerstience'
    >>> change_section('computerscience', 'S', 2, 5)
    'compuersctience'
    """
    sec_start_index = get_section_start(num, length)
    if gam_move == SHIFT:
        return shift(gam_state, sec_start_index, sec_start_index + length)
    if gam_move == SWAP:
        return swap(gam_state, sec_start_index, sec_start_index + length)
    return ''

def get_move_hint(game_state: str, sec_num: int, sec_len: int, ans: str) -> str:
    """Return a suggestion, based on the correct answer ans for the specified
    section number sec_num and section length sec_len, for which game move to
    perform next on the state string game_state.
    precondition: sec_num and sec_len and correct_answer are valid.
    >>> get_move_hint('compuctersience', 2, 5, 'computerscience')
    'S'
    >>> get_move_hint('TCADOGFOXEMU', 1, 3, 'CATDGOXOFEMU')
    'S'
    >>> get_move_hint('TACDOGFOXEMU', 1, 3, 'CATDGOXOFEMU')
    'W'
    """
    one_shift = change_section(game_state, SHIFT, sec_num, sec_len)
    two_shifts = change_section(one_shift, SHIFT, sec_num, sec_len)
    if check_section(one_shift, sec_num, sec_len, ans):
        return 'S'
    if check_section(two_shifts, sec_num, sec_len, ans):
        return 'S'
    return 'W'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    