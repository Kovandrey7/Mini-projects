import json
import requests
from datetime import datetime
from pprint import pprint as print
from tqdm import tqdm


'''Для корректной работы потребуется токен VK и Яндекс Диска'''

with open("tokens.txt", "r") as file_object:
    token_vk = file_object.readline().strip()
    token_yandex = file_object.readline().strip()


class VKApiClient:
    def __init__(self, token_vk: str = token_vk, api_version: str = "5.131", base_url: str = "https://api.vk.com"):
        self.token_vk = token_vk
        self.base_url = base_url
        self.api_version = api_version

    def general_params_vk(self):
        return {
            "access_token": self.token_vk,
            "v": self.api_version
        }

    def get_photos(self, vk_id: int):
        count = int(input("Введите количество фотографий: "))
        album_id = input("Выберите из представленного списка название альбома, который хотите получить "
                         "и введите его название:\n"
                         "wall - фотографии со стены;\n"
                         "profile - фотографии профиля;\n"
                         "saved - сохраненные фотографии. Возвращается только с ключом доступа пользователя.\n"
                         "Введите здесь: ")
        params = {
            "owner_id": vk_id,
            "album_id": album_id,
            "extended": "likes",
            "count": count
        }
        params.update(self.general_params_vk())
        res = requests.get(f"{self.base_url}/method/photos.get", params=params).json()
        return res["response"]["items"]

    def parsed_photo(self, photo_info: list):
        user_profile_photos = []

        for photo in photo_info:
            photo_dict = {}
            name_photo = str(photo["likes"]["count"])

            for user_photo in user_profile_photos:
                if user_photo["name"] == name_photo:
                    name_photo += f"({datetime.utcfromtimestamp(int(photo['date'])).strftime('%Y-%m-%d')})"

            photo_dict.setdefault("name", name_photo)
            photo_dict.setdefault("url", photo["sizes"][-1]["url"])
            photo_dict.setdefault("size", photo["sizes"][-1]["type"])
            user_profile_photos.append(photo_dict)

        return user_profile_photos


class YandexClient:
    def __init__(self):
        self.token_yadisk = token_yandex
        self.url = "https://cloud-api.yandex.net/v1/disk/"

    def get_headers_ya_disk(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token_yadisk}"
        }

    def create_folder(self, name_directory: str):
        method = "resources"
        headers = self.get_headers_ya_disk()
        param = {
            "path": f"/{name_directory}"
        }
        res = requests.put(self.url + method, headers=headers, params=param)
        status = res.status_code
        if status == 201:
            return res
        else:
            print("Ошибка при создании папки")

    def upload_ya_disk(self, files: list, name_directory: str):
        method = "resources/upload"
        data_json = []

        for file in tqdm(files, desc="Loading", ncols=100, colour="red"):
            headers = self.get_headers_ya_disk()
            param_for_upload = {
                "url": file["url"],
                "path": f"/{name_directory}/{file['name']}"
            }
            res = requests.post(self.url + method, headers=headers, params=param_for_upload)
            status = res.status_code
            data = {
                "file_name": f'{file["name"]}.jpg',
                "size": file["size"]
            }
            data_json.append(data)

        with open("data.json", "a") as json_file:
            json.dump(data_json, json_file, indent=4)

        if status < 400:
            print(f"Данные загружены в папку - '{name_directory}'")
        else:
            print("Ошибка при загрузке файлов")


def from_VK_in_Yandex_disk():
    id_vk = int(input("Введите id VK: "))
    new_folder = input("Введите название новой папки: ")
    vk_client = VKApiClient()
    json_photo = vk_client.get_photos(id_vk)
    parsed_photo = vk_client.parsed_photo(json_photo)

    yandex_client = YandexClient()
    yandex_client.create_folder(new_folder)
    yandex_client.upload_ya_disk(parsed_photo, new_folder)


from_VK_in_Yandex_disk()
