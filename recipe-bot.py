from asyncio import sleep
import discord
from discord.ext import commands
import api
import requests
import json
from keep_alive import keep_alive

recipe_id = {}
recipe_title = {}
title_list = []

client = commands.AutoShardedBot(commands.when_mentioned_or('.'))


@client.event
async def on_ready():
	print('You Are Now Logged In...')
 
# ============================================================================================
def fetch_data(user):
    try:
        default_response = requests.get("https://api.spoonacular.com/recipes/complexSearch?apiKey={}&query={}".format(api.recipe_api,user))
        json_data = json.loads(default_response.text)["results"]


        num = 0
        for data in json_data:
            num +=1
            ides = data["id"]
            title = data["title"]
            recipe_id["Id{}".format(num)] = ides
            recipe_title["Id{}".format(num)] = title


        num1 = 0
        for titles in recipe_title.values():
            num1 += 1
            title_list.append("{}) {}".format(num1, titles))
        return title_list

    except:
        return ".recipe command not working"


def fetch_recipe_by_id(id_user):
    try:
        if recipe_id and recipe_title == {}:
            print(recipe_id)
            print(recipe_title)
            return "Please First Run The Command $recipe pasta (Here pasta means your recipe base Ingredian)"
        else:
            user_id_recipe = "Id{}".format(id_user)
            id_recipe = recipe_id[user_id_recipe]
            id_response = requests.get("https://api.spoonacular.com/recipes/{}/information?apiKey={}&includeNutrition=false".format(id_recipe,api.recipe_api))
            id_json_data = json.loads(id_response.text)["spoonacularSourceUrl"]
            recipe_id.clear()
            recipe_title.clear()
            return id_json_data
    
    except:
        return "3).get_recipe command not working\nHere is what you can try:\n First use .recipe command with your base recipe Ingrediant(Ex: .recipe pasta)\n 2) Use .get_recipe 3 (Here 3 means the recipe number from the given list from Bot\n3) If nothing Works please Contact Us"


def help_deck():
    return "Commands:\n1) .random = To Get Random Recipe\n2) .recipe pasta = To get all Recipe with the base Ingrediant Pasta(Ex .recipe pasta, .recipe noodles ..etc\n3) .get_recipe = To select a recipe from the recipe list provided by bot (Ex: .get_recipe 3)\n4) .help_me = To get all avilable Commands"


def random_recipe():
    try:
        default_response = requests.get("https://api.spoonacular.com/recipes/random?apiKey={}".format(api.recipe_api))
        json_data = json.loads(default_response.text)["recipes"][0]["spoonacularSourceUrl"]
        return json_data
    
    except:
        return ".random command not working"

#===========================================================================

@client.command()
async def recipe(ctx, user):
	try:
		result = fetch_data(user)
		await ctx.send(result)
	except:
         pass


@client.command()
async def get_recipe(ctx, id_user):
	try:
		result = fetch_recipe_by_id(id_user)
		await ctx.send(result)
	except:
         pass
		

@client.command()
async def random(ctx):
	try:
		result = random_recipe()
		await ctx.send(result)
	except:
         pass
		

@client.command()
async def help_me(ctx):
	try:
         await ctx.send(help_deck())
	except:
         pass
         
keep_alive()
client.run(api.dicord_api)
