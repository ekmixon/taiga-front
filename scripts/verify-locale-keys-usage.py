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

import json
import os

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOCALE_PATH = os.path.join(ROOT_PATH, "app/locales/taiga/locale-en.json")
WHITELIST = [
    'ADMIN.PROJECT_VALUES_PRIORITIES.ACTION_ADD',
    'ADMIN.PROJECT_VALUES_SEVERITIES.ACTION_ADD',
    'ADMIN.PROJECT_VALUES_TYPES.ACTION_ADD',
    'HINTS.HINT1_TITLE',
    'HINTS.HINT1_TEXT',
    'HINTS.HINT2_TITLE',
    'HINTS.HINT2_TEXT',
    'HINTS.HINT3_TITLE',
    'HINTS.HINT3_TEXT',
    'HINTS.HINT4_TITLE',
    'HINTS.HINT4_TEXT',
]


def keywords(key, value):
    if key is not None:
        if not isinstance(value, dict):
            return [".".join(key)]

        kws = []
        for item_key in value.keys():
            kws += keywords(key+[item_key], value[item_key])
        return kws

    if isinstance(value, dict):
        kws = []
        for item_key in value.keys():
            kws += keywords([item_key], value[item_key])
        return kws


def read_file(path):
    with open(path) as fd:
        return fd.read()


def check_keyword(keyword, files_text):
    if keyword in WHITELIST:
        return True
    return any(text.find(keyword) != -1 for text in files_text)


def verify_keywords_usage():
    locales = json.load(open(DEFAULT_LOCALE_PATH))

    all_files = []
    for root, dirs, files in os.walk(os.path.join(ROOT_PATH, 'app')):
        json_and_jade_files = list(filter(lambda x: x.endswith('.coffee') or x.endswith('.jade'), files))
        json_and_jade_files = map(lambda x: os.path.join(root, x), json_and_jade_files)
        all_files += json_and_jade_files

    all_files_text = list(map(read_file, all_files))

    for keyword in keywords(None, locales):
        if not check_keyword(keyword, all_files_text):
            print(f"Keyword unused: {keyword}")


if __name__ == "__main__":
    verify_keywords_usage()
