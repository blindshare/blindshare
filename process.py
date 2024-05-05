import sys
import subprocess
import argparse
import json

### Global ############################################################################################################

file     = ""
out_file = ""
aud      = ""
width    = "0"
height   = "0"

mod = False
ac  = "qaac"
crf = "25"

#######################################################################################################################
parser = argparse.ArgumentParser()

parser.add_argument("-r", "--res", type=str, help="Overwrite resolution: [width]x[height] (e.g. 1920x1080)")
parser.add_argument("-c", "--crf", type=str, help="Overwrite the Constant-Rate-Factor (default crf=25)")
parser.add_argument("-fa", "--ffmpeg-audio", action="store_true", help="use ffmpeg instead of avisynth+qaac to de/encode audio")
parser.add_argument("-o", "--output", type=str, help="Out-Filename if different from Input. Specify full name + suffix")
parser.add_argument("file", nargs='?', help="File to process")

args = parser.parse_args()

if (args.res ):
  mod = True
  width = (args.res.split("x"))[0]
  height = (args.res.split("x"))[1]

if (args.ffmpeg_audio ):
  ac = "ffmpeg"
  
if (args.crf ):
  crf = args.crf

if (args.output ):
  out_file = args.output

if (args.file ):
  file = (args.file).strip("./")
else:
  print("No file specified. Exiting")
  sys.exit(0)
  
#######################################################################################################################

mediainfo   = "C:\\Program Files (x86)\\Video Tools\\MediaInfo_CLI_24.03_Windows_x64\\mediainfo.exe"
avs2pipemod = "C:\\Program Files (x86)\\Video Tools\\avs2pipemod-1.1.1\\avs2pipemod64.exe"
qaac        = "C:\\Program Files (x86)\\Video Tools\\qaac_2.67\\x64\\qaac64.exe"
x265        = "C:\\Program Files\\x265\\x265-3.5_110.exe"
ffmpeg      = "C:\\Program Files (x86)\\Video Tools\\ffmpeg\\ffmpeg.exe"

# cmd = "--Output=\"Video;x %Width%\\ny %Height%\\nfps %FrameRate%\""
# This reduced output doesn't work as python does not pass the argument correctly to mediainfo - for unaccountable reasons!
# It works perfectly on CLI but not within python code. So the easiest way was to use JSON

### Get Infos #########################################################################################################

t_file = file[:-4]
process = subprocess.Popen([mediainfo, "--Output=JSON", file], stdout=subprocess.PIPE)
output = process.communicate()
o = (str(output).replace("\\r\\n", "").replace("\\xc2\\xa9","c"))[3:-8]   # The JSON Decoder doesn't like the Copyright-Sign
jo = json.loads(o)
exit_code = process.wait()  

# print(jo)
  
if width == "0":
  width  = jo["media"]["track"][1]["Width"]
if height == "0":
  height = jo["media"]["track"][1]["Height"]
frate  = int(float(jo["media"]["track"][1]["FrameRate"]))
audio  = jo["media"]["track"][2]["Format"]

if (frate == 23):
  fnum = 24000
  fden = 1001
if (frate == 24):
  fnum = 24000
  fden = 1000
if (frate == 25):
  fnum = 25000
  fden = 1000
if (frate == 29):
  fnum = 30000
  fden = 1001
if (frate == 30):
  fnum = 30000
  fden = 1000
if (frate == 50):
  fnum = 50000
  fden = 1000
if (frate == 59):
  fnum = 60000
  fden = 1001
 
print("########################################################################################") 
print(file,width,height,fnum,fden,audio)
print("########################################################################################")

### demux aac if possible #############################################################################################

if audio == "AAC":
  outputfile = t_file + ".aac"
  aud = outputfile

  cmd = [ffmpeg, "-i", file, "-vn", "-c:a", "copy", outputfile]
  print(cmd)
  process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  process.communicate()

### convert audio if necessary ####

else:
  if ac == "qaac":
    aud = "01.mp4"
    lines = []
    with open("avs.template") as avstmpl:
      l = avstmpl.read()
      lines.append(l)
	  
    lines.append("LWLibAvAudioSource(\"" + file + "\")" )
    lines.append("return(last)" )

    with open("aud.avs", 'w') as audavs:
      audavs.write('\n'.join(str(l) for l in lines))

    cmd = [avs2pipemod, "-extwav=float", "aud.avs", "|", qaac, "--ignorelength", "--no-delay", "-q", "2", "-V", "91", "-", "-o", "01.mp4"]
    print(cmd)

  if ac == "ffmpeg":
    aud = "01.mp4"
    cmd = [ffmpeg, "-i", file, "-vn", "-c:a", "libfdk_aac", "-vbr", "1",  "01.mp4"] 
    print(cmd)
	
  process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
  process.communicate()
  
### re-compress video in HEVC #########################################################################################

lines = []
o_file = t_file + ".h265"
with open("avs.template") as avstmpl:
  l = avstmpl.read()
  lines.append(l)
	
lines.append("LWLibAvVideoSource(\"" + file + "\")" )
lines.append("prefetch(4)")
lines.append("dfttest(Sigma=2,tbsize=1,lsb=true)")
if mod:
  lines.append("Dither_resize16(" + width + "," + height + ")" )
lines.append("GradFun3(lsb=true, lsb_in=true, thr=0.4)")
lines.append("Dither_out()")
lines.append("return(last)" )

with open("01.avs", 'w') as vidavs:
  vidavs.write('\n'.join(str(l) for l in lines))
  
dim = width + "x" + height
spd = str(fnum) + "/" + str(fden)

cmd = [avs2pipemod, "-rawvideo", "01.avs", "|", x265, "--preset", "slower", "--crf", crf, "--psy-rd", "2.0", "--psy-rdoq" , "10.0", "--aq-mode", "2", "--me", "star", "--no-open-gop", "--no-open-gop", "--input-res", dim, "--input-depth", "16", "--fps", spd, "--output", o_file, "--input", "-"]
print(cmd)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.communicate()
 
### multiplex #########################################################################################################

num = fnum/fden
fps = "{:.4f}".format(num)

o_file = t_file + ".h265"

if (out_file == ""):
  out_file = t_file + " (HEVC).mp4"

cmd = [ffmpeg, "-i", o_file, "-i", aud, "-c:v", "copy", "-c:a", "copy", out_file] 
print(cmd)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.communicate()
