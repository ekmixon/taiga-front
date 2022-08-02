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
import click
from difflib import SequenceMatcher

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
DEFAULT_LOCALE_PATH = os.path.join(ROOT_PATH, "app/locales/taiga/locale-en.json")


def keywords(key, value):
    if key is not None:
        if not isinstance(value, dict):
            return [(".".join(key), value)]

        kws = []
        for item_key in value.keys():
            kws += keywords(key+[item_key], value[item_key])
        return kws

    if isinstance(value, dict):
        kws = []
        for item_key in value.keys():
            kws += keywords([item_key], value[item_key])
        return kws


@click.command()
@click.option('--threshold', default=1.0, help='Minimun similarity to show')
@click.option('--min-length', default=10, help='Minimun size of the string to show')
@click.option('--omit-identical', default=False, is_flag=True, help='Omit identical strings')
def verify_similarity(threshold, min_length, omit_identical):
    locales = json.load(open(DEFAULT_LOCALE_PATH))
    all_keywords = keywords(None, locales)
    already_shown_keys = set()

    for key1, value1 in all_keywords:
        for key2, value2 in all_keywords:
            if key1 == key2:
                continue
            if len(value1) < min_length and len(value2) < min_length:
                continue

            similarity = SequenceMatcher(None, value1, value2).ratio()
            if omit_identical and similarity == 1.0:
                continue

            if (
                similarity >= threshold
                and (key1, key2) not in already_shown_keys
            ):
                already_shown_keys.add((key1, key2))
                already_shown_keys.add((key2, key1))
                click.echo(
                    f"The keys {key1} and {key2} has a similarity of {similarity}\n - {value1}\n - {value2}"
                )

if __name__ == "__main__":
    verify_similarity()
