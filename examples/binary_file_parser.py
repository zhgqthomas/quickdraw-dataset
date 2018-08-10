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

categories = ["aircraft carrier", "airplane", "alarm clock", "ambulance", "angel", "animal migration", "ant", "anvil", "apple", "arm", "asparagus", "axe", "backpack", "banana", "bandage", "barn", "baseball", "baseball bat", "basket", "basketball", "bat", "bathtub", "beach", "bear", "beard", "bed", "bee", "belt", "bench", "bicycle", "binoculars", "bird", "birthday cake", "blackberry", "blueberry", "book", "boomerang", "bottlecap", "bowtie", "bracelet", "brain", "bread", "bridge", "broccoli", "broom", "bucket", "bulldozer", "bus", "bush", "butterfly", "cactus", "cake", "calculator", "calendar", "camel", "camera", "camouflage", "campfire", "candle", "cannon", "canoe", "car", "carrot", "castle", "cat", "ceiling fan", "cello", "cell phone", "chair", "chandelier", "church", "circle", "clarinet", "clock", "cloud", "coffee cup", "compass", "computer", "cookie", "cooler", "couch", "cow", "crab", "crayon", "crocodile", "crown", "cruise ship", "cup", "diamond", "dishwasher", "diving board", "dog", "dolphin", "donut", "door", "dragon", "dresser", "drill", "drums", "duck", "dumbbell", "ear", "elbow", "elephant", "envelope", "eraser", "eye", "eyeglasses", "face", "fan", "feather", "fence", "finger", "fire hydrant", "fireplace", "firetruck", "fish", "flamingo", "flashlight", "flip flops", "floor lamp", "flower", "flying saucer", "foot", "fork", "frog", "frying pan", "garden", "garden hose", "giraffe", "goatee", "golf club", "grapes", "grass", "guitar", "hamburger", "hammer", "hand", "harp", "hat", "headphones", "hedgehog", "helicopter", "helmet", "hexagon", "hockey puck", "hockey stick", "horse", "hospital", "hot air balloon", "hot dog", "hot tub", "hourglass", "house", "house plant", "hurricane", "ice cream", "jacket", "jail", "kangaroo", "key", "keyboard", "knee", "knife", "ladder", "lantern", "laptop", "leaf", "leg", "light bulb", "lighter", "lighthouse", "lightning", "line", "lion", "lipstick", "lobster", "lollipop", "mailbox", "map", "marker", "matches", "megaphone", "mermaid", "microphone", "microwave", "monkey", "moon", "mosquito", "motorbike", "mountain", "mouse", "moustache", "mouth", "mug", "mushroom", "nail", "necklace", "nose", "ocean", "octagon", "octopus", "onion", "oven", "owl", "paintbrush", "paint can", "palm tree", "panda", "pants", "paper clip", "parachute", "parrot", "passport", "peanut", "pear", "peas", "pencil", "penguin", "piano", "pickup truck", "picture frame", "pig", "pillow", "pineapple", "pizza", "pliers", "police car", "pond", "pool", "popsicle", "postcard", "potato", "power outlet", "purse", "rabbit", "raccoon", "radio", "rain", "rainbow", "rake", "remote control", "rhinoceros", "rifle", "river", "roller coaster", "rollerskates", "sailboat", "sandwich", "saw", "saxophone", "school bus", "scissors", "scorpion", "screwdriver", "sea turtle", "see saw", "shark", "sheep", "shoe", "shorts", "shovel", "sink", "skateboard", "skull", "skyscraper", "sleeping bag", "smiley face", "snail", "snake", "snorkel", "snowflake", "snowman", "soccer ball", "sock", "speedboat", "spider", "spoon", "spreadsheet", "square", "squiggle", "squirrel", "stairs", "star", "steak", "stereo", "stethoscope", "stitches", "stop sign", "stove", "strawberry", "streetlight", "string bean", "submarine", "suitcase", "sun", "swan", "sweater", "swing set", "sword", "syringe", "table", "teapot", "teddy-bear", "telephone", "television", "tennis racquet", "tent", "The Eiffel Tower", "The Great Wall of China", "The Mona Lisa", "tiger", "toaster", "toe", "toilet", "tooth", "toothbrush", "toothpaste", "tornado", "tractor", "traffic light", "train", "tree", "triangle", "trombone", "truck", "trumpet", "t-shirt", "umbrella", "underwear", "van", "vase", "violin", "washing machine", "watermelon", "waterslide", "whale", "wheel", "windmill", "wine bottle", "wine glass", "wristwatch", "yoga", "zebra", "zigzag"]

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
    response = requests.post('https://cloud.minapp.com/oserve/v1/table/47547/record/', json=payload, headers=headers)
    print(response.text)

print('over')





