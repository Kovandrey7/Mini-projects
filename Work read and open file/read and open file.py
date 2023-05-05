from pprint import pprint


def make_cook_book(name_file):
    cook_book = {}
    with open(name_file, encoding="utf-8") as file:
        for line in file:
            dish = line.strip()
            ingredient_count = int(file.readline())
            data_about_ingredients = []
            for _ in range(ingredient_count):
                ingredient_info = file.readline().strip()
                ingredient_name, quantity, measure = ingredient_info.split(" | ")
                data_about_ingredients.append(
                    {"ingredient_name": ingredient_name,
                     "quantity": int(quantity),
                     "measure": measure}
                )
            cook_book[dish] = data_about_ingredients
            file.readline()
    return cook_book


def get_shop_list_by_dishes(dishes: list, person_count=1):
    cook_book = make_cook_book("recipe.txt")
    list_for_shop = {}
    for dish in dishes:
        for ingredients in cook_book.get(dish, []):
            ingredients_for_shop = ingredients["ingredient_name"]
            quantity_ingredients = ingredients["quantity"] * person_count
            measure_ingredients = ingredients["measure"]
            if ingredients_for_shop not in list_for_shop:
                list_for_shop[ingredients_for_shop] = {"quantity": quantity_ingredients, "measure": measure_ingredients}
            else:
                list_for_shop[ingredients_for_shop]["quantity"] += quantity_ingredients
    return list_for_shop


pprint(get_shop_list_by_dishes(["Омлет", "Фахитос"], 2), sort_dicts=False)

# Задание №3
file_list = ["1.txt", "2.txt", "3.txt"]
my_dict = {}
for file in file_list:
    with open(file, encoding="utf-8") as file_1:
        name_file = file
        count_string = len(file_1.readlines())
        my_dict[name_file] = count_string
sorted_keys = sorted(my_dict, key=my_dict.get)
sorted_dict = {}
for _ in sorted_keys:
    sorted_dict[_] = my_dict[_]
for file_name, counter_string in sorted_dict.items():
    with open(file_name, encoding="utf-8") as file_in_dict:
        file_in_dict = file_in_dict.read()
        with open("4.txt", "a", encoding='utf-8') as new_file:
            new_file.write(file_name)
            new_file.write("\n")
            new_file.write(str(counter_string))
            new_file.write("\n")
            new_file.write(file_in_dict)
            new_file.write("\n")
