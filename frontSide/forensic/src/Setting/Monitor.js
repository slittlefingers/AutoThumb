
// adb exec-out /data/local/tmp/screenrecord --output-format=h264 - | ffmpeg -i - -vcodec libx264 -preset ultrafast -tune zerolatency -g 30 -fflags nobuffer -flags low_delay -probesize 32 -analyzeduration 0 -bufsize 1M -f flv rtmp://localhost:1935/live/stream
// .\objs\srs.exe -c .\conf\srs.conf
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
// import flvjs from 'flv.js';

function Monitor() {
  const [screenshot, setScreenshot] = useState(''); // 存储当前显示的截图
  const monitorRef = useRef(null); // 创建 ref 来获取组件的尺寸和位置

  const mouseStartInfo = useRef({ startX: 0, startY: 0, startTime: 0 });
  // 组件挂载时获取初始截图
  useEffect(() => {
    fetchScreenshot();
  }, []);

  // 获取截图的函数
  const fetchScreenshot = async () => {
    try {
      setTimeout(async () => {
        try {
          // 发送请求到后端获取截图的 URL
          const response = await axios.get('http://localhost:5000/api/screenshot');
          setScreenshot(`${response.data.screenshotUrl}?timestamp=${new Date().getTime()}`); // 添加时间戳
        } catch (error) {
          console.error('Error fetching screenshot inside setTimeout:', error);
        }
      }, 1000); // 延迟时间设为6000毫秒（6秒）
    } catch (error) {
      console.error('Error setting up delayed screenshot fetch:', error);
    }
  };

  // 坐标转换函数
  const convertCoordinates = (clientX, clientY) => {
    const monitorRect = monitorRef.current.getBoundingClientRect(); // 获取容器的尺寸和位置
    const containerLeft = monitorRect.left; // 容器左边界
    const containerTop = monitorRect.top; // 容器上边界
    const containerWidth = monitorRect.width; // 容器宽度
    const containerHeight = monitorRect.height; // 容器高度

    // 图片在容器中的显示尺寸和偏移量（按百分比计算）
    const imageLeftOffset = containerWidth * (-2 / 100); // left: -2%
    const imageTopOffset = containerHeight * (2.5 / 100); // top: 2.5%
    const imageDisplayWidth = containerWidth; // 图片实际显示的宽度
    const imageDisplayHeight = containerHeight * (92 / 100); // 图片实际显示的高度（h-92%）

    // 实际设备分辨率（需要替换为真实设备的宽高）
    const deviceWidth = 720;
    const deviceHeight = 1650;

    // 计算相对于图片左上角的坐标
    const relativeX = clientX - containerLeft - imageLeftOffset;
    const relativeY = clientY - containerTop - imageTopOffset;

    // 映射到设备坐标
    const convertedX = Math.floor(relativeX * (deviceWidth / imageDisplayWidth));
    const convertedY = Math.floor(relativeY * (deviceHeight / imageDisplayHeight));

    return { convertedX, convertedY };
  };

  // 点击事件处理函数
  const handleClick = async (event) => {
    console.log("handleclick")
    const { clientX, clientY } = event; // 获取点击位置
    const { convertedX, convertedY } = convertCoordinates(clientX, clientY); // 转换坐标

    try {
      // 将点击位置发送到后端进行操作
      await axios.post('http://localhost:5000/api/click', { x: convertedX, y: convertedY });
      // 获取操作后的最新截图
      fetchScreenshot();
    } catch (error) {
      console.error('Error handling click:', error);
    }
  };

  // 滑动事件处理函数
  const handleSwipe = async (startX, startY, endX, endY) => {
    console.log("handlswipe")
    const { convertedX: startXConverted, convertedY: startYConverted } = convertCoordinates(startX, startY);
    const { convertedX: endXConverted, convertedY: endYConverted } = convertCoordinates(endX, endY);

    try {
      // 将滑动操作发送到后端进行处理
      await axios.post('http://localhost:5000/api/swipe', {
        startX: startXConverted,
        startY: startYConverted,
        endX: endXConverted,
        endY: endYConverted,
      });
      // 获取操作后的最新截图
      fetchScreenshot();
    } catch (error) {
      console.error('Error handling swipe:', error);
    }
  };
  const isClick = (startX, startY, endX, endY, startTime, endTime) => {
    const distance = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2); // 计算拖拽距离
    const timeElapsed = endTime - startTime; // 计算时间差

    // 调试信息
    console.log(`Distance: ${distance}, Time Elapsed: ${timeElapsed}ms`);

    return distance < 20 && timeElapsed < 300; // 增大距离和时间的阈值
  };

  return (
    <div
      ref={monitorRef} // 绑定 ref
      className="relative w-[350px] h-[700px]"
      // onClick={handleClick}
      onMouseDown={(e) => {
        // 绑定鼠标按下事件，记录开始位置
        const { clientX, clientY } = e;
        mouseStartInfo.current.startX = clientX;
        mouseStartInfo.current.startY = clientY;
        mouseStartInfo.current.startTime = new Date().getTime();
      }}
      onMouseUp={(e) => {
        // 绑定鼠标释放事件，记录结束位置和时间
        const { clientX, clientY } = e;
        const endTime = new Date().getTime(); // 记录结束时间
        const { startX, startY, startTime } = mouseStartInfo.current;

        if (isClick(startX, startY, clientX, clientY, startTime, endTime)) {
          handleClick(e); // 如果是点击，调用 handleClick 函数
        } else {
          handleSwipe(startX, startY, clientX, clientY); // 如果是滑动，调用 handleSwipe 函数
        }
      }}
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