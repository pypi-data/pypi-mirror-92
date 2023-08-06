import prompt

number_of_attempts = 3


def flow_game(game):
    print("Welcome to the Brain Games!")
    name = prompt.string("May I have your name? ")
    print("Hello, " + name + "!")
    for i in range(number_of_attempts):
        question, correct_answer = game()
        print("Question: {}".format(question))
        answer = prompt.string("Your answer: ")
        if correct_answer == answer:
            print("Correct!")
        else:
            print("'{}' is wrong answer ;(. Correct answer was '{}'.".format(correct_answer, answer))
            print("Let`s try again, {}!".format(name))
            return
        print("Congratulations, {}!".format(name))
