from datetime import datetime
from collections import UserDict
import pickle


class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, count=5):
        pages = []
        i = 0
        for record in self.data.values():
            pages.append(record)
            i += 1
            if i == count:
                yield pages
                pages = []
                i = 0
            if pages:
                yield pages

    def load_contacts(self, file):
        try:
            with open(file, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            pass

    def remove_record(self, name: str):
        self.data.pop(name)

    def search(self, value):
        record_result = []
        for record in self.data.values():
            if value in record.name.value:
                record_result.append(record)
                continue
            for phone in record.phones:
                if value in phone.value:
                    record_result.append(record)
        if not record_result:
            raise ValueError("Contact does not exist")
        return record_result

    def save_contacts(self, file):
        with open(file, "wb") as fh:
            pickle.dump(self.data, fh)


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not value.isnumeric():
            raise ValueError("Phones are wrong")
        if len(value) < 10 or len(value) > 12:
            raise ValueError("Phone must have 10 symbols")
        self._value = value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today_is = datetime.now().date()
        birth_date = datetime.strptime(value, "%d-%m-%Y").date()
        if birth_date > today_is:
            raise ValueError("Wrong enter. Up to date")
        self._value = birth_date


class Record:
    def __init__(self, name, *phones, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None
        for phone in phones:
            self.add_phone(phone)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def del_phone(self, phone: str):
        for record_phone in self.phones:
            if record_phone.value == phone:
                self.phones.remove(record_phone)

    def edit_phone(self, old_phone, new_phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def get_days_to_next_birthday(self):
        if not self.birthday._value:
            raise ValueError("Please, add birthday firstly")
        today = datetime.now().date()
        next_birthday_year = today.year

        if (
            today.month >= self.birthday._value.month
            and today.day > self.birthday._value.day
        ):
            next_birthday_year += 1

        next_birthday = datetime(
            year=next_birthday_year,
            month=self.birthday._value.month,
            day=self.birthday._value.day,
        )
        return (next_birthday.date() - today).days

    def get_info(self):
        phone_number = ""
        birth_info = ""

        for phone in self.phones:
            phone_number += f"{phone.value}, "

        if self.birthday:
            birth_info = f"(Birthday: {self.birthday.value})"

        return f"{self.name.value.title()}: {phone_number[:-2]}; {birth_info}"


MY_BOOK = AdressBook()
FILE_NAME = "data_console_bot.bin"
