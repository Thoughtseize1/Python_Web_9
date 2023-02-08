from classes import MY_BOOK, Record, FILE_NAME
from pyowm.commons.exceptions import NotFoundError
from pyowm import OWM
from user_interface import *

WEATHER_API = OWM("26ba7b8ee9b16c72a279e4b785a5ff02")


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This contact doesnt exist, please try again."
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return "This contact cannot be added, it exists already"
        except TypeError:
            return "Unknown command or parametrs, please try again."
        except NotFoundError:
            return "Unknown city, please try again."
        except UnboundLocalError:
            return "Unknown command or parametrs, please try again."

    return inner


@input_error
def add_user(args):
    name, phone = args
    if name not in MY_BOOK:
        MY_BOOK.add_record(Record(name, phone))
        return f"User {name} added with phone {phone}"
    MY_BOOK[name].add_phone(phone)
    return f"Adding a new tel {phone} for {name}"


@input_error
def birthday_func(args):
    name, date = args[0], args[1]
    record = MY_BOOK[name]
    record.add_birthday(date)
    return f"For {name} you added Birthday {date}"


@input_error
def change_phone(args):
    name, new_phone, old_phone = args
    old_phone = MY_BOOK.get(name)
    print(old_phone)
    MY_BOOK[name].edit_phone(old_phone, new_phone)
    return f"User {name} have a new phone number. Old number was {old_phone}"


@input_error
def delete_user(args):
    name = args[0]
    MY_BOOK.remove_record(name)
    return f"User with name {name} was deleted"


def exit(_):
    PrintExitMessage.get_info()
    return "exit"


def hello(_):
    return PrintHello.get_info()


@input_error
def next_birthday_func(name):
    record = MY_BOOK[name[0]]
    return f"Days to next {name[0]}'s birthday will be in {record.get_days_to_next_birthday()} days."


def save_func(_):
    MY_BOOK.save_contacts(FILE_NAME)
    print("Contacts saved")


def avaliable_comands(_):
    return PrintAvaliableCommands.get_info()


@input_error
def search_record(args):
    return PrintSearchResult.get_info(MY_BOOK, args[0])


@input_error
def show_all(_):
    return PrintAllBook.get_info(MY_BOOK)


@input_error
def show_number(args):
    user = args[0]
    phone = MY_BOOK[user]
    return PrintUserInfo.get_info(user, [tel.value for tel in phone.phones])


@input_error
def get_weather(args):
    city = args[0].capitalize()
    manager = WEATHER_API.weather_manager()
    observe = manager.weather_at_place(city)
    country = observe.to_dict()["location"]["country"]
    if country == "RU":
        return "!!! FUCK RUSSIA - WE NOT WORKS WITH TERRORISTS\nEnter the city again"
    elif city == "exit":
        return "BYE!"
    else:
        w = observe.weather
        temp = w.temperature("celsius")

    return f"""Hello, friend! Weather in {city}.
    Temperature is {temp} C.
    Feels like: {temp['feels_like']} C.
    Status: {w.status} """


HANDLERS = {
    "hello": hello,
    "hi": hello,
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "q": exit,
    "add": add_user,
    "change": change_phone,
    "show": show_all,
    "weather": get_weather,
    "show all": show_all,
    "phone": show_number,
    "help": avaliable_comands,
    "del": delete_user,
    "delete": delete_user,
    "search": search_record,
    "birthday": birthday_func,
    "next": next_birthday_func,
    "save": save_func,
}


def parser_input(user_input):
    command, *args = user_input.split()
    data = ""
    for key in HANDLERS:
        if user_input.strip().lower().startswith(key):
            command = key
            break
    try:
        handler = HANDLERS[command.lower()]
    except KeyError:

        def handler(_):
            return "Unknown command"

    return handler, args
