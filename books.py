import json
import os

DATA_FILE = 'books.json'  # название json файла с книгами, который должен находиться в одной директории

# Загружаем данные с json файла
def load_data():
    if not os.path.exists(DATA_FILE):
        return []   # если файла не существует, вернём пустой список
    with open(DATA_FILE, 'r') as file:
        return json.load(file)  # открываем и грузим данные как json


# Сохраняем данные в файл как json
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)  #


# Генерация уникальных айдишников. Если удалить книгу, начнёт заполнять айдишники начиная с первого
def generate_id(data):
    return max((book['id'] for book in data), default=0) + 1


# Добавляем книгу. Просим ввод трёх полей
def add_book():
    title = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    year = input("Введите год издания книги: ")
    if not year.isdigit():  # проверка на ошибку
        print("Год издания должен быть числом.")
        return
    data = load_data()  # открываем файл
    data.append({'id': generate_id(data), 'title': title, 'author': author, 'year': int(year), 'status': 'в наличии'})  # записали данные из инпута в нужном json формате, изначально книга всегда в наличии
    save_data(data) # сохранили
    print(f"Книга '{title}' добавлена.")


# Удаление книг
def delete_book():
    book_id = input("Введите id книги для удаления: ")
    data = load_data()  # открыли файл
    for book in data:
        if book['id'] == int(book_id):
            data.remove(book)
            save_data(data) # перебрали файл, нашли совпадение по id, удалили файл
            print(f"Книга с id {book_id} удалена.")
            return
    print(f"Книга с id {book_id} не найдена.") # если не нашли, вышли из функции


# Поиск книг
def search_books():
    search_type = input("Искать по (title/author/year): ").strip().lower()  # сначала выбираем поле, по которому ищем книгу
    search_term = input("Введите поисковый запрос: ").strip().lower()  # вводим поисковый запрос
    if search_type not in ['title', 'author', 'year']:
        print("Неверный тип поиска.")  # проверяем на корректность ввода поля
        return
    data = load_data()  #  открыли файл
    found_books = [book for book in data if search_term in str(book[search_type]).lower()]  # заносим в список все книги, которые удовлетворяют запросу
    if found_books:
        for book in found_books:
            print(book)  # вывели списком все найденные книги
    else:
        print("Книги не найдены.")


# Вывод всех книг
def display_books():
    data = load_data()  # открыли файл
    if data:
        for book in data:
            print(book)  # перебрали файл и вывели поочерёдно
    else:
        print("Библиотека пуста.")


# Изменение статуса
def change_status():
    book_id = input("Введите id книги для изменения статуса: ")
    new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip().lower()
    if new_status not in ['в наличии', 'выдана']:  # проверим корректность ввода статуса
        print("Неверный статус.")
        return
    data = load_data()  # открыли файл
    for book in data:
        if book['id'] == int(book_id):  # перебираем файл и находим книгу по id
            book['status'] = new_status  # переназначаем поле status
            save_data(data)
            print(f"Статус книги с id {book_id} изменен на '{new_status}'.")
            return
    print(f"Книга с id {book_id} не найдена.")


# Основное приложение
def main():
    actions = {
        '1': add_book,
        '2': delete_book,
        '3': search_books,
        '4': display_books,
        '5': change_status,
    }  # словарь с возможными кейсами
    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Отображение всех книг")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")
        if choice == '6':
            break  # выбор 6 кейса закрывает приложение
        action = actions.get(choice)  # получаем функцию из словаря по выбору пользователя
        if action:
            action()  # вызываем эту функцию
        else:
            print("Неверный выбор, попробуйте еще раз.")


if __name__ == '__main__':
    main()
