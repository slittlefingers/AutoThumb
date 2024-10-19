import React, { useEffect,useRef } from "react";

const LogViewer = () => {
  const timelineRef = useRef(null);
  const list = [
    { action1: "action_name1", action_description: "action_description1", status: "success" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name1", action_description: "action_description1", status: "success" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name1", action_description: "action_description1", status: "success" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name1", action_description: "action_description1", status: "success" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
    { action1: "action_name2", action_description: "action_description2", status: "failed" },
  ];
  useEffect(() => {
    const handleWheel = (event) => {
      if (timelineRef.current) {
        event.preventDefault(); // 防止页面整体滚动
        timelineRef.current.scrollBy({
          top: event.deltaY, // 根据鼠标滚动方向上下移动
          behavior: "smooth",
        });
      }
    };

    const timelineElement = timelineRef.current;
    if (timelineElement) {
      timelineElement.addEventListener("wheel", handleWheel);
    }

    // 清理事件监听器
    return () => {
      if (timelineElement) {
        timelineElement.removeEventListener("wheel", handleWheel);
      }
    };
  }, []);
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-5 items-left justify-items-center w-full mt-8 px-4">
      {/* 左侧内容 */}
      <div className="md:col-span-1 flex items-center justify-center w-full">
        {/* <Monitor screenshot={screenshot}></Monitor> */}
      </div>

      {/* 中间时间轴 */}
      <div className="md:col-span-1 flex items-center justify-center w-full">
        <div   ref={timelineRef} className="container mx-auto w-full max-h-[80vh] overflow-y-auto">
          <div className="relative wrap overflow-hidden p-10 h-full">
            <div className="border-2 absolute border-opacity-20 border-gray-700 h-full" style={{ left: "50%" }}></div>

            {list.map((item, index) => (
              <div
                key={index}
                className={`mb-8 flex justify-between items-center w-full ${index % 2 === 0 ? 'right-timeline' : 'flex-row-reverse left-timeline'}`}
              >
                <div className="order-1 w-5/12"></div>
                <div className={`z-20 flex items-center order-1 shadow-xl w-8 h-8 rounded-full ${item.status === "success" ? "bg-green-500" : "bg-red-500"}`}>
                  <h1 className="mx-auto font-semibold text-lg text-white">
                    {item.status === "success" ? "✔" : "✘"}
                  </h1>
                </div>
                <div className={`order-1 rounded-lg shadow-xl w-5/12 px-6 py-4 ${item.status === "success" ? "bg-green-200" : "bg-red-200"}`}>
                  <h3 className="mb-3 font-bold text-gray-800 text-xl">{item.action1}</h3>
                  <p className="text-sm leading-snug tracking-wide text-gray-900 text-opacity-100">
                    {item.action_description}
                  </p>
                </div>
              </div>
            ))}

          </div>
        </div>
      </div>

      {/* 右侧内容 */}
      <div className="md:col-span-1  w-full pl-2 h-full">
      <div className="flex flex-col items-center justify-center w-full h-full">
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <img src="/action.png" alt="operation" class="w-1/6 h-1/8 pl-2" />
              <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                ACTION
              </h5>
              <p class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1">

              </p>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <img src="/operation.png" alt="operation" class="w-1/6 h-1/8" />
              <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                OPERATION
              </h5>
              <p class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1">
                Because it's about motivating the doers. Because I'm here to follow my
                dreams and inspire others.
              </p>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <img src="/thinking.png" alt="operation" class="w-1/6 h-1/8" />
              <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                THINKING
              </h5>
              <p class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1">
                Because it's about motivating the doers. Because I'm here to follow my
                dreams and inspire others.
              </p>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      </div>
      </div>
    </div>
  );
};

export default LogViewer;

//   const [logs, setLogs] = useState('');

//   useEffect(() => {
//     // 连接到 Flask-SocketIO 服务器
//     const socket = io('http://localhost:5000', {
//       transports: ['websocket'],
//     });

//     // 监听 'log' 事件并更新日志
//     socket.on('need be captured', (data) => {
//       setLogs(data.message);
//     });

//     socket.on('need be captured2', (data) => {
//       setLogs(data.message);
//       console.log("captured");
//     });
//     return () => {
//       socket.disconnect(); // 清理连接
//     };
//   }, []);

//   return (
//     <div>
//       <h1>Log Viewer</h1>
//       <p>{logs}</p>
//     </div>
//   );
// };


