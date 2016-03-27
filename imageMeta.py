import os
import sys
import codecs
import json
argv = sys.argv
try:
    index = argv.index("--") + 1
except:
    index = len(argv)

argv = argv[index:]
if(argv[0]):
	png = (argv[0])
# chunk generator
def chunk_iter(data):
    total_length = len(data)
    end = 4

    while(end + 8 < total_length):     
        length = int(codecs.encode(data[end + 4: end + 8], 'hex'), 16) # int.from_bytes(data[end + 4: end + 8], 'big')
        begin_chunk_type = end + 8
        begin_chunk_data = begin_chunk_type + 4
        end = begin_chunk_data + length

        yield (data[begin_chunk_type: begin_chunk_data],
               data[begin_chunk_data: end])
res = {}
with open(png, 'rb') as fobj:
    data = fobj.read()
    assert data[:8] == b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

    for chunk_type, chunk_data in chunk_iter(data):
        #print("chunk type: {}".format(chunk_type.decode()))
        if chunk_type == b'iTXt':
            print("")
        elif chunk_type == b'tEXt':
            nv = chunk_data.decode('iso-8859-1').split('\0')
            res[nv[0]] = nv[1]
    print(json.dumps(res, separators=(',',':')))
    