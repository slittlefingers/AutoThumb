
// adb exec-out /data/local/tmp/screenrecord --output-format=h264 - | ffmpeg -i - -vcodec libx264 -preset ultrafast -tune zerolatency -g 30 -fflags nobuffer -flags low_delay -probesize 32 -analyzeduration 0 -bufsize 1M -f flv rtmp://localhost:1935/live/stream
// .\objs\srs.exe -c .\conf\srs.conf
import React from 'react';

// import flvjs from 'flv.js';

const Monitor = ({screenshot}) => {
  


  return (
    <div
      
      className="relative w-[350px] h-[700px]"
      
    
    >
      <img
        src={`http://localhost:5000${screenshot}`} 
        alt="Screenshot"
        className="absolute top-[2.5%] left-[-2%] w-[100%] h-[92%] object-contain "
        draggable="false" 
      />
      <img
        src="/phoneframe.png" 
        alt="Phone Frame"
        className="absolute top-[0%] left-[0%] w-[95%] h-[100%] object-contain pointer-events-none"
        draggable="false" 
      />
    </div>
  );
}

export default Monitor;