#!/usr/bin/env python

# Copyright (C) 2014-present Taiga Agile LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import json

plugins = [
    json.load(open(f"./dist/plugins/{f}/{f}.json"))
    for f in os.listdir("./dist/plugins")
    if f != "packed"
]

js = ""
css = ""
for plugin in plugins:
    if "js" in plugin:
        js += open(f"./dist{plugin['js']}", "r").read()
        js += "\n";
        del plugin["js"]
    if "css" in plugin:
        css += open(f"./dist{plugin['css']}", "r").read()
        css += "\n";
        del plugin["css"]

os.makedirs("./dist/plugins/packed", exist_ok=True)

with open("./dist/plugins/packed/plugins.js", "w") as plugins_js_file:
    plugins_js_file.write(js)
with open("./dist/plugins/packed/plugins.css", "w") as plugins_css_file:
    plugins_css_file.write(css)
packedPlugin = {
    "isPack": True,
    "js": "/plugins/packed/plugins.js",
    "css": "/plugins/packed/plugins.css",
    "plugins": plugins
}

with open("./dist/plugins/packed/packed.json", "w") as plugins_json_file:
    json.dump(packedPlugin, plugins_json_file)
