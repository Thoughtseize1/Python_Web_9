from abc import ABC, abstractmethod
from classes import MY_BOOK
from pyowm.commons.exceptions import NotFoundError


class PrintInfo(ABC):
    @abstractmethod
    def get_info(self, *args, **kwargs):
        pass


class PrintHello(PrintInfo):
    def get_info(self):
        return "Can I help you? Write something to me:) You can see the avaliable commands by 'help' command"


class PrintAvaliableCommands(PrintInfo):
    def get_info(self):
        return """
    Use "add" *name* *phone* to add new user.
    Use "change" *name* *phone* to change user\'s number.
    Use "show" or "show all" to see all adress book. 
    Use "exit" or "q" to exit from bot.
    Use "del" *user* or "delete" to delete user.
    Use "birthday" *user* *birthday* to add birthday to contact in format "DD-MM-YYY".
    Use "next" *user* if you want to know how mane days before birthday.
    Use "save" to save your contacts.
    Use "search" *name* to find user's info.
    """


class PrintAllBook(PrintInfo):
    def get_info(self):
        if self.items():
            print("YOUR CONTACTS BOOK:")
            for name, record in self.data.items():
                print(f"Name: {name}")
                print("Phones: " + ", ".join([phone.value for phone in record.phones]))
                if record.birthday:
                    print("Birthday:", record.birthday.value)
                print()
        else:
            print("The book is empty")


class PrintUserInfo(PrintInfo):
    def get_info(self, phones):
        return f"{self} : {phones}"


class PrintSearchResult(PrintInfo):
    def get_info(self, *args):
        records = self.search(args[0].capitalize())
        searched_records = " "
        for record in records:
            searched_records += f"{record.get_info()}\n"
        return searched_records


class PrintExitMessage(PrintInfo):
    def get_info(self):
        print("Good Bye!")
        return "exit"
