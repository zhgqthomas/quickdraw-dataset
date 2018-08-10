# Copyright 2017 Google Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import struct
from struct import unpack
import json
import requests


def unpack_drawing(file_handle):
    key_id, = unpack('Q', file_handle.read(8))
    # countrycode, = unpack('2s', file_handle.read(2))
    # recognized, = unpack('b', file_handle.read(1))
    # timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    image = []
    for i in range(n_strokes):
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        x = list(unpack(fmt, file_handle.read(n_points)))
        y = list(unpack(fmt, file_handle.read(n_points)))
        image.append([x, y])

    return {
        'key_id': key_id,
        # 'countrycode': countrycode,
        # 'recognized': recognized,
        # 'timestamp': timestamp,
        'image': image
    }


def unpack_drawings(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield unpack_drawing(f)
            except struct.error:
                break

categories = []
fd = file("categories.txt", "r")
 
for line in fd.readlines():
    categories.append(line.split('\n')[0])
print(len(categories))

drawings = []
for drawing in unpack_drawings('chunk.0000.bin'):
    # do something with the drawing
    drawings.append(drawing)

for drawing in unpack_drawings('chunk.0001.bin'):
    # do something with the drawing
    drawings.append(drawing)
# print(drawings)
print(len(drawings))

final = []
for i in range(345):
    item = {
        'key_id': drawings[i]['key_id'],
        'drawing': drawings[i]['image'],
        'word': categories[i]
    }
    final.append(item)

config = []
fd = file("config.txt", "r")
for line in fd.readlines():
    config.append(line.split('\n')[0])
client_id = config[0]
client_secret = config[1]

payload = {'client_id': client_id, 'client_secret': client_secret}
response = requests.post('https://cloud.minapp.com/api/oauth2/hydrogen/openapi/authorize/', json=payload)
code = response.json()['code']
print(code)
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'code': code,
}
print(payload)
response = requests.post('https://cloud.minapp.com/api/oauth2/access_token/', data=payload)
print(response.text)

token = response.json()['access_token']
auth = 'Bearer ' + token
headers = {'Authorization': auth}
for i in range(345):
    payload = {
    'key_id': final[i]['key_id'],
    'data': json.dumps(final[i]['drawing']),
    'word': final[i]['word']
    }
    response = requests.post('https://cloud.minapp.com/oserve/v1/table/47520/record/', json=payload, headers=headers)
    print(response.text)

print('over')





