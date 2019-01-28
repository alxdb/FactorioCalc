json = require "json"
factorio_path = os.getenv("HOME") .. "/.local/share/Steam/steamapps/common/Factorio/"

data = {}
function data.extend(target, new_data)
    for i,e in pairs(new_data) do
        local entry = {}
        for k,v in pairs(e) do
            if k ~= "name" then
                entry[k] = v
            end
        end
        target[e["name"]] = entry
    end
end

recipe_files = io.popen("ls -d -1 " .. factorio_path .. "data/base/prototypes/recipe/**"):lines()

for file in recipe_files do
    dofile(file)
end

io.output("recipes.json")
data.extend = nil
io.write(json.encode(data))
