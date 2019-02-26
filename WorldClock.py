#
#  Word Clock - TimeDescription helper class
#   Jim Rowe
#   2/22/2019
#
import time

from console import fg

# time letter array
letters = ['I', 'T', 'L', 'I', 'S', 'E', 'J', 'U', 'S', 'T', 'L', 'O', 'B', 'E', 'F', 'O', 'R', 'E', 'V', 'A', 'F', 'T', 'E', 'R', 'Q', 'U', 'A', 'R', 'T', 'E', 'R', 'E', 'H', 'A', 'L', 'F', 'T', 'W', 'E', 'N', 'T', 'Y', 'S', 'F', 'I', 'V', 'E', 'A', 'D', 'T', 'E', 'N', 'R', 'M', 'I', 'N', 'U', 'T', 'E', 'S', 'P', 'A', 'S', 'T', 'T',
           'O', 'I', 'T', 'H', 'R', 'E', 'E', 'O', 'N', 'E', 'L', 'T', 'W', 'O', 'S', 'E', 'V', 'E', 'N', 'F', 'O', 'U', 'R', 'F', 'I', 'V', 'E', 'N', 'I', 'N', 'E', 'S', 'I', 'X', 'A', 'E', 'I', 'G', 'H', 'T', 'T', 'E', 'N', 'E', 'L', 'E', 'V', 'E', 'N', 'T', 'W', 'E', 'L', 'V', 'E', 'O’', 'C', 'L', 'O', 'C', 'K', 'N', 'A', 'M', 'J', 'P', 'M']

# matrix layout
ROW_LENGTH = 12
ROWS = 11

# time words
c_it = [0, 1]
c_is = [3, 4]
c_just = [6, 7, 8, 9]
c_before = [12, 13, 14, 15, 16, 17]
c_after = [19, 20, 21, 22, 23]
c_a = [19]
c_quarter = [24, 25, 26, 27, 28, 29, 30]
c_half = [32, 33, 34, 35]
c_twenty = [36, 37, 38, 39, 40, 41]
c_five = [43, 44, 45, 46]
c_ten = [49, 50, 51]
c_minutes = [53, 54, 55, 56, 57, 58, 59]
c_past = [60, 61, 62, 63]
c_to = [64, 65]
c_three = [67, 68, 69, 70, 71]
c_one = [72, 73, 74]
c_two = [76, 77, 78]
c_seven = [79, 80, 81, 82, 83]
c_four = [84, 85, 86, 87]
c_five2 = [88, 89, 90, 91]
c_nine = [92, 93, 94, 95]
c_six = [96, 97, 98]
c_eight = [100, 101, 102, 103, 104]
c_ten2 = [105, 106, 107]
c_eleven = [108, 109, 110, 111, 112, 113]
c_twelve = [114, 115, 116, 117, 118, 119]
c_oclock = [120, 121, 122, 123, 124, 125]
c_am = [127, 128]
c_pm = [130, 131]

words = [c_it, c_is, c_just, c_before, c_after, c_a, c_quarter, c_half, c_twenty, c_five,
         c_ten, c_minutes, c_past, c_to, c_three, c_one, c_two, c_seven, c_four, c_five2,
         c_nine, c_six, c_eight, c_ten2, c_eleven, c_twelve, c_am, c_pm]

minRound = 3


def print_matrix(selectedLetters):
    for i in range(ROWS):
        for j in range(ROW_LENGTH):
            idx = i * ROW_LENGTH + j
            if(idx in selectedLetters):
                print(fg.red + letters[idx], end=' ')
            else:
                print(fg.white + letters[idx], end=' ')
        print('')

    print(fg.white)


