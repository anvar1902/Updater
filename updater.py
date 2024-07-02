import wget
import logging
import time
import os
import ctypes
import io
import datetime
from sys import argv


updater_logger = logging.getLogger("updater")
updater_logger.setLevel(logging.DEBUG)

log_handler = logging.FileHandler("updater.log", mode='w')
log_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

log_handler.setFormatter(log_formatter)
updater_logger.addHandler(log_handler)

def backup_prog():
    if not os.path.isdir("backup_update"): os.mkdir("backup_update")
    os.rename(PROGRAM_PATH, BACKUP_PATH)

def recovery_backup_prog():
    os.rename(BACKUP_PATH, PROGRAM_PATH)

def end_program():
    time.sleep(5)
    updater_logger.info("Завершение обновление")
    while 1:
        try:
            os.startfile(PROGRAM_NAME)

        except OSError as Error:
            print(f"Ошибка запуска приложения: \n{Error}")
            updater_logger.error("Ошибка запуска приложения", exc_info=True)

            print("Попытка восстановление удалённой версии")
            updater_logger.info("Попытка восстановление удалённой версии")
            recovery_backup_prog()
            print("Повторный запуск приложения")
            updater_logger.info("Повторный запуск приложения")

        else:
            updater_logger.info("Запущена обновлённая программа")
            updater_logger.info("Удаление апдейтера")
            os.remove(argv[0])

def main():
    global PROGRAM_NAME, PROGRAM_PATH, BACKUP_PATH
    print("Начата установка новой версии ожидайте...")
    print(__file__)
    updater_logger.info("Начата установка новой версии ожидайте")



    try:
        with io.open("updater_settings.txt", 'r') as file:
            data = file.readlines()
        updater_logger.debug(f"Открыт файл updater_settings.txt и получена дата: {data}")

        os.remove("updater_settings.txt")
        updater_logger.debug("Удалён файл updater_settings.txt")

        LATEST_VERSION = data[0].replace("\n", "")
        URL = data[1].replace("\n", "")
        PROGRAM_NAME = data[2].replace("\n", "")
        updater_logger.info("Рассортирована дата")
        updater_logger.debug((LATEST_VERSION, URL, PROGRAM_NAME))
        PROGRAM_PATH = os.path.join(os.getcwd(), PROGRAM_NAME)
        BACKUP_PATH = os.path.join(os.getcwd(), f"backup_update\\{time.strftime("%d.%m.%Y-%H.%M")}_{PROGRAM_NAME}")
        print(PROGRAM_PATH, BACKUP_PATH)

        backup_prog()
        os.remove(PROGRAM_NAME)
        updater_logger.info("Удалена старая версия")
        wget.download(URL + f"/releases/download/{LATEST_VERSION}/{PROGRAM_NAME}")

    except Exception as Error:
        print(f"Не удалось установить новую версию программы: \n{Error}", )
        updater_logger.error("Ошибка установки", exc_info=True)

    else:
        print("Новая версия успешно установлена запуск приложения через 5 секунд...")
        updater_logger.info("Новая версия успешно установлена")

    end_program()

if __name__ == "__main__":
    main()
