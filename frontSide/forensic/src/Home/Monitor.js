
// adb exec-out /data/local/tmp/screenrecord --output-format=h264 - | ffmpeg -i - -vcodec libx264 -preset ultrafast -tune zerolatency -g 30 -fflags nobuffer -flags low_delay -probesize 32 -analyzeduration 0 -bufsize 1M -f flv rtmp://localhost:1935/live/stream
// .\objs\srs.exe -c .\conf\srs.conf
import React from 'react';
// import flvjs from 'flv.js';

function Monitor() {
  return (
    <div className="relative w-[350px] h-[700px]">
      <img
        src="/output.gif" 
        alt="Screenshot"
        className="absolute top-[10%] left-[14%] w-[80%] h-[80%] object-contain"
      />
      <img
        src="/phoneframe2.png" 
        alt="Phone Frame"
        className="absolute top-[%] left-[0%] w-[100%] h-[100%] object-contain pointer-events-none "
      />
    </div>
  );
}

export default Monitor;