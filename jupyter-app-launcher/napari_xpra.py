from flask import Flask
from argparse import ArgumentParser
import time
import os 

parser = ArgumentParser()
parser.add_argument('--port', type = int, default = 8000)
args = parser.parse_args()

outfile = '/home/lead/log.txt'

cmd = f'echo Attempting to launch docker. Time is {time.time()} >> {outfile}'
os.system(cmd)

#Original docker image
#cmd = f'docker run --rm -p {args.port}:{args.port} -e XPRA_PORT={args.port} -e XPRA_EXIT_WITH_CLIENT="no" -v /home/lead/notebooks/:/data/ ghcr.io/napari/napari-xpra'
#Updated docker image
cmd = f'docker run --rm -p {args.port}:{args.port} -e XPRA_PORT={args.port} -e XPRA_EXIT_WITH_CLIENT="no" -v /home/lead/notebooks/:/data/ benlansdell/hub-napari-xpra:latest'
os.system(cmd)

#DISPLAY=":100"
#DISPLAY=f":{args.port}"
#XPRA_START="python3 -m napari"
#XPRA_EXIT_WITH_CLIENT="no"
#XPRA_XVFB_SCREEN="1920x1080x24+32"

#cmd = f"""
#xpra start \
#    --bind-tcp=0.0.0.0:{args.port} \
#    --html=on \
#    --start="{XPRA_START}" \
#    --exit-with-client="{XPRA_EXIT_WITH_CLIENT}" \
#    --daemon=no \
#    --xvfb="/usr/bin/Xvfb +extension Composite -screen 0 {XPRA_XVFB_SCREEN} -nolisten tcp -noreset" \
#    --pulseaudio=no \
#    --notifications=no \
#    --bell=no \
#    {DISPLAY}
#"""

#os.system(cmd)
