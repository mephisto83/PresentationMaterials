import os
import bpy
from bpy import context
import json
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
	renderPath = argv[3]+".avi"
  # --> ['example', 'args', '123']
image_mapping = None
if(argv[4]):
    image_mapping_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), argv[4])
    f = open(image_mapping_file, 'r')
    filecontents = f.read()
    image_mapping = json.loads(filecontents)
anim_settings = None
if(len(argv) > 5 and argv[5]):
    anim_settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), argv[5])
    f = open(anim_settings_file, 'r')
    filecontents = f.read()
    anim_settings = json.loads(filecontents)

audio_map_settings = None
if(argv[6]):
    audio_map_file = argv[6]
    f = open(audio_map_file, 'r')
    filecontents = f.read()
    audio_map_settings = json.loads(filecontents)
    audio_file_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "audio") #argv[7]

scene = context.scene
def findAudioName(array, id):
    for a in array:
        if a["id"] == id:
            return a["fileName"]
    raise Exception("can not find file")

print("starting ")
#path = "./1/"
path =  os.path.join(os.path.dirname(os.path.realpath(__file__)), relPath)
path_audio = os.path.join(os.path.dirname(os.path.realpath(__file__)), relAudioPath)
files = os.listdir(path)
files.sort()
_scene = bpy.data.scenes[0]
_scene.render.resolution_x = 1920
_scene.render.resolution_y = 1080
_scene.render.resolution_percentage = 100
bpy.context.scene.frame_end = count

_scene.render.image_settings.file_format = 'H264'
_scene.render.filepath =  os.path.join(os.path.dirname(os.path.realpath(__file__)),"output", renderPath) # os.path.join("output", renderPath)  os.path.join("output", renderPath)
_scene.render.ffmpeg.audio_codec = 'MP3'
_scene.render.ffmpeg.audio_bitrate = 350
channel = 1
scene.sequence_editor_create()
if audio_map_settings != None:
    audio_array = audio_map_settings["audio"]
    for audio_item in audio_array:
        audioFileName = findAudioName(audio_map_settings["resources"], audio_item["audioId"])
        if audioFileName != None:
            frame = int(audio_item["start"] * 30)
            print("audio_file_folder")
            print(audio_file_folder)
            filepath_audio = os.path.join(audio_file_folder, audioFileName)
            scene.sequence_editor.sequences.new_sound(name=audio_item["id"], filepath=filepath_audio, channel=channel, frame_start=frame)
            channel = (channel + 1) % 32
            
if anim_settings != None and "settings" in anim_settings:
    settings =  anim_settings["settings"]
    if "resolution_x" in settings:
        _scene.render.resolution_x = float(settings["resolution_x"])
    if "resolution_y" in settings:
        _scene.render.resolution_y = float(settings["resolution_y"])
    if "file_format" in settings:
        _scene.render.image_settings.file_format = settings["file_format"]
    if "audio_codec" in settings:
        _scene.render.image_settings.audio_codec = settings["audio_codec"]
    if "audio_bitrate" in settings:
        _scene.render.image_settings.audio_bitrate = float(settings["audio_bitrate"])

def getImageFromMap(imap, frame):
    for im in imap:
        if im["frame"] == frame:
            return im
    return None

print(files[0])
# create the sequencer data
filepath = os.path.join(path, files[0])
print(filepath)
if image_mapping != None and "renderedfilename" in image_mapping[0]:
    im = getImageFromMap(image_mapping, 1)
    seq = scene.sequence_editor.sequences.new_image(
            name="MyStrip",
            filepath= os.path.join(os.path.dirname(os.path.realpath(__file__)), relPath, im["renderedfilename"]+'.png') ,
            channel=1, frame_start=1)
    nextIm = getImageFromMap(image_mapping, 2)
    currentIm = 2
    while(nextIm):
        impath = nextIm["renderedfilename"]+'.png'
        seq.elements.append(impath)
        currentIm = currentIm + 1
        nextIm = getImageFromMap(image_mapping, currentIm)

else:
    # bpy.context.area.type = "VIEW_3D"
    seq = scene.sequence_editor.sequences.new_image(
            name="MyStrip",
            filepath=filepath,
            channel=1, frame_start=1)

    # add the rest of the images.
    if image_mapping == None:
        for f in files[1:count]:
            seq.elements.append(f)
    else:
        for mapping in image_mapping[1:]:
            count = mapping["frame"]
            image = mapping["image"]
            seq.elements.append(files[image])

files_audio = os.listdir(path_audio)
if len(files_audio) > 0:
    filepath_audio = os.path.join(path_audio, files_audio[0])
    print(filepath_audio)
    scene.sequence_editor.sequences.new_sound( name="MyStrip", filepath=filepath_audio, channel=2, frame_start=1)

bpy.context.scene.frame_end = count
bpy.ops.render.render(animation=True)

print("rendered")