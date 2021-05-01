import os
import json


def refresh():
    dic = {}
    for root, dirs, files in os.walk("assets/tones", topdown=False):
        for name in dirs:
            for root_, dirs_, files_ in os.walk("assets/tones/"+name, topdown=False):
                dic[name] = files_

    print(dic)
    with open('utils/notes.json', 'w') as json_file:
        json.dump(dic, json_file)


if __name__ == '__main__':
    refresh()
