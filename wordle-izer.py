import string, re
from english_words import english_words_set

alphabet = list(string.ascii_lowercase)
word = {
	1: "",
        2: "",
        3: "",
        4: "",
        5: ""
}

def only_letters_allowed(tries):
	global alphabet
	trimmed = []

	for t in tries:
		if t not in alphabet:
			print("invalid input detected: {}".format(t))
		else:
			trimmed.append(t)
	return trimmed


def get_correct():
	global alphabet

	# Get number of correct letters
	while True:
		try:
			num_correct = int(input("How many letters do you have correct so far? "))
			assert (num_correct > -1 and num_correct < 6)
			break
		except ValueError:
			print("whole numbers only please.")
		except AssertionError:
			print("Must be from 0 to 5.")

	# End if none
	if num_correct == 0:
		return False

	inp = input("Please enter the position (1,2,3,4,5) of the letter you have correct, then the letter itself. Enter to pass.\nExample: 1 b [press enter], 3 e [press enter]\n")
	tries = inp.split(" ")

	count = 0
	while count != num_correct:
		if len(tries) == 2:
			try:
				index = int(tries[0])
				if tries[1] not in alphabet:
					raise ValueError

				word[index] = tries[1]
				count += 1
				if count == num_correct:
					break
				tries = input("Please enter the next correct position & letter: ").split(" ")
			except ValueError:
				print("Value error for one of two inputs, should be integer and single character.")
				tries = input("Please try again: ").split(" ")
		else:
			tries = input("Please ensure there are only 2 values, one position and one letter. ").split(" ")
	return True


def get_right_letter_wrong_spot():
	inp = input("Please enter the letters you have that are correct, but in the wrong spot. Enter to pass\n")
	tries = inp.split(" ")
	if tries[0] == '':
		return False
	return only_letters_allowed(tries)


def get_incorrect():
	inp = input("Please enter the letters you have that are incorrect, with a space between! Enter to pass\n")
	tries = inp.split(" ")
	if tries[0] == '':
		return False
	return only_letters_allowed(tries)


def main():
	global english_words_set

	print("Welcome to Wordle-izer!\nFirst we need some basic info.\n")

	# value is True or False. False means none correct yet. "GREEN" letters
	value = get_correct()

	print("{}".format(word))

	# letters_to_use is False if none, or a list of letters otherwise. "YELLOW" letters
	letters_to_use = get_right_letter_wrong_spot()
	if letters_to_use != False:
		print("Must include {}".format(letters_to_use))

	# letters_to_exclude is False if none, or a list of letters otherwise. "GREY" letters
	letters_to_exclude = get_incorrect()
	if letters_to_exclude != False:
		print("Must exclude {}".format(letters_to_exclude))

	# Now that we have GREEN and YELLOW letters, putting them together to match our word list (english_words_set)
	word_regex = ""
	for key, value in sorted(word.items()):
		if value == "":
			word_regex += "."
		else:
			word_regex += value

	#word_checker = re.compile('{}'.format(word_regex))

	string = ''.join(english_words_set)

	temp_match = re.findall(r"{}".format(word_regex), string)
	partial_match = []
	full_match = []


	# Stackoverflow Users Sven Marnach, Asclepius, and fantabolous - many thanks!
	# https://stackoverflow.com/questions/4843158/how-to-check-if-a-string-is-a-substring-of-items-in-a-list-of-strings
	if letters_to_use != False:
		temp = [m for m in temp_match if any(l in m for l in letters_to_use)]
		for t in temp:
			partial_match.append(t)
	else:
		partial_match = temp_match.copy()

	if letters_to_exclude != False:
		for p in partial_match:
			if not any(e in p for e in letters_to_exclude):
				full_match.append(p)
	else:
		full_match = partial_match.copy()

	full_match = list(set(full_match))
		
	print("Matches (no yellow):\n{}\nlen:{}".format(temp_match, len(temp_match)))
	print("Matches:\n{}\nlen:{}".format(full_match, len(full_match)))


main()
