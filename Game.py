import random
import string

from Dictionary import Dictionary

MAXIMUM_REMAINING_MODE, RANDOM_REMAINING_MODE = False, True

MAX_WORD_LENGTH = 137


def share_pattern_based_on_char(word1, word2, ch):  # assume that word1 and word2 are of the same length
    for i in range(len(word1)):
        if word1[i] == ch and word2[i] != ch:
            return False
        if word1[i] != ch and word2[i] == ch:
            return False
    return True


class WordGuessing:
    def __init__(self, filename):
        # game setting parameters
        self.__my_dictionary = Dictionary(filename)
        #print(self.__my_dictionary)
        self.__word_length = 0
        self.__guess_num = 0
        self.__want_remaining_num = False
        # guessing status
        self.__remaining_word_list = []
        self.__guessed_letter_list = []
        self.__current_blanked_out_version = ""

    # game settings
    def __ask_for_word_length(self):
        while True:
            try:
                wd_len = int(input("Input a word length:"))
            except:
                continue
            if wd_len < 1 or wd_len > MAX_WORD_LENGTH:
                continue
            if self.__my_dictionary.get_words_of_length(wd_len):
                break
        self.__word_length = wd_len
        self.__remaining_word_list = self.__my_dictionary.get_words_of_length(wd_len)
        self.__current_blanked_out_version = "-" * wd_len

    def __ask_for_guess_num(self):
        while True:
            try:
                guess_n = int(input("Input the number of guesses:"))
            except:
                continue
            if guess_n >= 1:
                break
        self.__guess_num = guess_n

    def __ask_whether_want_remaining_num(self):
        while True:
            in_str = input("Do you want the number of remaining words? (y/n)")
            if in_str == "y":
                self.__want_remaining_num = True
                break
            elif in_str == "n":
                self.__want_remaining_num = False
                break

    def __clear(self):
        # guessing status
        self.__remaining_word_list = []
        self.__guessed_letter_list = []
        self.__current_blanked_out_version = ""

    def __set_game(self):
        self.__clear()
        self.__ask_for_word_length()
        self.__ask_for_guess_num()
        self.__ask_whether_want_remaining_num()

    # game playing
    def __shrink_remaining_word_list(self, ch):
        pattern_partition_list = [[] for i in range(len(self.__remaining_word_list))]

        for word in self.__remaining_word_list:
            for i in range(len(self.__remaining_word_list)):
                if not pattern_partition_list[i] or share_pattern_based_on_char(word, pattern_partition_list[i][0], ch):
                    pattern_partition_list[i].append(word)
                    break

        if RANDOM_REMAINING_MODE:
            #empty_list_num = pattern_partition_list.count([])
            #filled_list_num = len(pattern_partition_list) - empty_list_num
            indicator_list = [1 for i in range(len(self.__remaining_word_list)) if pattern_partition_list[i]]
            self.__remaining_word_list = pattern_partition_list[random.randrange(0, len(indicator_list), 1)]

        if MAXIMUM_REMAINING_MODE:
            len_lst = [len(li) for li in pattern_partition_list]
            index_of_biggest_partition = len_lst.index(max(len_lst))
            self.__remaining_word_list = pattern_partition_list[index_of_biggest_partition]

    def __guess(self, ch):  # assume that ch has never been guessed before
        self.__shrink_remaining_word_list(ch)
        # guessed letter list
        self.__guessed_letter_list.append(ch)
        # blanked out version
        word = self.__remaining_word_list[0]
        for ch in word:
            if ch not in self.__guessed_letter_list:
                word = word.replace(ch, "-")
        self.__current_blanked_out_version = word

    def __play(self):
        for i in range(self.__guess_num):
            print("The number of remaining guesses is %d" % (self.__guess_num - i))
            print("The guessed letter list: " + str(sorted(self.__guessed_letter_list)))
            print("The blanked out version: " + self.__current_blanked_out_version)
            if self.__want_remaining_num:
                print("The number of remaining words is %d" % len(self.__remaining_word_list))

            while True:
                ch = input("guess a letter:\n")
                if len(ch) != 1:
                    continue
                if ch not in string.ascii_letters:
                    continue
                ch = ch.lower()
                if ch not in self.__guessed_letter_list:
                    break

            self.__guess(ch)
            if "-" not in self.__current_blanked_out_version:
                print("Congratulations, you have obtained the correct answer.")
                print("The word is :", self.__current_blanked_out_version)
                return

        print("Sorry, attempts are used up")
        shown_word = self.__remaining_word_list[random.randrange(0, len(self.__remaining_word_list), 1)]
        print("The word to be guessed is: ", shown_word)

    def execute(self):
        want_to_go_on = True
        while want_to_go_on:
            self.__set_game()
            self.__play()
            while True:
                in_str = input("Do you want to go on? (y/n)")
                if in_str == "y":
                    want_to_go_on = True
                    break
                elif in_str == "n":
                    want_to_go_on = False
                    break
