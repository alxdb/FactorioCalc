import json

recipe_data = json.load(open('data/recipes.json'))
recipe_variant = 'normal'


class Item:
    def __init__(self, name, recipes):
        self.name = name
        self.recipes = recipes


class Recipe:
    def __init__(self, name, results, energy, dependencies):
        self.name = name
        self.results = results
        self.energy = energy
        self.dependencies = dependencies


class Dependency:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount


recipes = set()
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

    recipes.add(Recipe(recipe_name, results, energy, recipe['ingredients']))

items = dict()
for recipe in recipes:
    for result in recipe.results:
        if result['name'] not in items.keys():
            items[result['name']] = Item(result['name'], [recipe])
        else:
            item = items[result['name']]
            item.recipes.append(recipe)

for item in items.values():
    for recipe in item.recipes:
        for index, dependency in enumerate(recipe.dependencies):
            if isinstance(dependency, dict):
                recipe.dependencies[index] = Dependency(
                    items.get(dependency['name'], dependency['name']), dependency['amount'])
            elif isinstance(dependency, list):
                recipe.dependencies[index] = Dependency(
                    items.get(dependency[0], dependency[0]), dependency[1])

        for result in results:
            result = {'item': items.get(
                result['name'], result['name']), 'amount': result['amount']}

example = list(items.values())[0]

# broken
def itterate(obj, level=0):
    if isinstance(obj, str):
        return
    for entry in dir(obj):
        if not entry.startswith("__"):
            print('\t' * level + entry)
            itterate(entry, level + 1)

itterate(example)
