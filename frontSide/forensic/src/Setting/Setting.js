import React from 'react';
import Header from '../Setting/Header';
import Monitor from '../Setting/Monitor';
import Table from '../Setting/table';
const Setting = () => {
  return (
    <div className="min-h-screen bg-[#f8f8f6] grid grid-rows-[auto,1fr,auto]">
      {/* 顶部导航部分 */}
      <div className="w-full grid grid-cols-1 justify-items-center text-lg py-0 border-b">
        <Header></Header>
      </div>

      {/* 主体内容部分 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-left justify-items-center w-full mt-8 px-4">
        {/* 左侧内容 */}
        <div className="flex items-center justify-center w-full">
          <Monitor></Monitor>
        </div>

        {/* 右侧内容 */}
        <div className="flex items-center justify-start w-full">
          <Table></Table>
        </div>
      </div>
    </div>
  );
};

export default Setting;