# class to calculate the current time in words
class WorldClock:
    def __init__(self, currentLocalTimeStruct):
        self._it = c_it
        self._iz = c_is
        self._just = []
        self._beforeAfter = []
        self._minute = []
        self._minutes = c_minutes
        self._toPast = []
        self._hour = []
        self._oClock = c_oclock
        self._amPmWord = []
        self._current24Hour = currentLocalTimeStruct[3]
        self._currentHour = self._current24Hour
        self._currentMinute = currentLocalTimeStruct[4]
        self._calculate_words()

    # get the letter array
    def get_letter_array(self):
        self._calculate_words()
        return self._it + self._iz + self._just + self._beforeAfter + self._minute + self._minutes + \
            self._toPast + self._hour + self._oClock + self._amPmWord

    def get_words(self):
        wordList = []
        wordList.append(self._get_word_text(self._it))
        wordList.append(self._get_word_text(self._iz))
        wordList.append(self._get_word_text(self._just))
        wordList.append(self._get_word_text(self._beforeAfter))
        wordList.append(self._get_word_text(self._minute))
        wordList.append(self._get_word_text(self._minutes))
        wordList.append(self._get_word_text(self._toPast))
        wordList.append(self._get_word_text(self._hour))
        wordList.append(self._get_word_text(self._oClock))
        wordList.append(self._get_word_text(self._amPmWord))
        return wordList

    # print the words, one-per-line
    def print_words(self):
        words = self.get_words()
        for w in words:
            if(w != ''):
                print(w)

    # calculate the words for the current time

    def _calculate_words(self):
        self._get_before_after()
        self._get_minutes()
        self._get_am_pm()
        self._get_hour()

    def _print_word(self, letterArray):
        for l in letterArray:
            print(letters[l], end='')
        print('')

    def _get_word_text(self, letterArray):
        word = ""
        for l in letterArray:
            word += letters[l]
        return word

    # just before/after modifier
    def _get_before_after(self):
        deltaMinute = self._currentMinute % 5
        if(deltaMinute == 0):
            self._just = []
            self._beforeAfter = []
        elif(deltaMinute < 3):
            self._just = c_just
            self._beforeAfter = c_after
        else:
            self._just = c_just
            self._beforeAfter = c_before

    # minute modifer
    def _get_minutes(self):
        self._minutes = c_minutes
        self._toPast = c_past
        minute = self._currentMinute
        if (minute < minRound):
            self._minute = []
            self._toPast = []
            self._minutes = []
        elif (minute < 5 + minRound):
            self._minute = c_five
        elif (minute < 10 + minRound):
            self._minute = c_ten
        elif (minute < 15 + minRound):
            self._minute = c_quarter
            self._minutes = c_a
        elif (minute < 20 + minRound):
            self._minute = c_twenty
        elif(minute < 25 + minRound):
            self._minute = c_twenty + c_five
        elif(minute < 30 + minRound):
            self._minute = c_half
            self._minutes = c_a
        elif(minute < 35 + minRound):
            self._minute = c_twenty + c_five
            self._toPast = c_to
        elif(minute < 40 + minRound):
            self._minute = c_twenty
            self._toPast = c_to
        elif(minute < 45 + minRound):
            self._minute = c_quarter
            self._minutes = c_a
            self._toPast = c_to
        elif(minute < 50 + minRound):
            self._minute = c_ten
            self._toPast = c_to
        elif(minute < 55 + minRound):
            self._minute = c_five
            self._toPast = c_to
        elif(minute < 60):
            self._minute = []
            self._toPast = []
            self._minutes = []

    # am/pm
    def _get_am_pm(self):
        self._amPmWord = c_am

        if(self._current24Hour > 12):
            self._amPmWord = c_pm

        if(self._currentMinute > 30 + minRound):
            self._currentHour = (self._current24Hour + 1) % 12
        else:
            self._currentHour = self._current24Hour % 12

    # hour
    def _get_hour(self):
        switcher = {
            0: c_twelve,
            1: c_one,
            2: c_two,
            3: c_three,
            4: c_four,
            5: c_five2,
            6: c_six,
            7: c_seven,
            8: c_eight,
            9: c_nine,
            10: c_ten,
            11: c_eleven,
            12: c_twelve
        }
        self._hour = switcher[self._currentHour]
