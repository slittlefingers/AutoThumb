import React, { useEffect, useState } from 'react';
import Sidebar from './sidebar';
import ChangedFile from './Changedfile';
import axios from 'axios';
import DatabaseDiffDisplay from './detailfilecompare';
import XMLDiffDisplay from './xmldiffdisplay';
import HexViewer from './hex_view';
import HexViewer2 from './Hexviewer2';
import PictureDisplay from './picture_compare';
import AddedDatabaseDiffDisplay from './added_database';
function Analysis() {
  const [Operation, setOperations] = useState([]);
  const [operation_id, setOperation_id] = useState(0);
  const [loading, setLoading] = useState(false); // 加载状态
  // const [formVisible, setFormVisible] = useState(true); // 表单显示状态
  const [selectedOperation, setSelectedOperation] = useState(null);
  const [analysisCompleted, setAnalysisCompleted] = useState(false);
  const [diffResult, setDiffResult] = useState('');
  const [diffResult1, setDiffResult1] = useState({});
  const [xmlResult, setXmlResult] = useState({});
  const [hexData1, setHexData1] = useState([]);
  const [asciiData1, setAsciiData1] = useState([]);
  const [hexData2, setHexData2] = useState([]);
  const [asciiData2, setAsciiData2] = useState([]);
  const [file, setFile] = useState([]);
  const [thumbnailUrl, setThumbnailUrl] = useState(null);
  const [thumbnailUrl1, setThumbnailUrl1] = useState(null);
  const [thumbnailUrl2, setThumbnailUrl2] = useState(null);
  const [pictureUrl1, setPictureUrl1] = useState(null);
  const [pictureUrl2, setPictureUrl2] = useState(null);
  const [pictureUrl, setPictureUrl] = useState(null);
  const [whichcomponent, setWhichComponent] = useState(0);
  const [thumbnaillist, setThumbnaillist] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [ThumbnailUrlan, setThumbnailUrlan] = useState(null);
  const [keywordmatch, setkeywordmatch] = useState([]);
  const [experiment, setExperiment] = useState([])
  const [isModalOpen2, setIsModalOpen2] = useState(false);
  const [metadata, setmetadata] = useState({});
  const [metadata1, setmetadata1] = useState({});
  const [metadata2, setmetadata2] = useState({});
  // const [xmldata, setxmldata] = useState({});
  useEffect(() => {
    starttoanalysis();
    fetchOperations();

  }, []);
  const handleOperationClick = async (operation_id) => {
    try {
      console.log({ 'operation_id': operation_id, 'databasePath': localStorage.getItem('databasePath') })
      // 向后端发送请求，获取与 operation_id 相关的数据
      const response = await axios.post('http://localhost:5000/api/get-changed-files', { 'operation_id': operation_id, 'databasePath': localStorage.getItem('databasePath') });
      // 将后端返回的数据存储到状态中
      setOperation_id(operation_id);
      console.log(response.data);
      setSelectedOperation(response.data);
      console.log(selectedOperation);
    } catch (error) {
      console.error('Error fetching data from backend:', error);
    }
    try {
      console.log({ 'end_operation_id': operation_id, 'databasePath': localStorage.getItem('databasePath') })
      // 向后端发送请求，获取与 operation_id 相关的数据
      const response = await axios.post('http://localhost:5000/api/get-thumbnailname', { 'end_operation_id': operation_id, 'databasePath': localStorage.getItem('databasePath') });
      // 将后端返回的数据存储到状态中
      console.log(response.data);
      setThumbnaillist(response.data);
      console.log(thumbnaillist);
    } catch (error) {
      console.error('Error fetching data from backend:', error);
    }

  };

  const fetchOperations = async () => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/get-operations', {
        'databasePath': databasePath  // 替换为实际的数据库路径
      });
      setOperations(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  };

  const starttoanalysis = async () => {
    setLoading(true); // 显示加载动画
    try {
      const databasePath = localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/start_to_analysis', {
        'databasePath': databasePath // 替换为实际的数据库路径
      });
      console.log(response.data)
      setAnalysisCompleted(true);
      setLoading(false); // 关闭加载动画
    } catch (error) {
      console.error('Error fetching actions:', error);
      setLoading(false)
    }
  };

  const getjsondatabase = async (filepath) => {
    try {

      const databasePath = localStorage.getItem('databasePath');
      console.log({ 'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath })
      const response = await axios.post('http://localhost:5000/api/get-detail-jsondata', {
        'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath // 替换为实际的数据库路径
      })
      console.log(response.data)
      setDiffResult(response.data);
      setXmlResult({});
      setHexData1([]);
      setHexData2([]);
      setWhichComponent(1);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  };

  const get_added_database = async (filepath) => {
    try {

      const databasePath = localStorage.getItem('databasePath');
      console.log({ 'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath })
      const response = await axios.post('http://localhost:5000/api/get-detail-jsondata', {
        'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath // 替换为实际的数据库路径
      })
      console.log(response.data)
      setDiffResult1(response.data);
      setWhichComponent(5);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  };

  const getxmldatabase = async (filepath) => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      console.log({ 'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath })
      const response = await axios.post('http://localhost:5000/api/get-detail-jsondata', {
        'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath // 替换为实际的数据库路径
      })
      console.log(response.data)
      setDiffResult({});
      setXmlResult(response.data);
      setHexData1([]);
      setHexData2([]);
      setWhichComponent(2);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  };

  const getxmldata = async (filepath) => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      console.log({ 'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath })
      const response = await axios.post('http://localhost:5000/api/get-detail-jsondata', {
        'databasePath': databasePath, 'operation_id': operation_id, 'filepath': filepath // 替换为实际的数据库路径
      })
      console.log(response.data)
      setXmlResult(response.data);
      setWhichComponent(8);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  };



  // 将文件的 ArrayBuffer 转换为十六进制和 ASCII
  const arrayBufferToHexAndAscii1 = (buffer) => {
    const hexArray = [];
    const asciiArray = [];
    const bytes = new Uint8Array(buffer);

    for (let i = 0; i < bytes.length; i += 16) {
      // 生成十六进制数据
      const hexPart = bytes.slice(i, i + 16)
        .reduce((acc, byte) => acc + byte.toString(16).padStart(2, '0') + ' ', '');
      hexArray.push(hexPart);

      // 生成 ASCII 数据
      const asciiPart = bytes.slice(i, i + 16)
        .reduce((acc, byte) => acc + (byte >= 32 && byte <= 126 ? String.fromCharCode(byte) : '.'), '');
      asciiArray.push(asciiPart);
    }

    setHexData1(hexArray);
    setAsciiData1(asciiArray);
    setDiffResult('');
    setXmlResult({});
    setWhichComponent(3);
  };
  const arrayBufferToHexAndAscii2 = (buffer) => {
    const hexArray = [];
    const asciiArray = [];
    const bytes = new Uint8Array(buffer);

    for (let i = 0; i < bytes.length; i += 16) {
      // 生成十六进制数据
      const hexPart = bytes.slice(i, i + 16)
        .reduce((acc, byte) => acc + byte.toString(16).padStart(2, '0') + ' ', '');
      hexArray.push(hexPart);

      // 生成 ASCII 数据
      const asciiPart = bytes.slice(i, i + 16)
        .reduce((acc, byte) => acc + (byte >= 32 && byte <= 126 ? String.fromCharCode(byte) : '.'), '');
      asciiArray.push(asciiPart);
    }

    setHexData2(hexArray);
    setAsciiData2(asciiArray);
  };
  const fetchBinaryData = async (file) => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/get-binary-files', {
        'file': file, 'databasePath': databasePath // 替换为实际的数据库路径
      }, {
        responseType: 'arraybuffer'
      })
      console.log(file);
      arrayBufferToHexAndAscii1(response.data);
      setWhichComponent(6);
    } catch (error) {
      console.error('Error fetching binary data:', error);
    }
  };
  const fetchBinaryData1 = async (file1, file2) => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/get-binary-files', {
        'file': file1, 'databasePath': databasePath // 替换为实际的数据库路径
      }, {
        responseType: 'arraybuffer'
      })
      console.log(file2);
      const list = [file1, file2]
      setFile(list);
      console.log(file);
      arrayBufferToHexAndAscii1(response.data);
    } catch (error) {
      console.error('Error fetching binary data:', error);
    }
  };

  const fetchBinaryData2 = async (file2) => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/get-binary-files', {
        'file': file2, 'databasePath': databasePath // 替换为实际的数据库路径
      }, {
        responseType: 'arraybuffer'
      })
      arrayBufferToHexAndAscii2(response.data);
    } catch (error) {
      console.error('Error fetching binary data:', error);
    }
  };

  const fetchThumbnail1 = async () => {
    try {
      console.log(file[0]);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-thumbnail', {
        'databasePath': databasePath, 'file_path': file[0], 'end_operation_id': operation_id,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setThumbnailUrl1(imageUrl);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };
  const fetchThumbnail = async (file) => {
    try {
      setThumbnailUrl(null);
      console.log(file[0]);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-thumbnail', {
        'databasePath': databasePath, 'file_path': file, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setThumbnailUrl(imageUrl);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };

  const fetchThumbnail2 = async () => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      console.log(file[1]);
      const response = await axios.post('http://localhost:5000/api/get-thumbnail', {
        'databasePath': databasePath, 'file_path': file[1], 'end_operation_id': operation_id,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setThumbnailUrl2(imageUrl);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };
  const fetchThumbnailmeta = async (file) => {
    try {
      console.log(file[0]);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-thumbnailmeta', {
        'databasePath': databasePath, 'file_path': file, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      })
      setmetadata(response.data);
      console.log(response.data);
      
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };
  const fetchThumbnailmeta1 = async (file) => {
    try {
      setThumbnailUrl(null);
      console.log(file[0]);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-thumbnailmeta', {
        'databasePath': databasePath, 'file_path': file, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      })

      setmetadata1(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };

  const fetchThumbnailmeta2 = async () => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      console.log(file[1]);
      const response = await axios.post('http://localhost:5000/api/get-thumbnailmeta', {
        'databasePath': databasePath, 'file_path': file[1], 'end_operation_id': operation_id,   // 替换为实际的图片路径
      })

      setmetadata2(response.data);
      console.log(response.data);
     
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };
  const get_picture1 = async (file1) => {
    try {
      console.log(file[0]);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-picture', {
        'databasePath': databasePath, 'file_path': file1, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setPictureUrl1(imageUrl);
      setWhichComponent(4);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };

  const get_picture2 = async (file2) => {
    try {
      console.log(file[0]);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-picture', {
        'databasePath': databasePath, 'file_path': file2, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setPictureUrl2(imageUrl);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };

  const get_picture = async (file) => {
    try {

      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-picture', {
        'databasePath': databasePath, 'file_path': file, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setPictureUrl(imageUrl);
      setWhichComponent(7);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };
  const get_all_experiment = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/get_all_experiment')
      setExperiment(response.data)
      setIsModalOpen2(true)
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }

  }
  const closeModal2 = () => {
    setIsModalOpen2(false);

    setExperiment([[]]);
  };
  // const openModal = () => {
  //   setIsModalOpen(true);
  // };

  const closeModal = () => {
    setIsModalOpen(false);
    setThumbnailUrlan(null);
    setkeywordmatch([]);
  };
  const openModal = async () => {
    try {
      setIsModalOpen(true);
      const databasePath = localStorage.getItem('databasePath');
      // 替换为实际的图片路径
      const response = await axios.post('http://localhost:5000/api/get-thumbnailan', {
        'databasePath': databasePath, 'file_path': operation_id, 'end_operation_id': operation_id + 1000,   // 替换为实际的图片路径
      }, {
        responseType: 'blob'  // 确保返回的是二进制数据
      });

      const imageUrl = URL.createObjectURL(new Blob([response.data])); // 将blob转换为URL
      setThumbnailUrlan(imageUrl);
    } catch (error) {
      console.error('Error fetching thumbnail:', error);
    }
  };

  const getkeywordmatch = async () => {
    try {
      const databasePath = localStorage.getItem('databasePath');
      const response = await axios.post('http://localhost:5000/api/get-keywordmatch', {
        'databasePath': databasePath, 'end_operation_id': operation_id,   // 替换为实际的图片路径
      });
      console.log(response.data)
      setkeywordmatch(response.data);
    } catch (error) {
      console.error('Error fetching actions:', error);
    }
  }
  const settingdatapath = (databasepath) => {
    localStorage.setItem('databasePath', databasepath)
    console.log('database change to',databasepath)

  }
  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-7 gap-5 items-left justify-items-center w-full mt-8 px-4">
        <div className="md:col-span-1 flex items-center justify-center w-full">
          <Sidebar Operation={Operation} onOperationClick={handleOperationClick} openModal={openModal} getkeywordmatch={getkeywordmatch} get_all_experiment={get_all_experiment} />
        </div >
        <div className="md:col-span-6 flex items-center justify-center w-full">
          <div className="flex flex-col gap-5 items-center justify-start w-full mt-8 px-4">

            {analysisCompleted && selectedOperation ? (
              <ChangedFile selectedOperation={selectedOperation} getjsondatabase={getjsondatabase} getxmldatabase={getxmldatabase} fetchbinarydata1={fetchBinaryData1} fetchbinarydata2={fetchBinaryData2} fetchBinaryData={fetchBinaryData} get_picture1={get_picture1} get_picture2={get_picture2} get_picture={get_picture} get_added_database={get_added_database} fetchThumbnail={fetchThumbnail} getxmldata={getxmldata} thumbnaillist={thumbnaillist} fetchThumbnailmeta={fetchThumbnailmeta} fetchThumbnailmeta1={fetchThumbnailmeta1} fetchThumbnailmeta2={fetchThumbnailmeta2}/>
            ) : (
              <div>Please select an operation after analysis is completed.</div>
            )}
            {/* Add modal */}
            {isModalOpen && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
                <div className="bg-white p-6 rounded-lg shadow-lg relative 2xl mx-auto">
                  <button
                    onClick={closeModal}
                    className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-xl">
                    &times;
                  </button>
                  <div className="text-center">


                    {/* 使用 flex 将图片和关键词列表左右排列 */}
                    <div className="flex">

                      {/* 左边显示 Thumbnail */}
                      <div className="w-1/4 text-left mt-4 pr-12"> {/* 左边宽度占据一半 */}
                        <h2 className="text-2xl font-bold mb-4">Thumbnail Detail</h2>
                        {ThumbnailUrlan ? (
                          <img
                            src={ThumbnailUrlan}
                            alt="Thumbnail"
                            className="object-contain h-auto max-h-[80vh] rounded-lg shadow-md" // 限制图片最大高度为屏幕的一半
                          />
                        ) : (
                          <div className="text-gray-500 text-xl">
                            <p>Not Found</p> {/* 如果没有图片则显示 "Not Found" */}
                          </div>
                        )}
                      </div>

                      {/* 右边显示关键词匹配 */}
                      <div className="w-3/4 text-left mt-4 pl-12">
                        <h3 className="text-2xl font-bold mb-4">Keyword Match</h3>
                        <div className="mt-2">
                          {keywordmatch.length > 0 ? (
                            keywordmatch.map((item, index) => (
                              item[1].length > 0 && (  // 如果第二个元素（列表）非空，才显示
                                <div key={index} className="flex items-center text-gray-700"> {/* 使用 flex */}
                                  <div className="font-bold">{item[1].split(/[\\/]/).slice(4).join('/')}</div>

                                  {/* 小箭头 */}
                                  <div className="mx-2">→</div>

                                  {/* 显示对应描述 */}
                                  <div>{JSON.stringify(item[0])}</div>
                                </div>
                              )
                            ))
                          ) : (
                            <p className="text-gray-500">No keyword matches found.</p>  // 当 keywordmatch 为空时显示的内容
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            {isModalOpen2 && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
                <div className="bg-white p-6 rounded-lg shadow-lg relative 2xl mx-auto  max-h-[80vh] overflow-y-auto">
                  <button
                    onClick={closeModal2}
                    className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-xl">
                    &times;
                  </button>
                  <div className="text-center">

                    <h3 className="text-2xl font-bold mb-4">Experimentname</h3>
                    <div className="mt-2">
                      {experiment.length > 0 ? (
                        experiment.map((item, index) => (
                          item[0].length > 0 && (  // 如果第二个元素（列表）非空，才显示
                            <div key={index} className="flex items-center text-gray-700"> {/* 使用 flex */}
                              <div className="font-bold" onClick={() => settingdatapath(item[1])}>{item[0]}</div>
                            </div>
                          )
                        ))
                      ) : (
                        <p className="text-gray-500">No experiment found.</p>  // 当 keywordmatch 为空时显示的内容
                      )}
                    </div>
                  </div>
                </div>
              </div>

            )}

            <div className=" w-full mt-8 px-4 pl-60 pr-60">

              {whichcomponent === 1 ? (
                <DatabaseDiffDisplay diffResult={diffResult} />
              ) : whichcomponent === 2 && xmlResult && typeof xmlResult === 'object' && Object.keys(xmlResult).length > 0 ? (
                <XMLDiffDisplay diffResult={xmlResult} />
              ) : whichcomponent === 3 && hexData1.length > 0 && asciiData1.length > 0 && hexData2.length > 0 && asciiData2.length > 0 && hexData2 ? (<div className='flex flex-row justify-center items-center'>
                <HexViewer2 hexData1={hexData1} asciiData1={asciiData1} hexData2={hexData2} asciiData2={asciiData2} whichone={'Previous file'} fetchThumbnail={fetchThumbnail1} thumbnailUrl={thumbnailUrl1} metadata={metadata1} />
                <HexViewer2 hexData1={hexData2} asciiData1={asciiData2} hexData2={hexData1} asciiData2={asciiData1} whichone={'Current file'} fetchThumbnail={fetchThumbnail2} thumbnailUrl={thumbnailUrl2}  metadata={metadata2}/>
              </div>) : whichcomponent === 4 ? (
                <div className='flex flex-row justify-center items-center'>
                  <PictureDisplay pictureurl={pictureUrl1} picture={"Previous Picture"} metadata={metadata1} />
                  <PictureDisplay pictureurl={pictureUrl2} picture={"Current Picture"} metadata={metadata2} />
                </div>
              ) : whichcomponent === 5 ? (
                <AddedDatabaseDiffDisplay diffResult1={diffResult1} />) :
                whichcomponent === 6 ? (
                  <HexViewer hexData={hexData1} asciiData={asciiData1} thumbnailUrl={thumbnailUrl} metadata={metadata}/>) :
                  whichcomponent === 7 ? (
                    <PictureDisplay pictureurl={pictureUrl} picture={"Picture"} metadata={metadata}/>) :
                    whichcomponent === 8 ? (
                      <XMLDiffDisplay diffResult={xmlResult} />) :

                      (
                        <div className='text-center'>No data to display</div>
                      )}

            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default Analysis;