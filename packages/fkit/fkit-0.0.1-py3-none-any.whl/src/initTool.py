import os, json

template = {
    "name": "",
    "desc": "",
    "cmd": "",
    "id": "",
    "imageName": "",
    "inputs": [
        {
            "key": "",
            "label": "",
            "name": "*"
        }
    ],
    "outputs": [
        {
            "key": "",
            "label": "",
            "name": ""
        }
    ]
}


def initTool(name):
    template['name'] = name.strip()
    cur_path = os.getcwd()
    with open(cur_path + '/tool.json', 'w') as f:
        f.write(json.dumps(template, indent=4, ensure_ascii=False))
    os.mkdir(os.getcwd() + '/input')
    os.mkdir(os.getcwd() + '/output')
