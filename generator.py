import json

links = {}
for i in range(1, 239):
    for c in ("A", "B", "C"):
        links["http://farsight.org/sponsors/Pool{0}/t{1}.html".format(c, i)] = ["Automatic initialization"]

with open("database.json", "w") as f:
    f.write(json.dumps(links, indent=4))
