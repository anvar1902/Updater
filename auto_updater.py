import wget
import requests
import os


class Updater:
    def __init__(self,
                current_version_str: str,
                repository_url: str,
                program_name: str = "main.exe",
                updater_name: str = "updater.exe",
                updater_repository: str = "https://github.com/anvar1902/Updater"
                ):
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
        print(f"Текущая версия программы: {self.CURRECT_VERSION_str}")

    def check_new_version(self):
        print("Проверка на наличие новой версии ожидайте...")

        try:
            latest_respone_url = requests.get(self.URL + "/releases/latest").url
            self.LATEST_VERSION_str = latest_respone_url.replace(self.URL + "/releases/tag/", '')
            self.LATEST_VERSION = list(map(int, self.LATEST_VERSION_str.split('.')))
            yn = ""
            for i in range(self.VERSION_LEN):
                if self.CURRECT_VERSION[i] + 1 <= self.LATEST_VERSION[i]:
                    print(f"Найдена новая версия: {self.LATEST_VERSION_str}")
                    yn = input("Хотите установить (Y/N)?: ").upper()

                    while yn != "Y" and yn != "N":
                        yn = input("Хотите установить (Y/N)?: ").upper()

                    if yn == "Y":
                        self.update_program()
                    return
            if yn == "":
                print("Последняя версия уже установлена")
                os.system("clear")
                os.system("cls")

        except Exception as Error:
            print("Ошибка проверки: \n", Error)
            print("Обратитесь за помощью к разработчику")

    def update_program(self):
        os.system("cls")
        os.system("clear")
        print("Начата установка новой версии...")

        try:
            print("Получение последней версии Апдейтера...")
            latest_updater_url = requests.get(self.UPDATER_REPOSITORY + "/releases/latest").url
            latest_updater_ver = latest_updater_url.replace("https://github.com/anvar1902/OrigonFish/releases/tag/", "")
            latest_updater_download_url = self.UPDATER_REPOSITORY.replace("tag", "download")
            print(f"Последняя версия Апдейтера: {latest_updater_ver}")

            print("Скачивание Апдейтера...")
            wget.download(latest_updater_download_url + f"/{self.UPDATER_NAME}")
            print(f"Апдейтер успешно скачан")

            print("Передаю инструкции Апдейтеру...")
            if os.path.exists("updater_settings.txt"): os.remove("updater_settings.txt")
            with open("updater_settings.txt", 'w') as file:
                lines = [self.LATEST_VERSION_str, self.URL, self.PROGRAM_NAME]
                file.writelines("%s\n" % line for line in lines)

            print("Запускаю Апдейтер...")
            os.startfile(self.UPDATER_NAME)
            os.close(1)
        except Exception as Error:
            print("Ошибка установки новой версии: \n", Error)
            print("Пожалуйста обратитесь к разработчику за помощью либо обновите програму сами")