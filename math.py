import random


def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*', '/'])

    if operation == '/':  # Ensure division results in whole numbers
        num1 = num1 * num2

    question = f"{num1} {operation} {num2}"
    answer = eval(question)
    return question, answer


def math_quiz():
    score = 0
    while True:
        question, correct_answer = generate_question()
        user_answer = input(f"Solve: {question} = ")

        try:
            if float(user_answer) == correct_answer:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer is {correct_answer}")
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        play_again = input("Do you want another question? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break

    print(f"Your final score: {score}")
    print("Thanks for playing!")


if __name__ == "__main__":
    math_quiz()
