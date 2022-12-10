from addressbook_class import AddressBook, Record


"""
Бот помічник.
Працює з командами (help, hello, add, change, delete_user, user_add_phone, user_delete_phone, phone, show_all, 
good_bye, close, exit, .)
"""


PHONE_BOOK = AddressBook()


def input_error(func):
    """
    Обробник помилок
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return f"Wrong command."
        except KeyError:
            return f"KeyError"
        except IndexError:
            return f"Wrong index"
        except ValueError:
            return f"ValueError: Wrong enter."

    return wrapper


@input_error
def change_input(user_input):
    """
    Функція для обробки введених даних від користувача
    """
    new_input = user_input
    data = ''
    for key in USER_COMMANDS:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input)+1:]
            break
    if data:
        return handler(new_input)(data)
    return handler(new_input)()


def hello():
    return "How can I help you?"


@input_error
def add(data):
    """
    Функція для додавання нового номеру в телефонну книгу
    """
    name, phones = create_data(data)
    if name in PHONE_BOOK:
        return f"Цей контакт {name} вже використовується введіть інше ім`я"
    record = Record(name)
    record.add_phone(phones)
    PHONE_BOOK.add_record(record)
    return f"Запис ({name} : {phones}) успішно додано до словника"


@input_error
def create_data(data):
    """
    Розділяє вхідні дані - номер і телефон.
    """
    name, phones = data.strip().split(' ')

    if name.isnumeric():
        raise ValueError('Wrong name.')

    return name.title(), phones


@input_error
def change(data):
    """
    Функція для зміни існуючого номеру в телефонній книзі
    """
    name, number = data.strip().split(' ')
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    records = PHONE_BOOK[name]
    records.change_phone_record(number)
    return f"Запис ({name} : {number}) замінено в словнику"


def days_to_birthday(name):
    """
    Функція яка повертає кількість днів до наступного дня народження контакту.
    :return:
    """
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]
    result = record.days_to_birthday()

    if str(result) in "У контакта не задана дата народження.":
        return f"У контакта {name} не задана дата народження."

    return f"До дня народження {name} залишилось {result} днів."


def delete_user(name):
    """
    Функція видалення контакту.
    :param name:
    :return:
    """
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK.pop(name)
    return f"Запис ({record.return_record()}) видалено з словника."


@input_error
def user_add_birthday(data):
    """
    Функція для додавання дня народження до існуючого контакту.
    """
    name, birthday = data.strip().split(' ')
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]
    record.change_birthday_record(birthday)
    return f"Дата народження ({birthday}) додано до контакту {name}"


@input_error
def user_add_phone(data):
    """
    Функція для додавання номеру до існуючого контакту.
    """
    name, number = data.strip().split(' ')
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]
    record.add_phone(number)
    return f"Номер ({number}) додано до контакту {name}"


def user_delete_phone(name):
    """
    Функція для видалення номеру в існуючого контакту.
    """
    name = name.title()
    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"
    record = PHONE_BOOK[name]
    result = record.delete_phone_record(name)
    returns = f"У контакта немає номерів..."
    if result in returns:
        return returns
    return f"Номер телефону: {result}, видалено в контакта {name}"


def user_delete_birthday(name):
    """
    Функція для видалення дня народження у контакту.
    """
    name = name.strip()
    name = name.title()

    if name not in PHONE_BOOK:
        return f"{name} імя не знайдено в словнику"

    record = PHONE_BOOK[name]
    record.delete_birthday()
    return f"Дата народження видалено у контакту {name}"


def phone(name):
    """
    Функція повертає номер телефону з телефонної книги
    """
    name = name.title().strip()
    if not PHONE_BOOK.get_name_record(name):
        return f"{name} не знайдено в телефонній книзі"
    phones = PHONE_BOOK.get_name_record(name).return_record()
    return f"Інфомацію знайдено:\n{phones}"


def show_all():
    """
    Функція для відображення всієї телефонної книги
    """
    show_number = ""
    list_info = 1

    for lists in PHONE_BOOK.iterator():
        show_number += f"Сторінка {list_info}\n"

        for record in lists:
            show_number += f"{record.return_record()}\n"

        list_info += 1

    return show_number


def good_bye():
    return "Good Bye!"


def break_f():
    """
    Коли користувач введе щось інше крім команд повертається строка про неправильний ввід команди.
    """
    return f"Wrong enter... "


@input_error
def handler(commands):
    return USER_COMMANDS.get(commands, break_f)


def helps():
    return f"Команди на які відповідає помічник: \n"\
           "help\n"\
           "hello \n"\
           "add - (add name phone)\n"\
           "delete_user - (delete_user name)\n"\
           "change - (change name phone(+380995551122))\n"\
           "phone - (phone name)\n"\
           "user_add_phone - (user_add_phone name phone(+380995551122))\n"\
           "user_delete_phone - (user_delete_phone name)\n" \
           "user_add_birthday - (user_add_birthday 00.00.0000/д.м.р)\n" \
           "user_delete_birthday - (user_delete_birthday name)\n" \
           "days_to_birthday - (days_to_birthday name)\n"\
           "show_all\n"\
           "good_bye, close, exit, .\n"


USER_COMMANDS = {
    "hello": hello,
    "add": add,
    "change": change,
    "user_add_phone": user_add_phone,
    "user_delete_phone": user_delete_phone,
    "user_add_birthday": user_add_birthday,
    "user_delete_birthday": user_delete_birthday,
    "days_to_birthday": days_to_birthday,
    "delete_user": delete_user,
    "phone": phone,
    "show_all": show_all,
    "good_bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    ".": good_bye,
    "help": helps
}


def main():
    """
    Логіка роботи бота помічника
    """
    while True:
        user_input = input("Введіть будь ласка команду: (або використай команду help)\n")
        result = change_input(user_input)
        print(result)
        if result == "Good Bye!":
            break


if __name__ == "__main__":
    main()
