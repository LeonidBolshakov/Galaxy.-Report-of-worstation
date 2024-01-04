import re
import csv
from tkinter import filedialog
import os

# Шаблоны трёх первых полей в информационной строке
#    1. Имя файла.
#    2. Дата (ДД\ММ\ГГГГ) Время (ЧЧ:ММ)
#    3. Размер файла
#
PATTERN = [r'\w+.?\w+',  # Имя файла
           r'\d{2}\\\d{2}\\\d{4} \d{2}:\d{2}',  # ДД\ММ\ГГГГ ЧЧ:ММ
           r'[(\d{3}\s|\d{2}\s|\d{1}\s)]*']  # 999 999 999

#   Расширение выходного файла
NEW_EXTENTION = 'txt'


#   Замена расширения расширения в имени файла
#   Параметры:
#       1. Полное имя файла.
#       2. Новое расширение.
#   Результат
#       Полное имя файла с новым расширением
#
def change_file_extension(f, new_extension):
    file_name, file_extension = os.path.splitext(f)
    new_extension = new_extension.lstrip('.')
    return f"{file_name}.{new_extension}"


#   Выделение очередного поля и усечение входной строки на выделенное поле.
#       Если первое во входной строке поле, удовлетворяет шаблону,
#       то возвращается это поле и входная строка без этого поля.
#       Если поле не удовлетворяет шаблону - возвращается (None, None)
#   Параметры:
#       1. Шаблон регулярного выражнния для первого поля.
#       2. Строка, в которой ищется поле.
#   Результат:
#       1. Первое поле.
#       2. Строка без первого поля.
#           Если первое поле не удовлетворяет шаблону, то
#           (None, None)
#
def parsing(pattern: str, string: str) -> (str, str):
    str_strip = string.strip()
    result = re.match(pattern, str_strip)
    return (None, None) if result is None else (result.group(), str_strip[result.end():])


#   Обработка строки входного файла:
#   Поочерёдная проверка 3 первых полей строки на соответсвие шаблонам.
#   Если все поля удовлетворяют шаблонам, то они стновятся результатом работы функции.
#   В третьем поле (Размер) удаляются пробелы между цифрами.
#   Если, хотя бы одно поле не удовлетворяет шаблону результат функции:
#   (None, None, None)
#   Параметр.
#       Строка файла
#   Результат.
#      Три первых поля строки
#
def line_processing(line: str) -> ([str]):
    str_with_out_element = line.strip()
    elements = []
    for pattern in PATTERN:
        (element, str_with_out_element) = parsing(pattern, str_with_out_element)
        if element is None:
            break
        elements.append(element)
    else:
        elements[2] = elements[2].replace(' ', '')
        return elements
    return None


#   Чтение входного и запись преобразованного файла
#   Запрашиваем у пользователя путь на входной файл.
#   Читаем записи входного файла и только
#   информационные строки копим в списке.
#   Накопленные строки выводи в CSV файл.
#
def main():
    rows = []  # Список информационных строк входного файла
    input_filepath = filedialog.askopenfilename()
    with open(input_filepath, 'r', encoding='866') as file_input:
        for line in file_input:
            elements = line_processing(line)
            if elements is not None:
                rows.append(elements)

    output_filepath = change_file_extension(input_filepath, NEW_EXTENTION)
    with open(output_filepath, 'w', newline='') as file_output:
        writer = csv.writer(file_output, delimiter='\t')
        for row in rows:
            writer.writerow(row)


if __name__ == '__main__':
    main()
