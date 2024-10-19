
import Header from './Header';
import Reminder from './reminder';
import Monitor from './Monitor';
import Checker from './checker';
import Start from './start';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import styles from './Home.module.css';
const Home = () => {
  // 定义状态变量，用于存储后端返回的结果
  const [adbConnection, setAdbConnection] = useState(null);
  const [rootAuthority, setRootAuthority] = useState(null);

  // 定义提示信息
  const [adbErrorMessage, setAdbErrorMessage] = useState("");
  const [rootErrorMessage, setRootErrorMessage] = useState("");
  const api = axios.create({
      baseURL: 'http://localhost:5000', // 设置基础 URL
    });
  // 使用 useEffect 钩子来请求后端 API
  useEffect(() => {
      const checkStatus = async () => {
          try {
              // 发送请求到后端 API
              const response = await api.get("/api/check-status");
              // 假设后端返回 { adbConnection: true, rootAuthority: false }
              const { adbConnection, rootAuthority } = response.data;

              // 更新状态
              setAdbConnection(adbConnection);
              setRootAuthority(rootAuthority);

              // 根据状态更新提示信息
              if (!adbConnection) {
                  setAdbErrorMessage("Failed to connect ADB. Please check USB debugging and connection.");
              }
              if (!rootAuthority) {
                  setRootErrorMessage("Failed to obtain root authority. Please check if the phone is rooted.");
              }
          } catch (error) {
              console.error("Failed to fetch status:", error);
          }
      };

      checkStatus();
  }, []);

  return (
<div className="min-h-screen bg-[#f8f8f6] grid grid-rows-[auto,1fr,auto]">
      {/* 顶部导航部分 */}
      <div className="w-full grid grid-cols-1 justify-items-center text-lg py-0 border-b ">
        <Header></Header>
      </div>

      {/* 主体部分 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center justify-items-center w-full mt-8 px-4">
        {/* 左侧文字 */}
        <Reminder></Reminder>
      
        {/* 中间的手机图片 */}
        <div className="relative">
          <Monitor></Monitor>
        </div>

        {/* 右侧状态指示 */}
        <div >
          <Checker
                  adbConnection={adbConnection}
                  rootAuthority={rootAuthority}
                  adbErrorMessage={adbErrorMessage}
                  rootErrorMessage={rootErrorMessage}>
          </Checker>
        </div>
      </div>

      {/* 底部启动按钮 */}
      <div className="grid place-items-center mt-1">
        <Start
        adbConnection={adbConnection} 
        rootAuthority={rootAuthority} ></Start>
      </div>
      <div className="grid place-items-center mt-1 h-32"> {/* 设置固定高度的留白区域 */}
        {/* 这是一个留白的 div，没有内容 */}
      </div>
    </div>
    
  );
}

export default Home;
