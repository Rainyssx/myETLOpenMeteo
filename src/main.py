from GetDataFunction import getDatafromOpenMeteo, outputinFiletoCsv , outputFiletoDB , is_valid_date_format
import os
def main( latitude , longitude, start_date, end_date , path = "/home/pavel/Рабочий стол/", nameFile = "Data" , form = "DB"):
    try:
        data = getDatafromOpenMeteo(latitude = latitude, longitude = longitude,start_date = start_date, end_date = end_date)
    except ValueError as ve:
        print(f"Ошибка при получении данных c API {ve}")


    if form == "csv":
        try:
            outputinFiletoCsv(data,path = path, nameFile = nameFile)

        except ValueError as v:
            print(f"Ошибка при выгрузке данных в csv")

    else:
        try:
            outputFiletoDB(data)

        except ValueError as v:
            print(f"Ошибка при выгрузке данных в DB")



if __name__ == "__main__":

    print("При пустых или неверно введенных longitude или latitude будут по умолчанию выставлены latitude = 55, longitude = 83")
    longitude = input("Введите longitude - координата долготы места данных погоды: ")
    latitude = input("Введите latitude - координата долготы места данных погоды: ")
    if not longitude.isnumeric() or not latitude.isnumeric():
        latitude = 55
        longitude = 83
        print("Неправильно введены latitude или longitude , выставлены по умолчанию latitude = 55, longitude = 83")
    else:
        latitude = float(latitude)
        longitude = float(longitude)
    form = input("Введите формат выгрузки данных: можно написать 'csv'. При любом другом вводе данные будут выгружены в бд:  ")

    nameFile = "Datacsv"
    if form == "csv":
        path = input("Введите путь сохранения csv файла: ").strip()

        # Если путь не указан, сохраняем в текущую папку
        if not path:
            path = os.getcwd()  # или os.path.expanduser("~") для домашней папки



        full_path = os.path.join(path, nameFile + ".csv")
        print(f"Файл будет сохранён по пути: {full_path}")

    else:
        path = ""

    print("Начальную и конечную даты можно оставить пустыми, тогда данные будут только за сегодня")
    print("Ввести дату в формате %Y-%m-%d Год полностью - месяц двумя цифрами и число двумя цифрами")

    start_date = input("Ввести начальную дату: ").strip()
    if start_date:
        if not is_valid_date_format(start_date):
            start_date = ""
            print("Неправильный формат даты")
    else:
        st_d = start_date.split("-")


    end_date = input("Ввести конечную дату: ").strip()
    if end_date:
        if not is_valid_date_format(end_date.strip()):
            end_date = ""
            print("Неправильный формат даты")

    main(latitude , longitude, start_date, end_date , path , nameFile  , form )

    print("Все выполнено, данные выгружены: ")

