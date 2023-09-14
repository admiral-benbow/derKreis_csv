"""Используем ТОЛЬКО стандартные библиотеки"""

import csv
import datetime
import time
from math import fabs


def datetime_conv(time_rec: str) -> datetime.datetime | None:
    """
    Конвертируем формат времени и даты из .csv таблицы - e.g. '18 августа 2022 г. 7:58:33.002 мсек'
    (а именно заменяем название месяца) для перевода в класс datetime.datetime
    """

    local_dict = {
        "января": "01",
        "февраля": "02",
        "марта": "03",
        "апреля": "04",
        "мая": "05",
        "июня": "06",
        "июля": "07",
        "августа": "08",
        "сентября": "09",
        "октября": "10",
        "ноября": "11",
        "декабря": "12",
    }

    try:
        time_list = time_rec.split()
        time_list[1] = local_dict.get(time_list[1])
        fixed_time_rec = " ".join(time_list)

        return datetime.datetime.strptime(fixed_time_rec, "%d %m %Y г. %H:%M:%S.%f мсек")
    except (TypeError, IndexError):
        return None


def aperture_diff_finder(start_time: str, end_time: str, aperture: int | float,
                         csv_table: str, found_table: str) -> None:
    """
    Ищем ряды, где есть отличия от апертуры. Решил допустить, что вводим такой же формат даты, что у нас в изначальном
    .csv (другого не дано). Если что, то можно будет более универсальный способ работы с форматом времени сделать
    :param start_time: начало диапазона времени
    :param end_time: конец диапазона времени
    :param aperture: апертура значений параметров
    :param csv_table: название таблицы, из которой берём данные
    :param found_table: название таблицы, куда сохраняем наши данные
    :return: None; вывод в консоль времени работы ф-ции и создание нового .csv файла с полученными значениями
    """
    func_start = time.time()

    start_time = datetime_conv(start_time)
    end_time = datetime_conv(end_time)

    if not start_time or not end_time:
        print("Неправильно введён формат даты и времени")
        return

    prev_row = None
    heads_flag = True

    with open(csv_table) as table:
        reader = csv.reader(table, delimiter=";")
        csv_headers = reader.__next__()    # пропускаем и сохраняем заголовки

        for row in reader:
            row_time = datetime_conv(row[1])
            if start_time <= row_time <= end_time:  # проверяем соответствие времени
                if not prev_row:
                    prev_row = row[2:]
                    continue

                for index, param in enumerate(row[2:]):     # итерируемся по параметрам ряда
                    if fabs(float(param.replace(",", ".")) - float(prev_row[index].replace(",", "."))) > aperture:
                        with open(found_table, "a", encoding="utf-8") as new_table:
                            writer = csv.writer(new_table, delimiter=";", lineterminator="\n")
                            if heads_flag:
                                writer.writerow(csv_headers)
                                heads_flag = False

                            writer.writerow(row)
                        break
                prev_row = row[2:]

    func_finish = time.time()
    print(f"Затраченное время на работу функции: {func_finish - func_start}")


if __name__ == '__main__':
    aperture_diff_finder(start_time='18 августа 2022 г. 7:58:32.002 мсек',
                         end_time='18 августа 2022 г. 10:48:54.008 мсек',
                         aperture=125,
                         csv_table="table.csv",
                         found_table="found_rows.csv")
    aperture_diff_finder(start_time='18 августа 2022 г. 7:58:32.002 мсек',
                         end_time=' dsa  dsa das  das',
                         aperture=125,
                         csv_table="table.csv",
                         found_table="found_rows.csv")
