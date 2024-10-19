import React,{useEffect,useRef} from 'react';

const Timeline = ({ steps }) => {
  const timelineRef = useRef(null);
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
    <div   ref={timelineRef} className="container mx-auto w-full max-h-[80vh] overflow-y-auto">
          <div className="relative wrap overflow-hidden p-10 h-full">
            <div className="border-2 absolute border-opacity-20 border-gray-700 h-full" style={{ left: "50%" }}></div>

            {steps.map((item, index) => (
              <div
                key={index}
                className={`mb-8 flex justify-between items-center w-full ${index % 2 === 0 ? 'right-timeline' : 'flex-row-reverse left-timeline'}`}
              >
                <div className="order-1 w-5/12"></div>
                <div className={`z-20 flex items-center order-1 shadow-xl w-8 h-8 rounded-full ${getStatusColor(item.status)}`}>
                  <h1 className="mx-auto font-semibold text-lg text-white">
                    {getStatusCh(item.status)}
                  </h1>
                </div>
                <div className={`order-1 rounded-lg shadow-xl w-5/12 px-6 py-4 ${getStatusColor(item.status)}`}>
                  <h3 className="mb-3 font-bold text-gray-800 text-xl">ACTION_{item.action_id}</h3>
                  <p className="text-sm leading-snug tracking-wide text-gray-900 text-opacity-100">
                    {item.action_description}
                  </p>
                </div>
              </div>
            ))}

          </div>
         
        </div>
  );
};

// 状态颜色函数
const getStatusColor = (status) => {
  switch (status) {
    case 'completed':
      return 'bg-green-200';
    case 'not completed':
      return 'bg-red-200';
    default:
      return 'bg-gray-200';
  }
};

const getStatusCh = (status) => {
  switch (status) {
    case 'completed':
      return '✔';
    case 'not completed':
      return '✘';
    default:
      return 'W';
  }
};

export default Timeline;
