import json
import collections

recipes = json.load(open('recipe_grab/recipes.json'))
recipe_difficulty = 'normal'

Dependency = collections.namedtuple('Dependency', 'recipe amount dependencies')
BaseDependency = collections.namedtuple('BaseDependency', 'recipe amount')

class Recipe:
    def __init__(self, name):
        self.name = name
        recipe = recipes[name]

        if 'ingredients' in recipe:
            self.dependencies = recipe['ingredients']
        else:
            self.dependencies = recipe[recipe_difficulty]['ingredients']

        if 'energy_required' in recipe:
            self.time = recipe['energy_required']
        else:
            self.time = 0.5

        if 'result-count' in recipe:
            self.results = recipe['result-count']
        else:
            self.results = 1

    def __repr__(self):
        return self.name

    def get_dependencies(self):
        for dependency in self.dependencies:
            if isinstance(dependency, list):
                name = dependency[0]
                amount = dependency[1]
            else:
                name = dependency['name']
                amount = dependency['amount']
            if name in recipes:
                recipe = Recipe(name)
                yield Dependency(recipe, amount, recipe.get_dependencies())
            else:
                yield BaseDependency(name, amount)


def print_deps(deps, level = 0):
    for d in deps:
        if isinstance(d, Dependency):
            print('\t' * level, d.recipe.name, d.recipe.time, d.amount)
            print_deps(d.dependencies, level + 1)
        else:
            print('\t' * level, d.recipe, d.amount)

print_deps(Recipe("cannon-shell").get_dependencies())
