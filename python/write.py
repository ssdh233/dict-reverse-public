from __future__ import unicode_literals
from writemdict import writemdict
import json
from string import Template
import lxml.html
import jaconv

# 需要和刚才使用的DICT_KEY一致
DICT_KEY = "en_en"
# 这个title会变成欧路词典上显示的词典名
title = "New Oxford American Dictionary"

dictionary = {}
words = []
with open('../_share/' + DICT_KEY + '_source.dict.json') as jsonFile:
    data = json.load(jsonFile)
    words.extend(data)
    print(len(words))

def sortFunc(word):
    return word["word"].lower()

# remove word starting from large letter.
words = list(filter(lambda x: x["word"] != "" and x["word"][0] > "Z", words))
print(len(words))

sorted(words, key=sortFunc)

print("Finished sorting")

count = 0
for word in words:
    count += 1
    if count % 1000 == 0:
        print("Finished " + str(count) + " words...")
    definationHtml = lxml.html.fromstring(word["definition"])
    alterText = jaconv.kata2hira(definationHtml.cssselect("span.hw")[0].text_content())
    dictionary[alterText + ": " + word["word"]] = "@@@link=" + word["word"]
    if word["word"] in dictionary:
        dictionary[word["word"]] += word["definition"]
    else:
        dictionary[word["word"]] = word["definition"]

print("wait, patiently")
writer = writemdict.MDictWriter(dictionary, title=title, description="")
outfile = open("../_share/" + DICT_KEY + "_dict.mdx", "wb")
writer.write(outfile)
outfile.close()