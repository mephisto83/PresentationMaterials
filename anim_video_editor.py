import os
import bpy
from bpy import context
import sys
argv = sys.argv
try:
    index = argv.index("--") + 1
except:
    index = len(argv)

argv = argv[index:]
print(argv)
if(argv[0]):
	relPath = argv[0]

if(argv[1]):
	count = int(argv[1])

if(argv[2]):
	relAudioPath = argv[2]

renderPath = "default"
if(argv[3]):
	renderPath = argv[3]+"_"
  # --> ['example', 'args', '123']
scene = context.scene

print("starting ")
#path = "./1/"
path =os.path.dirname(os.path.realpath(__file__))+relPath
path_audio =os.path.dirname(os.path.realpath(__file__))+relAudioPath
files = os.listdir(path)
files.sort()
_scene = bpy.data.scenes[0]
_scene.render.resolution_x = 1920
_scene.render.resolution_y = 1080
_scene.render.resolution_percentage = 100


_scene.render.image_settings.file_format = 'H264'
_scene.render.filepath = "//output/" + renderPath
_scene.render.ffmpeg.audio_codec = 'MP3'
_scene.render.ffmpeg.audio_bitrate = 350

print(files[0])
# create the sequencer data
scene.sequence_editor_create()
filepath = os.path.join(path, files[0])
print(filepath)

# bpy.context.area.type = "VIEW_3D"
seq = scene.sequence_editor.sequences.new_image(
        name="MyStrip",
        filepath=filepath,
        channel=1, frame_start=1)

# add the rest of the images.
for f in files[1:count]:
    seq.elements.append(f)

files_audio = os.listdir(path_audio)
filepath_audio = os.path.join(path_audio, files_audio[0])
print(filepath_audio)
scene.sequence_editor.sequences.new_sound(
        name="MyStrip",
        filepath=filepath_audio,
        channel=2, frame_start=1)
bpy.context.scene.frame_end = count

bpy.ops.render.render(animation=True) 

print("rendered")