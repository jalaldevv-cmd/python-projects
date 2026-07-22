import random

letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "0123456789"
symbols = "!@#$%^&*"


def generate_password(length, password_bank):
    password = ""
    for _ in range(length):
        letter = random.choice(password_bank)
        password += letter

    return password


def main():
    length = int(input("How many password characters? "))
    num = input("Include numbers? (Y/N)")
    sym = input("Include symbols? (Y/N)")

    print("Starting to generate...")

    password_bank = letters

    if num.lower() == "y":
        password_bank += numbers

    if sym.lower() == "y":
        password_bank += symbols

    password = generate_password(length, password_bank)

    print("Generated Password:", password)


if __name__ == "__main__":
    main()
