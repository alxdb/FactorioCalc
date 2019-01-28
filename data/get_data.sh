#! /usr/bin/env sh

lua get_data.lua && \
python -m json.tool recipes.json > /tmp/json.pp && \
mv /tmp/json.pp recipes.json
