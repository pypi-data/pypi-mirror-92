#!/usr/bin/env python

"""Python implementation of Avro Phonetic in hindi.

-------------------------------------------------------------------------------
Copyright (C) 2016 Subrata Sarkar <subrotosarkar32@gmail.com>
modified by:- Subrata Sarkar <subrotosarkar32@gmail.com>
original by:- Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.
Copyright (C) 2013 Kaustav Das Modak <kaustav.dasmodak@yahoo.co.in.

This file is part of pyhinvrophonetic.

pyAvroPhonetic is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pyAvroPhonetic is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyhinavrophonetic.  If not, see <http://www.gnu.org/licenses/>.

"""


# Imports
import os
import json
import io

# Constants
# -- Path to current directory
BASE_PATH = os.path.dirname(__file__)
# -- path to avrodict.json
AVRO_DICT_FILE = os.path.abspath(os.path.join(BASE_PATH,
                                              "resources/avrodict.json"))
# -- Loads json data from avrodict.json
AVRO_DICT = json.load(io.open(AVRO_DICT_FILE, encoding='utf-8'))
# -- Shortcut to vowels
AVRO_VOWELS = set(AVRO_DICT['data']['vowel'])
# -- Shortcut to consonants
AVRO_CONSONANTS = set(AVRO_DICT['data']['consonant'])
# -- Shortcut to case-sensitives
AVRO_CASESENSITIVES = set(AVRO_DICT['data']['casesensitive'])
# -- Shortcut to number
AVRO_NUMBERS = set(AVRO_DICT['data']['number'])
