import sys

MAX_WORD_LENGTH = 137


class Dictionary:
    def __init__(self, filename):
        try:
            file_handle = open(filename)
        except:
            print("%s open failure", filename)
            sys.exit()

        self.__partition = [[] for i in range(MAX_WORD_LENGTH + 1)]

        for line in file_handle:
            word = line.rstrip()
            self.__partition[len(word)].append(word)

        file_handle.close()

    def get_words_of_length(self, l):
        return self.__partition[l]

#'''

    def __str__(self):
        for i in range(1, MAX_WORD_LENGTH + 1):
            #if len(self.__partition[i]) > 0:
                #print(self.__partition[i])
            print("word length ", i, ": ", len(self.__partition[i]))
        return ""

#'''



