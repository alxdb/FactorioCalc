import json
import random

recipe_data = json.load(open('data/recipes.json'))
recipe_variant = 'normal'

# class Item:
#     def __init__(self, name, recipes):
#         self.name = name
#         self.recipes = recipes


# class Recipe:
#     def __init__(self, name, results, energy, dependencies):
#         self.name = name
#         self.results = results
#         self.energy = energy
#         self.dependencies = dependencies


# class Dependency:
#     def __init__(self, item, amount):
#         self.item = item
#         self.amount = amount


recipes = []
for recipe_name in recipe_data:
    recipe = recipe_data[recipe_name]

    if recipe_variant in recipe.keys():
        recipe = recipe[recipe_variant]

    if 'result' in recipe.keys():
        results = [{'name': recipe['result'], 'amount': 1}]
    else:
        results = []
        for result in recipe['results']:
            results.append(
                {'name': result['name'], 'amount': result['amount']})

    if 'energy_required' in recipe.keys():
        energy = recipe['energy_required']
    else:
        energy = 0.5

    recipes.append({'Type': 'Recipe',
                    'name': recipe_name,
                    'results': results,
                    'energy': energy,
                    'dependencies': recipe['ingredients']})

items = dict()
for recipe in recipes:
    for result in recipe['results']:
        if result['name'] not in items.keys():
            items[result['name']] = {
                'Type': 'Item',
                'name': result['name'],
                'recipes': [recipe]}
        else:
            item = items[result['name']]
            item['recipes'].append(recipe)

for item in items.values():
    for recipe in item['recipes']:
        for index, dependency in enumerate(recipe['dependencies']):
            if isinstance(dependency, dict) and dependency.get('Type') is None:
                recipe['dependencies'][index] = {'Type': 'Dependency',
                                                 'item': items.get(dependency['name'],
                                                                   dependency['name']),
                                                 'amount': dependency['amount']}
            elif isinstance(dependency, list):
                recipe['dependencies'][index] = {'Type': 'Dependency',
                                                 'item': items.get(dependency[0], dependency[0]),
                                                 'amount': dependency[1]}


# fluids cause circular dependency
try:
    # item = random.choice(list(items.keys()))
    item = 'tank'
    f = open("res.json", "w+")
    json.dump(items.get(item), f, indent=4)
except ValueError as err:
    print(err)
    print("probably contains liquid: " + item)
