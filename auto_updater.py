import wget
import requests
import logging
import os
import io
import time

if not os.path.isdir("logs"): os.mkdir("logs")
autoupdater_logger = logging.getLogger(__name__.split('.')[-1])
autoupdater_logger.setLevel(logging.DEBUG)

log_handler = logging.FileHandler("logs/" + __name__.split('.')[-1] + ".log", mode='w')
log_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

log_handler.setFormatter(log_formatter)
autoupdater_logger.addHandler(log_handler)
autoupdater_logger.debug("Логгер запущен")


class Updater:
    def __init__(self,
                current_version_str: str,
                repository_url: str,
                program_name: str,
                updater_name: str = "updater.exe",
                updater_repository: str = "https://github.com/anvar1902/Updater"
                ):
        autoupdater_logger.info("Запущена инициализация настроек")
        try:
            self.CURRECT_VERSION_str = current_version_str
            self.CURRECT_VERSION = list(map(int, current_version_str.split('.')))
            self.LATEST_VERSION_str = None
            self.LATEST_VERSION = None
            self.VERSION_LEN = 3
            self.URL = repository_url
            self.PROGRAM_NAME = program_name
            self.UPDATER_NAME = updater_name
            self.UPDATER_REPOSITORY = updater_repository
            if os.path.exists(self.UPDATER_NAME): os.remove(self.UPDATER_NAME)

        except Exception as Error:
            print(f"Ошибка инициализации: \n{Error}")
            autoupdater_logger.error("Ошибка инициализации", exc_info=True)
            time.sleep(5)

        else:
            print("Инициализация прошла успешно")
            autoupdater_logger.info("Инициализация прошла успешно")
        print(f"Текущая версия программы: {self.CURRECT_VERSION_str}")
        time.sleep(1)

    def check_new_version(self):
        print("Проверка на наличие новой версии ожидайте...")
        autoupdater_logger.info("Запуск проверки на наличие новой версии")

        try:
            latest_respone_url = requests.get(self.URL + "/releases/latest").url
            self.LATEST_VERSION_str = latest_respone_url.replace(self.URL + "/releases/tag/", '')
            self.LATEST_VERSION = list(map(int, self.LATEST_VERSION_str.split('.')))
            yn = ""

            for i in range(self.VERSION_LEN):
                #print(self.CURRECT_VERSION[i] + 1 <= self.LATEST_VERSION[i], "\n", self.CURRECT_VERSION[i], self.LATEST_VERSION[i])
                if self.CURRECT_VERSION[i] + 1 <= self.LATEST_VERSION[i]:
                    print(f"Найдена новая версия: {self.LATEST_VERSION_str}")
                    autoupdater_logger.info(f"Найдена новая версия: {self.LATEST_VERSION_str}")
                    yn = input("Хотите установить (Y/N)?: ").upper()

                    while yn != "Y" and yn != "N":
                        autoupdater_logger.debug(f"Неверный ответ: {yn}")
                        yn = input("Хотите установить (Y/N)?: ").upper()

                    autoupdater_logger.debug(f"Ответ: {yn}")
                    if yn == "Y":
                        self.update_program()
                    return
                elif self.CURRECT_VERSION[i] + 1 != self.LATEST_VERSION[i]:
                    break

            if yn == "":
                print("Последняя версия уже установлена")
                autoupdater_logger.info("Последняя версия уже установлена")
                time.sleep(1)
                os.system("clear")
                os.system("cls")

        except Exception as Error:
            print("Ошибка проверки: \n", Error)
            print("Обратитесь за помощью к разработчику")
            autoupdater_logger.error("Ошибка проверки наличия обновления", exc_info=True)
            time.sleep(5)

    def update_program(self):
        os.system("cls")
        os.system("clear")
        print("Начата установка новой версии...")
        autoupdater_logger.info("Запуск процесса обновление программы")

        try:
            print("Получение последней версии Апдейтера...")
            latest_updater_url = requests.get(self.UPDATER_REPOSITORY + "/releases/latest/").url
            latest_updater_ver = latest_updater_url.replace("https://github.com/anvar1902/OrigonFish/releases/tag/", "")
            latest_updater_download_url = latest_updater_url.replace("tag", "download")
            print(f"Последняя версия Апдейтера: {latest_updater_ver}")
            autoupdater_logger.debug(f"Последняя версия Апдейтера: {latest_updater_ver}")

            print("Скачивание Апдейтера...")
            autoupdater_logger.info("Скачивание Апдейтера")
            wget.download(latest_updater_download_url + f"/{self.UPDATER_NAME}")
            autoupdater_logger.info("Апдейтер успешно скачан")
            print(f"Апдейтер успешно скачан")

            print("Сохранение инструкций для Апдейтера...")
            autoupdater_logger.info("Сохранение инструкций для Апдейтера")
            if os.path.exists("updater_settings.txt"): os.remove("updater_settings.txt")
            with io.open("updater_settings.txt", 'w') as file:
                lines = [self.LATEST_VERSION_str, self.URL, self.PROGRAM_NAME]
                file.writelines("%s\n" % line for line in lines)
            autoupdater_logger.info("Инструкции успешно сохранены")

            print("Запускаю Апдейтер...")
            autoupdater_logger.info("Запускаю Апдейтер")
            os.startfile(self.UPDATER_NAME, 'runas')
            autoupdater_logger.info("Апдейтер успешно запущен")
            os.close(1)

        except Exception as Error:
            print("Ошибка установки новой версии: \n", Error)
            print("Пожалуйста обратитесь к разработчику за помощью либо обновите программу сами")
            autoupdater_logger.error("Ошибка установки Апдейтера", exc_info=True)
            time.sleep(5)
