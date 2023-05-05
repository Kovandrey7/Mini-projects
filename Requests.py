import requests
import datetime
import json
from pprint import pprint

#1
list_with_heroes = ["Hulk", "Captain America", "Thanos"]


def get_info_about_intelligence_at_hero(heroes_list: list):
    heroes_dict = {}
    url = "https://akabab.github.io/superhero-api/api/all.json"
    response = requests.get(url)
    if response.status_code != 200:
        return print("Некорректный запрос или ошибка на сервере")
    info_about_all_heroes = response.json()  # получаем всю инфу о героях в словаре
    for heroes_info in info_about_all_heroes:
        for heroes in heroes_list:
            if heroes_info["name"] == heroes:
                heroes_dict[heroes] = heroes_info["powerstats"]["intelligence"]
    hero_with_max_int = max(heroes_dict, key=lambda x: heroes_dict[x])
    result = f"Самый умный герой - {hero_with_max_int}. \nЕго интеллект: {heroes_dict[hero_with_max_int]}"
    return result


print(get_info_about_intelligence_at_hero(list_with_heroes))


#2
class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def upload(self, file_path: str, path_on_disk: str):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        param = {
            "path": f"{path_on_disk}",
            "overwrite": "True"
        }
        headers = self.get_headers()
        resp = requests.get(upload_url, headers=headers, params=param)
        if resp.status_code == 200:
            url_for_upload = resp.json()["href"]
            upload_final = requests.put(url_for_upload, data=open(file_path, "rb"))
            if upload_final.status_code == 201:
                return print("Файл загружен")


uploader = YaUploader(str(input("Введите токен: ")))

#3
def get_today():
    return int(datetime.datetime.now().timestamp())


def get_day_before_yesterday():
    return int((datetime.datetime.today() - datetime.timedelta(days=2)).timestamp())


def get_response(url: str, method: str, num: int, tagged: str):
    url = url
    method = method
    param = {

        "page": num,
        "pagesize": 100,
        "fromdate": get_day_before_yesterday(),
        "todate": get_today(),
        "order": "desc",
        "sort": "activity",
        "tagged": tagged,
        "site": "stackoverflow"
    }
    resp = requests.get(f"{url}{method}", params=param)
    if resp.status_code == 200:
        return resp.json()
    else:
        print("Ошибка запроса")


new_dict = {}
page = 1
while True:
    items = get_response("https://api.stackexchange.com", "/2.3/search", page, "python")
    for item in items["items"]:
        author = item["owner"]["display_name"]
        new_dict.setdefault(author, {})
        new_dict[author].update({"link": item["link"]})
        new_dict[author].update({"title": item["title"]})
    if items["has_more"]:
        page += 1
    else:
        break

with open("resp.json", "w") as out_file:
    json.dump(new_dict, out_file, indent=4)
