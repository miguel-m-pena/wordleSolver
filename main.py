import time
from nltk.corpus import words
from collections import Counter
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import copy


# Website class borrowed and adapted from https://github.com/Kubasinska/Wordle-Solver/blob/main/solver.py

class Website:
    def __init__(self):
        s = Service(os.getcwd() + '/chromedriver')
        op = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(service=s, options=op)
        self.browser.get('https://www.powerlanguage.co.uk/wordle/')
        time.sleep(1)
        self.background = self.browser.find_element(By.TAG_NAME, 'html')
        self.background.click()
        time.sleep(1)
        self.counter = 0

    def send_word_get_answer(self, word):
        self.background.send_keys(word)
        self.background.send_keys(Keys.ENTER)
        time.sleep(2)
        host = self.browser.find_element(By.TAG_NAME, "game-app")
        game = self.browser.execute_script("return arguments[0].shadowRoot.getElementById('game')",
                                           host)
        board = game.find_element(By.ID, "board")
        rows = self.browser.execute_script("return arguments[0].getElementsByTagName('game-row')",
                                           board)
        row = self.browser.execute_script("return arguments[0].shadowRoot.querySelector("
                                          "'.row').innerHTML",
                                          rows[self.counter])
        bs_text = BeautifulSoup(row, 'html.parser')
        results = {}
        pos = 0
        for word in bs_text.findAll('game-tile'):
            letter = word.get('letter')
            eval = word.get('evaluation')
            results[pos] = (letter, eval)
            pos += 1

        return self.counter - 1, results


def generate_starting_possibilities():
    word_list = words.raw('en').split("\n")
    five_letter_words = []
    first_char, second_char, third_char, fourth_char, fifth_char = [], [], [], [], []
    for word in word_list:
        if len(word) == 5:
            word = word.lower()
            five_letter_words.append(word)
            first_char.append(word[0])
            second_char.append(word[1])
            third_char.append(word[2])
            fourth_char.append(word[3])
            fifth_char.append(word[4])
    return (five_letter_words, Counter(first_char), Counter(second_char), Counter(third_char),
            Counter(fourth_char), Counter(fifth_char))


def guess(web, five_letter_words, first_letter_count, second_letter_count, third_letter_count, \
          fourth_letter_count, fifth_letter_count):
    for i in range(len(first_letter_count)):
        for j in range(len(second_letter_count)):
            for k in range(len(third_letter_count)):
                for l in range(len(fourth_letter_count)):
                    for m in range(len(fifth_letter_count)):
                        guess = first_letter_count.most_common()[i][0] + second_letter_count.most_common()[j][0] + \
                                third_letter_count.most_common()[k][0] + fourth_letter_count.most_common()[l][0] + \
                                fifth_letter_count.most_common()[m][0]
                        # print(guess)
                        if guess in five_letter_words:
                            output = web.send_word_get_answer(guess)
                        else:
                            continue

                        for value in output[1].values():
                            if None in value:
                                web.background.send_keys(Keys.BACKSPACE)
                                web.background.send_keys(Keys.BACKSPACE)
                                web.background.send_keys(Keys.BACKSPACE)
                                web.background.send_keys(Keys.BACKSPACE)
                                web.background.send_keys(Keys.BACKSPACE)
                                break
                            else:
                                web.counter += 1
                                print(output[1])
                                # print("fuck")
                                return output[1]


def update_info(five_letter_words, output):
    vals = []
    for value in output.values():
        vals.append(value[0])
    counted_vals = Counter(vals)
    updated_words = copy.deepcopy(five_letter_words)
    for key in output.keys():
        if counted_vals[output[key][0]] > 1:
            if output[key][1] == "correct":
                for word in five_letter_words:
                    if word[key] != output[key][0]:
                        updated_words.remove(word)
            elif output[key][1] == "present":
                for word in five_letter_words:
                    if word[key] == output[key][0]:
                        updated_words.remove(word)
                    if not (output[key][0] in word):
                        updated_words.remove(word)
            else:
                for word in five_letter_words:
                    if word[key] == output[key][0]:
                        updated_words.remove(word)
            five_letter_words = copy.deepcopy(updated_words)
        else:
            if output[key][1] == "absent":
                for word in five_letter_words:
                    if output[key][0] in word:
                        updated_words.remove(word)
            elif output[key][1] == "present":
                for word in five_letter_words:
                    if word[key] == output[key][0]:
                        updated_words.remove(word)
                    if not (output[key][0] in word):
                        updated_words.remove(word)
            elif output[key][1] == "correct":
                for word in five_letter_words:
                    if word[key] != output[key][0]:
                        updated_words.remove(word)
            five_letter_words = copy.deepcopy(updated_words)
    # print(f'Here {five_letter_words}')
    first_char, second_char, third_char, fourth_char, fifth_char = [], [], [], [], []
    for word in five_letter_words:
        first_char.append(word[0])
        second_char.append(word[1])
        third_char.append(word[2])
        fourth_char.append(word[3])
        fifth_char.append(word[4])
    """    total_letter_count = Counter(" ".join(five_letter_words))
    total_letter_count.pop(' ')"""
    return (five_letter_words, Counter(first_char), Counter(second_char), Counter(third_char),
            Counter(fourth_char), Counter(fifth_char))

def check_correct(output):
    return all("correct" == val[1] for val in output.values())

def play():
    web = Website()
    five_letter_words, first_letter_count, second_letter_count, third_letter_count, \
    fourth_letter_count, fifth_letter_count = generate_starting_possibilities()
    start_word = input("Enter a word. Use ! if you do not wish to enter a word.")
    if start_word == "!":
        output = guess(web, five_letter_words, first_letter_count, second_letter_count,
                       third_letter_count, \
                       fourth_letter_count, fifth_letter_count)
    else:
        output = web.send_word_get_answer(start_word)
        for value in output[1].values():
            if None in value:
                web.background.send_keys(Keys.BACKSPACE)
                web.background.send_keys(Keys.BACKSPACE)
                web.background.send_keys(Keys.BACKSPACE)
                web.background.send_keys(Keys.BACKSPACE)
                web.background.send_keys(Keys.BACKSPACE)
                print("Invalid word. Defaulting to optimal guessing.")
                output = guess(web, five_letter_words, first_letter_count, second_letter_count,
                               third_letter_count, \
                               fourth_letter_count, fifth_letter_count)
                break
            else:
                web.counter += 1
                print(output[1])
                output = output[1]
                break
    while (not check_correct(output)) and web.counter < 6:
        five_letter_words, first_letter_count, second_letter_count, third_letter_count, \
            fourth_letter_count, fifth_letter_count = update_info(five_letter_words, output)
        output = guess(web, five_letter_words, first_letter_count, second_letter_count,
                       third_letter_count, fourth_letter_count, fifth_letter_count)
    print("Congratulations!")
    time.sleep(3)
    web.browser.quit()


play()
