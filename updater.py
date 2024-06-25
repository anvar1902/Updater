import wget
import logging
import time
import os

logging.basicConfig(level=logging.INFO, filename=__name__, filemode='w')

def main():
    print("Начата установка новой версии ожидайте...")

    try:
        with open("updater_settings.txt", 'r') as file:
            data = file.readlines()

        os.remove("updater_settings.txt")
        LATEST_VERSION = data[0].replace("\n", "")
        URL = data[1].replace("\n", "")
        PROGRAM_NAME = data[2].replace("\n", "")

        os.remove(PROGRAM_NAME)
        wget.download(URL + f"/releases/download/{LATEST_VERSION}/{PROGRAM_NAME}")
        print("Новая версия успешно установлена запуск приложения через 5 секунд...")

    except Exception as Error:
        print('Не удалось установить новую версию программы пожалуйста обратитесь к разработчику за помощью либо обновите програму сами: ', Error)
        logging.error("Ошибка установки", exc_info=True)

    time.sleep(5)
    os.startfile(PROGRAM_NAME)
    os.close(1)

if __name__ == "__main__":
    main()
