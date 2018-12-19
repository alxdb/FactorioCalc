json = require "json"

factorio_recipes_path = os.getenv("HOME") .. "/.local/share/Steam/steamapps/common/Factorio/data/base/prototypes/recipe/"

files = {
    "ammo",
    "capsule",
    "demo-furnace-recipe",
    "demo-recipe",
    "demo-turret",
    "equipment",
    "fluid-recipe",
    "furnace-recipe",
    "inserter",
    "module",
    "recipe",
    "turret",
}

recipes = {}
data = {}
data["extend"] = function (data, t)
   for i,r in pairs(t) do
      local recipe = {}
      for k,v in pairs(r) do
         if k ~= "name" then
            recipe[k] = v
         end
      end
      recipes[r["name"]] = recipe
   end
end

for i, f in ipairs(files) do
   file = factorio_recipes_path .. f .. ".lua"
   dofile(file)
end

io.output("recipes.json")
io.write(json.encode(recipes))