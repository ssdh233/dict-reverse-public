from struct import unpack
from zlib import decompress
import json
import re

# 需要把下面的文件路径改成你的MacOS上的Body.data的文件位置
filename = '/System/Library/Assets/com_apple_MobileAsset_DictionaryServices_dictionaryOSX/xxxxx.asset/AssetData/New Oxford American Dictionary.dictionary/Contents/Resources/Body.data'
# DICT_KEY可以随便起，之后转换mdx和写css文件的时候会用到
DICT_KEY = "en_en"

f = open(filename, 'rb')

def gen_entry():
    f.seek(0x40)
    limit = 0x40 + unpack('i', f.read(4))[0]
    f.seek(0x60)
    while f.tell()<limit:
        sz, = unpack('i', f.read(4))
        buf = decompress(f.read(sz)[8:])

        pos = 0
        while pos < len(buf):
            chunksize, = unpack('i', buf[pos:pos+4])
            pos += 4

            entry = buf[pos:pos+chunksize].decode()
            title = re.search('d:title="(.*?)"', entry).group(1)
            yield title, entry

            pos += chunksize

count = 0
result = []
with open('../_share/' + DICT_KEY + '_source.dict.json', 'w') as outfile:
    for word, definition in gen_entry():
        result.append({ "word": word, "definition": definition})
        count += 1
        if count % 1000 == 0:
            print("Finished " + str(count) + " words...")
    json.dump(result, outfile)
