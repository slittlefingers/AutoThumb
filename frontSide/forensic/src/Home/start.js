import React from "react";
import { Link } from "react-router-dom"
const Start = ({ adbConnection, rootAuthority }) => {
    // 检查是否可以启用按钮
    const isButtonEnabled = adbConnection && rootAuthority;
  
    return (
      <div className="flex justify-start items-center">
        {isButtonEnabled ? (
          // 当两个状态都为 true 时，按钮可以点击并跳转
          <Link to="/setting">
            <button className="bg-black text-white px-8 py-2 rounded-full text-lg hover:bg-gray-800">
              Start
            </button>
          </Link>
        ) : (
          // 否则按钮变成灰色，不可点击
          <button
            className="bg-gray-400 text-white px-8 py-2 rounded-full text-lg cursor-not-allowed"
            disabled
          >
            Start
          </button>
        )}
      </div>
    );
  };
  
  export default Start;