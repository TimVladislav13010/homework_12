from collections import UserDict
from datetime import datetime
import re


"""
Класи бота помічника.

Record
AddressBook(UserDict)
Field
Name(Field)
Phone(Field)
Birthday(Field)
"""


class Record:
    """
    Клас Record, який відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання
    обов'язкового поля Name.

    При ініціалізації класу створюється ім'я класу Name, та список номерів телефоні, в який будуть записані номери
    телефонів класу Phone.
    """
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday("-")

    def add_birthday(self, birthday):
        self.birthday = (Birthday(birthday))

    def add_phone(self, phones):
        self.phones.append(Phone(phones))

    def return_record(self):

        phone_numbers = ""

        for phone in self.phones:
            phone_numbers += f"{phone.value}, "
        return f"{self.name.value}: {phone_numbers[:-2]}. ДН: {self.birthday.value}"

    def change_birthday_record(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    def change_phone_record(self, new_phone):
        """
        Метод для зміни номера телефона в існуючого контакту.

        1. Якщо в існуючого контакту немає номерів він додає номер телефону до списку класу Phone.
        2. Якщо номер один в списку то він замінюється на new_phone.
        3. Якщо номерів декілька в списку контакта замінити на той що вибере користувач за індексом.
        :param new_phone:
        :return:
        """
        if len(self.phones) == 0:
            self.phones.append(Phone(new_phone))

        if len(self.phones) == 1:
            self.phones[0].value = new_phone

        if len(self.phones) > 1:
            i = -1
            print(f"Виберіть номер телефону для видалення")
            for phone in self.phones:
                i += 1
                print(f"№  {i}  :  {phone.value}")
            inp_user = int(input(f"Введіть №..."))
            self.phones[inp_user] = Phone(new_phone)

    def days_to_birthday(self):
        """
        Метод для визначення скільки днів залишилось до ДН контакта.
        :return:
        """
        if self.birthday.value in "-":
            return f"У контакта не задана дата народження."
        day_today = datetime.today()
        day_birthday = datetime.strptime(str(self.birthday.value[:5]) + "." + str(day_today.year), "%d.%m.%Y")
        if day_today > day_birthday:
            day_birthday = datetime.strptime(self.birthday.value[:5] + "." + str(int(day_today.year + 1)), "%d.%m.%Y")
        days_to_birth = day_birthday - day_today
        return days_to_birth.days

    def delete_birthday(self):
        self.birthday = Birthday("-")

    def delete_phone_record(self, name):
        """
        Метод для видалення номеру в існуючого контакту.

        1. Якщо в існуючого контакту немає номерів повернення строки.
        2. Якщо номер один в списку то він видаляється.
        3. Якщо номерів декілька в списку контакта видаляється той що вибере користувач за індексом.
        :param name:
        :return:
        """
        if len(self.phones) == 0:
            return f"У контакта немає номерів..."

        elif len(self.phones) == 1:
            number = self.phones[0].value
            self.phones.pop(0)
            return f"{number}"

        elif len(self.phones) > 1:
            i = -1
            print(f"Виберіть номер телефону для видалення")
            for phone in self.phones:
                i += 1
                print(f"№  {i}  :  {phone.value}")
            inp_user = int(input(f"Введіть №..."))
            number = self.phones[inp_user].value
            self.phones.pop(inp_user)
            return f"{number}"

    def get_birthday(self):
        return self.birthday.value


class AddressBook(UserDict):
    """
    Клас книги контактів.

    Батьківський клас UserDict.
    """

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_records(self):
        return self.data

    def get_name_record(self, name) -> Record:
        return self.data.get(name)

    def iterator(self, n_count=10):
        """
        Метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає
        уявлення для N записів.
        :param n_count:
        :return:
        """
        i = 0
        info_list = list()

        for record in self.data.values():
            info_list.append(record)
            i += 1
            if i == n_count:
                yield info_list
                i = 0
                info_list = list()

        if info_list:
            yield info_list


class Field:
    """
    Батьківський клас для Name, Phone.
    """
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        """
        Гетер для повернення значення value.
        :return:
        """
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        Сетер для зміни значення value.
        :param new_value:
        :return:
        """
        self.__value = new_value


class Name(Field):
    """
    Ім'я контакта.
    """
    pass


class Phone(Field):
    """
    Номер телефону контакта.

    Додається до списку phones, який створюється при ініціалізації класу Record.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        """
        Гетер для повернення значення value.
        :return:
        """
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        Сетер для зміни значення номеру телефона.

        Перевизначений для батьківського класу Field
        :param new_value:
        :return:
        """
        if not re.fullmatch(r"\+\d{12}", new_value):
            raise ValueError("Невірний номер телефону, введіть телефон в форматі: (+380981112233)")
        self.__value = new_value


class Birthday(Field):
    """
    День народження контакта.

    Додається до списку birthday, який створюється при ініціалізації класу Record.
    """

    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        """
        Гетер для повернення значення value.
        :return:
        """
        return self.__value

    @value.setter
    def value(self, new_value):
        """
        Сетер для зміни значення ДН.

        Перевизначений для батьківського класу Field
        :param new_value:
        :return:
        """
        while True:
            if new_value in "--.--.----":
                self.__value = new_value
                break
            elif re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", new_value):
                days, months, years = new_value.split(".")
                if int(days) > 31 or int(months) > 12:
                    raise ValueError("невірний день або місяць.")
                self.__value = new_value
                break
            raise ValueError("не дата в форматі (00.00.0000/д.м.р).")
