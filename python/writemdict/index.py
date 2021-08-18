# TODO move this file out of this folder
from __future__ import unicode_literals
from writemdict import MDictWriter
import json
from string import Template

wordTemp = Template("<b>$type</b><br>$desc")

dictionary = {}
words = []
for index in range(0,13):
    with open('../../_share/output' + str(index) + '.json') as jsonFile:
        data = json.load(jsonFile)
        words.extend(data)

    print(len(words))

def sortFunc(word):
    return word["word"].lower()

words = list(filter(lambda x: x["word"] != "" and x["word"][0] > "Z", words))
print(len(words))

sorted(words, key=sortFunc)

print("Finished sorting")

for word in words:
    dictionary[word["word"]] = wordTemp.substitute({
        "type": word["type"],
        "desc": "<br/>".join(word["desc"])
    })

print("wait, patiently")
writer = MDictWriter(dictionary, title="New Oxford American Dictionary", description="")
outfile = open("../../_share/dictionary.mdx", "wb")
writer.write(outfile)
outfile.close()