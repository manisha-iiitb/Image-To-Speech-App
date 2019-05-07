import os
import codecs
from ctypes import CDLL
from ctypes import Structure,CFUNCTYPE,POINTER,byref
from ctypes import c_int,c_short,c_float,c_char_p,c_void_p
from flask import Flask,request,send_file
import json

app = Flask(__name__)

dhvani = CDLL("libdhvani.so.0")

# Define call back types
t_dhvani_synth_callback = CFUNCTYPE(c_int,c_int)
t_dhvani_audio_callback = CFUNCTYPE(c_int,POINTER(c_short),c_int)

# Unused structure to match original implementation
class dhvani_VOICE(Structure):
    pass

# dhvani_option structure mapping class
class dhvani_options(Structure):
    _fields_ = [("voice",POINTER(dhvani_VOICE)),
                ("pitch",c_float),
                ("tempo",c_float),
                ("rate",c_int),
                ("language",c_int),
                ("output_file_format",c_int),
                ("isPhonetic",c_int),
                ("speech_to_file",c_int),
                ("output_file_name",c_char_p),
                ("synth_callback_fn",POINTER(t_dhvani_synth_callback)),
                ("audio_callback_fn",(t_dhvani_audio_callback))]


# Define dhvani speech function
dhvani_say = dhvani.dhvani_say
dhvani_say.restype = c_int
dhvani_say.argtypes = [c_char_p,POINTER(dhvani_options)]

# dhvani_speak_file function
dhvani_speak_file = dhvani.dhvani_speak_file
dhvani_speak_file.restype = c_int
dhvani_speak_file.argtypes = [c_void_p,POINTER(dhvani_options)]

# fdopen function not related to dhvani but a C library function
# in stdio.h this is used to
fileopen = dhvani.fdopen
fileopen.restype = c_void_p
fileopen.argtypes = [c_int,c_char_p]

def dhvani_init():
    option = dhvani_options()
    option.language = -1
    option.isPhonetic = 0
    option.speech_to_file = 0
    option.pitch = 0.0
    option.tempo = 0
    option.rate = 16000
    dhvani.start_synthesizer()
    return option

def dhvani_close():
    dhvani.stop_synthesizer()
    
@app.route('/', methods = ['POST', 'GET'])
def text_to_speech(pitch=3.0, speed=50000):
    if request.method == 'POST':
      logdata = request.stream.read()
      y = json.loads(logdata)
      f= codecs.open("text.txt","w+", encoding='utf-8')
      f.write(y["username"])
      f.close()
      text = codecs.open("text.txt",encoding="utf-8").read()
      dh = dhvani_init()
      dh.rate = c_int(int(speed))
      dh.pitch = c_float(float(pitch))
      dh.speech_to_file = 0
      return_type = dhvani_say(c_char_p(text.encode("utf-8")),byref(dh))
      return "test"      
    elif request.method =='GET':  
      path_to_file = "I2S.mp3"

      return send_file(
          path_to_file, 
          mimetype="audio/mp3", 
          as_attachment=True, 
          attachment_filename="I2S.mp3")

if __name__ == "__main__":
    app.run(host='0.0.0.0')    
