from random import randint

condition = 'Answer "yes" if number even otherwise answer "no".'


def is_even(number):
    return number % 2 == 0


def get_answer():
    question = randint(0, 100)
    if is_even(question) is True:
        answer = "yes"
    else:
        answer = "no"
    return question, answer
