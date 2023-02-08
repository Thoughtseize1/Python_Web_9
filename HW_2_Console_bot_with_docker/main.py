from console_func import parser_input
from classes import MY_BOOK, FILE_NAME
import sys


def main():
    try:
        MY_BOOK.load_contacts(FILE_NAME)
    except EOFError:
        print('Your book is empty. Write "Help" to see awaliable commands')

    while True:
        user_input = input("Enter the command:")
        handler, *args = parser_input(user_input)
        result = handler(*args)
        if result == "exit":
            MY_BOOK.save_contacts(FILE_NAME)
            break
        if result:
            print(result)


if __name__ == "__main__":
    main()
