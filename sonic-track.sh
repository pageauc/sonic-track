#!/bin/bash
echo "INFO - $0 ver 0.91 written by Claude Pageau"
echo ""
if [ -z "$(pgrep -f sonic-pi)" ] ; then
  echo "INFO - run xauth list to find displays"
  xdisplay=$( xauth list $DISPLAY | grep unix:0 )
  echo "INFO - found display - $xdisplay"
  echo "INFO - adding display - $xdisplay"
  xauth add $xdisplay
  echo "INFO - export DISPLAY"
  export DISPLAY=:0
  echo "INFO - Starting /usr/bin/sonic-pi in background"
  /usr/bin/sonic-pi &
  echo "INFO - sonic-pi now running in background"
else
  echo "INFO - sonic-pi is already running"
fi

echo "INFO - starting sonic-track.py"
./sonic-track.py

