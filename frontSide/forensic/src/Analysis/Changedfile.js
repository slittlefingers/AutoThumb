import React, { useState } from 'react';

const ChangedFile = ({selectedOperation, getjsondatabase, getxmldatabase,fetchbinarydata1,fetchbinarydata2,fetchBinaryData,get_picture1,get_picture2,get_picture,get_added_database,fetchThumbnail,getxmldata,thumbnaillist,fetchThumbnailmeta,fetchThumbnailmeta1,fetchThumbnailmeta2} ) => {
  // const  ModifiedFile={'xml':['ModifiedFile1','ModifiedFile2'],'database':['ModifiedFile3','ModifiedFile4','ModifiedFile5','ModifiedFile6'],'media':['ModifiedFile7','ModifiedFile8'],OTHER:['ModifiedFile9','ModifiedFile10']};
  // const  AddFile={'xml':['ModifiedFile11','ModifiedFile2'],'database':['ModifiedFile3','ModifiedFile4','ModifiedFile5','ModifiedFile6'],'media':['ModifiedFile7','ModifiedFile8'],OTHER:['ModifiedFile9','ModifiedFile10']};
  // const  RemovedFile={'xml':['ModifiedFile12','ModifiedFile2'],'database':['ModifiedFile3','ModifiedFile4','ModifiedFile5','ModifiedFile6'],'media':['ModifiedFile7','ModifiedFile8'],OTHER:['ModifiedFile9','ModifiedFile10']};
  const ModifiedFile = selectedOperation['modified'];
  const AddFile = selectedOperation['added'];
  const RemovedFile = selectedOperation['removed'];
    // 使用 useState 管理所有类型文件的展开/收缩状态
    const [expandedSections, setExpandedSections] = useState({});
    const [expandedSections1, setExpandedSections1] = useState({});
    const [expandedSections2, setExpandedSections2] = useState({});
    // 切换展开/收缩状态的函数
    const toggleSection0 = (section) => {
      setExpandedSections((prevState) => ({
        ...prevState,
        [section]: !prevState[section]
      }));
    };
    const toggleSection1 = (section) => {
      setExpandedSections1((prevState) => ({
        ...prevState,
        [section]: !prevState[section]
      }));
    };
    const toggleSection2 = (section) => {
      setExpandedSections2((prevState) => ({
        ...prevState,
        [section]: !prevState[section]
      }));
    };
    
  return (
    
    <div className="flex flex-row gap-5 items-center justify-center w-full">
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <div className='flex flex-row item-center gap-3 pb-3'>
              <img src="/modifyfile.png" alt="modify" class="w-1/6 h-1/8" />
              <h5 class="mb-2 pt-4 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                Modified File
              </h5>
              </div>
              <div class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1 h-48 overflow-y-auto">
                   {/* 遍历 ModifiedFile 对象中的每个键值对 */}
            {Object.keys(ModifiedFile).map((type) => (
              <div key={type} className="mb-2">
                {/* 文件类型标题，带有点击事件和箭头图标 */}
                <div
                  className="flex items-center cursor-pointer"
                  onClick={() => toggleSection0(type)}
                >
                  <h6 className="font-semibold text-lg text-gray-800">
                    --{type.toUpperCase()}
                  </h6>
                  <span className="ml-2 text-gray-500">
                    ({ModifiedFile[type].length} files)
                  </span>
                  <span className="ml-2 text-gray-500">
                    {/* 根据状态显示向下或向右箭头 */}
                    {expandedSections[type] ? '▼' : '▶'}
                  </span>
                </div>
                {/* 仅在展开状态下显示文件列表 */}
                {expandedSections[type] && (
                  <div className="pl-4 mt-2">
                      {ModifiedFile[type].map((file, index) => {
                      if (file){
                        // console.log(file);
                      const parts = file[1].split(/[/\\]+/);  // 处理正斜杠和反斜杠两种情况
                      // console.log(parts);
                      const lastTwoFolders = parts.slice(-2).join('/');
                      const isInThumbnailList = thumbnaillist.includes(file[1]);
                        // 提取最后两个文件夹并重新拼接为路径
                      return (
                        <p key={index}
                        className={` ${isInThumbnailList ? 'text-blue-400' : 'text-gray-600'}`}
                        onClick={() =>{if (type === 'db') {
                          getjsondatabase(file[1]); 
                        } else if (type === 'xml') {
                          getxmldatabase(file[1])
                          ;
                        } else if (type === 'other') 
                          {
                          fetchbinarydata1(file[0],file[1])
                          fetchThumbnailmeta1(file[0])
                          fetchbinarydata2(file[1])
                          fetchThumbnailmeta2(file[1])
                        }else if (type === 'picture') {
                          get_picture1(file[0])
                          fetchThumbnailmeta1(file[0])
                          get_picture2(file[1])
                          fetchThumbnailmeta2(file[1])
                        }
                      }}
                        >{lastTwoFolders}</p>
                      );
                    }
                    }
         
                      
)}
                  </div>
                )}
              </div>
            ))}
            </div>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <div className='flex flex-row item-center gap-3 pb-3'>
              <img src="/Addfile.png" alt="add" class="w-1/6 h-1/8" />
              <h5 class="mb-2 pt-4 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                Add File
              </h5>
              </div>
              <div class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1 h-48 overflow-y-auto">
                   {/* 遍历 ModifiedFile 对象中的每个键值对 */}
            {Object.keys(AddFile).map((type) => (
              <div key={type} className="mb-2">
                {/* 文件类型标题，带有点击事件和箭头图标 */}
                <div
                  className="flex items-center cursor-pointer"
                  onClick={() => toggleSection1(type)}
                >
                  <h6 className="font-semibold text-lg text-gray-800">
                    --{type.toUpperCase()}
                  </h6>
                  <span className="ml-2 text-gray-500">
                    ({AddFile[type].length} files)
                  </span>
                  <span className="ml-2 text-gray-500">
                    {/* 根据状态显示向下或向右箭头 */}
                    {expandedSections1[type] ? '▼' : '▶'}
                  </span>
                </div>
                {/* 仅在展开状态下显示文件列表 */}
                {expandedSections1[type] && (
                  <div className="pl-4 mt-2">
                      {AddFile[type].map((file, index) => {
                      if (file){
                        // console.log(file);
                      const parts = file.split(/[/\\]+/);  // 处理正斜杠和反斜杠两种情况
                      // console.log(parts);
                      const lastTwoFolders = parts.slice(-2).join('/');
                      const isInThumbnailList = thumbnaillist.includes(file)
                        // 提取最后两个文件夹并重新拼接为路径
                      return (
                        <p key={index}
                        className={` ${isInThumbnailList ? 'text-blue-400' : 'text-gray-600'}`}
                        onClick={() =>{if (type === 'db') {
                        get_added_database(file); 
                        }else if (type === 'other') {
                          fetchBinaryData(file)
                          fetchThumbnail(file)
                          fetchThumbnailmeta(file);
                        } else if (type === 'picture') {
                          get_picture(file)
                          fetchThumbnailmeta(file);
                        }else if (type === 'xml') {
                          getxmldata(file)
                        }
                        }}  
                        >{lastTwoFolders}</p>
                      );
                    }
                    }
         
                      
)}
                  </div>
                )}
              </div>
            ))}
            </div>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <div className='flex flex-row item-center gap-3 pb-3'>
              <img src="/modifyfile.png" alt="modify" class="w-1/6 h-1/8" />
              <h5 class="mb-2 pt-4 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                Removed File
              </h5>
              </div>
              <div class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1 h-48 overflow-y-auto">
                   {/* 遍历 ModifiedFile 对象中的每个键值对 */}
            {Object.keys(RemovedFile).map((type) => (
              <div key={type} className="mb-2">
                {/* 文件类型标题，带有点击事件和箭头图标 */}
                <div
                  className="flex items-center cursor-pointer"
                  onClick={() => toggleSection2(type)}
                >
                  <h6 className="font-semibold text-lg text-gray-800">
                    --{type.toUpperCase()}
                  </h6>
                  <span className="ml-2 text-gray-500">
                    ({RemovedFile[type].length} files)
                  </span>
                  <span className="ml-2 text-gray-500">
                    {/* 根据状态显示向下或向右箭头 */}
                    {expandedSections2[type] ? '▼' : '▶'}
                  </span>
                </div>
                {/* 仅在展开状态下显示文件列表 */}
                {expandedSections2[type] && (
                  <div className="pl-4 mt-2">
                    {RemovedFile[type].map((file, index) => {
                      if (file){
                        // console.log(file);
                      const parts = file.split(/[/\\]+/);  // 处理正斜杠和反斜杠两种情况
                      // console.log(parts);
                      const lastTwoFolders = parts.slice(-2).join('/');
                      const isInThumbnailList = thumbnaillist.includes(file)
                        // 提取最后两个文件夹并重新拼接为路径
                      return (
                        <p key={index} 
                        className={`${isInThumbnailList ? 'text-blue-400' : 'text-gray-600 '}`}
                        onClick={() =>{if (type === 'db') {
                          get_added_database(file);
                          }else if (type === 'other') {
                            fetchBinaryData(file);
                            fetchThumbnail(file);
                            fetchThumbnailmeta(file);
                          }else if (type === 'picture') {
                            get_picture(file)
                            fetchThumbnailmeta(file);
                          }else if (type === 'xml') {
                            getxmldata(file)
                          }
                        }} 
                        >{lastTwoFolders}</p>
                      );
                    }
                    }
         
                      
)}
                  </div>
                )}
              </div>
            ))}
            </div>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
     
      </div>
  );
};

export default ChangedFile;
