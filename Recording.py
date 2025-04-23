import os
from datetime import datetime
import subprocess

duration = 580000  # Recording duration in milliseconds

main = '/mnt/RNAiCam/RNAiVIDS'
if not os.path.exists(main):
    os.mkdir(main)
    
parent = '/mnt/RNAiCam/RNAiVIDS/CPB'
if not os.path.exists(parent):
    os.mkdir(parent)
    
date = datetime.now().strftime("%D").replace('/', '_')
outDir = os.path.join(parent, date)
if not os.path.exists(outDir):
    os.mkdir(outDir)

now = datetime.now()
filename = os.path.basename(os.path.expanduser('~')) + '_' + str(now).split('.')[0].replace(' ', '_').replace(':', '-')+'_ext1'

video_path = os.path.join(outDir, filename + '.h264')
image_path = os.path.join(outDir, filename + '.jpg')

# Record video in H.264 with reduced bitrate and framerate
subprocess.run([
    'rpicam-vid', '-t', str(duration), '--codec', 'h264', '--width', '4056', '--height', '3046','--framerate', '10', '--bitrate', '1000000',
    '-o', video_path
])

# Extract the first frame as an image using FFmpeg
subprocess.run([
    'ffmpeg', '-i', video_path, '-frames:v', '1', '-q:v', '2', image_path
])

print(f"Video saved: {video_path}")
print(f"First frame saved: {image_path}")

