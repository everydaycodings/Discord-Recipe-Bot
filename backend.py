import requests
import json
import random
import api

api = api.recipe_api

recipe_id = {}
recipe_title = {}

def help_deck():
    print("Meal Type Examples: main course, dessert, appetizer\n salad, breakfast, soup, beverage, sauce ..etc")
    print()
    print()
    print("Base Ingredient Recipe: Pasta, noodles, cake, Donuts ..etc")

def fetch_data():
    print("I having Confusion Please Type $help")
    course = input("Enter the Meal Type: ")
    user = input("Enter the base Ingredient Recipe: ")
    global json_data
    default_response = requests.get("https://api.spoonacular.com/recipes/complexSearch?apiKey={}&query={}&type={}".format(api,user,course))
    #json_data = json.loads(response.text)["recipes"][0]["spoonacularSourceUrl"]
    json_data = json.loads(default_response.text)["results"]


def arrange_data_in_dict():
    global recipe_title 
    num = 0
    for data in json_data:
        num +=1
        ides = data["id"]
        title = data["title"]
        recipe_id["Id{}".format(num)] = ides
        recipe_title["Id{}".format(num)] = title

def recipe_titles():
    num1 = 0
    print("============ OPTIONS ===============")
    for titles in recipe_title.values():
        num1 += 1
        print ("{}) {}".format(num1, titles))



def fetch_recipe_by_id():
    user = input("Enter The Recipie Number: ")
    user_id_recipe = "Id{}".format(user)
    id_recipe = recipe_id[user_id_recipe]
    id_response = requests.get("https://api.spoonacular.com/recipes/{}/information?apiKey={}&includeNutrition=false".format(id_recipe,api))
    id_json_data = json.loads(id_response.text)["spoonacularSourceUrl"]
    print(id_json_data)


fetch_data()
arrange_data_in_dict()
recipe_titles()
fetch_recipe_by_id()