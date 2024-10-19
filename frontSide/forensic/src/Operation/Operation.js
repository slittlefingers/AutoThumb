import React, { useState, useEffect } from 'react';
import Header from '../Operation/Header';
import Monitor from '../Operation/Monitor';
import axios from 'axios';
import Timeline from './Timeline';
import ActionDetail from './Actiondetail';
import io from 'socket.io-client';

const Operation = () => {
    const [screenshot, setScreenshot] = useState(''); // 存储当前显示的截图
    const [actions, setActions] = useState([]); // 存储 action 列表
    const [thinking, setThinking] = useState(''); // 存储 thinking 信息
    const [operation, setOperation] = useState(''); // 存储 operation 信息
    const [action, setAction] = useState(''); // 当前 action 的详细信息

  // 组件挂载时获取初始截图
  useEffect(() => {
    fetchScreenshot();
    create_operation();
    fetchActions();
    
    setTimeout(() => {
      startTask();
  }, 3000); // 3000 毫秒 = 3 秒
    

    const socket = io('http://localhost:5000',{
      transports: ['websocket'],
      reconnection: true, // 启用自动重连（默认启用）
        // reconnectionAttempts: Infinity, // 无限次重连，直到成功
        // reconnectionDelay: 1000, // 每次重连尝试之间的延迟时间为 1 秒
        // reconnectionDelayMax: 1000, // 最大延迟时间也是 1 秒
        // timeout: 20000, // 连接超时时间为 20 秒
        // autoConnect: true // 自动尝试连接
    });
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });
  
    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
    });
  
    socket.on('connect_error', (err) => {
      console.error('Connection Error:', err);
    });
    // 监听 operation 事件
    socket.on('operation', (data) => {
      const cleanedMessage = data.message.replace('[OPERATION]', '').trim();
      setOperation(cleanedMessage);
      console.log('Operation log:', data.message);

    });

    // 监听 thinking 事件
    socket.on('thinking', (data) => {
      const cleanedMessage = data.message.replace('[THINKING]', '').trim();
      setThinking(cleanedMessage);
      console.log('Thinking log:', data.message);
      fetchScreenshot();
      fetchActions();

    });

    // 监听 action 事件
    socket.on('action', (data) => {
      const cleanedMessage = data.message.replace('[ACTION]', '').trim();
      setAction(cleanedMessage);
      console.log('Action log:', data.message);
      
    });
    return () => {
      socket.disconnect();
    };

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
  const fetchActions = async () => {
    try {
    const databasePath=localStorage.getItem('databasePath');
    const response = await axios.post('http://localhost:5000/api/get-actions', {
    'databasePath': databasePath // 替换为实际的数据库路径
      });
      setActions(response.data);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  };

  // 启动任务的函数
  const startTask = async () => {
    try {
    const databasePath=localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/start-task', {
        'databasePath': databasePath // 替换为实际的数据库路径
      });
      console.log(response.data); // 确认任务已启动
    } catch (error) {
      console.error('Error starting task:', error);
    }
  };
  const create_operation = async () => {
    try {
    const databasePath=localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/create-operation', {
        'databasePath': databasePath // 替换为实际的数据库路径
      });
      console.log(response.data); // 确认任务已启动
    } catch (error) {
      console.error('Error creating operation:', error);
    }
  };

  
  // 坐标转换函数
  return (
<div className="min-h-screen bg-[#f8f8f6] grid grid-rows-[auto,1fr,auto]">
      {/* 顶部导航部分 */}
      <div className="w-full grid grid-cols-1 justify-items-center text-lg py-0 border-b">
        <Header></Header>
      </div>
      
      {/* 主体内容部分 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 items-left justify-items-center w-full mt-8 px-4">
        {/* 左侧内容 */}
        <div className="md:col-span-1 flex items-center justify-center w-full">
          <Monitor screenshot={screenshot}></Monitor>
        </div>
        <div className="md:col-span-1 flex items-center justify-center w-full">
            <Timeline steps={actions}></Timeline>
        </div>
        {/* 右侧内容 */}
        <div className="md:col-span-1 flex items-center justify-start w-full">
          <ActionDetail thinking={thinking} action={action} operation={operation}></ActionDetail>
        </div>
           
        
        
      </div>

</div>
  );
};

export default Operation;