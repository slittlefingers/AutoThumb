import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
function Table() {
  // 定义表单状态
  const navigate = useNavigate();
  const [experimentName, setExperimentName] = useState('');
  const [databasePath, setDatabasePath] = useState('');
  const [software, setSoftware] = useState('');
  const [packages, setPackages] = useState([]);
  const [selectedPackage, setSelectedPackage] = useState('');
  const [isPackageFound, setIsPackageFound] = useState(null);
  const [actions, setActions] = useState([]); // 动作列表状态
  const [loading, setLoading] = useState(false); // 加载状态
  const [formVisible, setFormVisible] = useState(true); // 表单显示状态

  // 处理表单输入变化
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'experimentName') setExperimentName(value);
    if (name === 'databasePath') setDatabasePath(value);
    if (name === 'software') setSoftware(value);

  };

  // 处理软件输入完成后的操作，例如获取相应的 packages 选项
  const handleSoftwareBlur = () => {
    axios.post('http://localhost:5000/api/get-packages', { software })
      .then(response => {
        const data = response.data;
        setPackages(data.packages);
        setSelectedPackage(''); // 清空已选择的 package
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };
  const handlePackageChange = (e) => {
    const selectedPkg = e.target.value;
    setSelectedPackage(selectedPkg);

    // 发送请求到后端验证包是否存在
    if (selectedPkg && software) {
      axios.post('http://localhost:5000/api/check-package', { software, package: selectedPkg })
        .then(response => {
          const data = response.data;
          if (data.check === true) {
            setIsPackageFound(true); // 包存在
          } else {
            setIsPackageFound(false); // 包不存在
          }
        })
        .catch(error => {
          console.error('Error:', error);
          setIsPackageFound(false); // 包不存在
        });
    } else {
      setIsPackageFound(null); // 重置状态
    }
  };
  const saveActions = () => {
    // const databasePath = localStorage.getItem('databasePath'); // 从本地存储获取数据库路径

    // const saveData = { actions, databasePath }; // 将动作列表与数据库路径打包为对象
    // console.log(saveData);
    console.log('Actions:', actions);
    const databasePath = localStorage.getItem('databasePath');
    axios.post('http://localhost:5000/api/save-actions', { 'Actions': actions, 'databasePath': databasePath }) // 发送 POST 请求到后端
      .then(response => {
        console.log('Actions saved successfully:', response.data); // 打印成功信息
        navigate('/operation');
      })
      .catch(error => {
        console.error('Error saving actions:', error); // 打印错误信息
        alert('Failed to save actions.');
      });
  };

  // 处理提交表单
  const handleSubmitpredict = (e) => {
    e.preventDefault();
    setLoading(true); // 显示加载动画
    setFormVisible(false); // 隐藏表单
    // 提交表单数据
    const formData = {
      experimentName,
      databasePath,
      software,
      selectedPackage,
    };
    console.log('Form Data:', formData);
    // 使用 Axios 发送表单数据
    axios.post('http://localhost:5000/api/submit-form', formData)
      .then(response => {
        console.log('Form submitted successfully.');
        localStorage.setItem('databasePath', response.data.databasePath);
        setActions(response.data.action_list || ["Action 1", "Action 2", "Action 3"]); // 更新动作列表
        setLoading(false); // 关闭加载动画
      })
      .catch(error => {
        console.error('Error submitting form:', error);
        setLoading(false); // 关闭加载动画
        setFormVisible(true); // 重新显示表单
      });
  };
  const handleSubmit1 = (e) => {
    e.preventDefault();
    setLoading(true); // 显示加载动画
    setFormVisible(false); // 隐藏表单
    // 提交表单数据
    const formData = {
      experimentName,
      databasePath,
      software,
      selectedPackage,
    };
    console.log('Form Data:', formData);
    // 使用 Axios 发送表单数据
    axios.post('http://localhost:5000/api/submit-form1', formData)
      .then(response => {
        console.log('Form submitted successfully.');
        localStorage.setItem('databasePath', response.data.databasePath);
        
      })
      .catch(error => {
        console.error('Error submitting form:', error);
      });
  };


  const addAction = () => {
    setActions([...actions, "New Action"]);
  };

 
  const deleteAction = (index) => {
    const newActions = actions.filter((_, i) => i !== index);
    setActions(newActions);
  };

 
  const editAction = (index, newValue) => {
    const newActions = [...actions];
    newActions[index] = newValue;
    setActions(newActions);
  };

  return (
    <div className="flex flex-col items-center justify-start p-4 w-full">
      {formVisible ? (
        <form onSubmit={handleSubmit1} className="w-1/2">
          <div className="mb-4">
            <label className="block text-2xl font-medium text-gray-700">Experiment Name</label>
            <input
              type="text"
              name="experimentName"
              value={experimentName}
              onChange={handleInputChange}
              className="mt-1 p-2 text-2xl border border-gray-300 rounded w-full"
              placeholder="Enter experiment name"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-2xl font-medium text-gray-700">Database Path</label>
            <div className="flex items-center">
              <input
                type="text"
                name="databasePath"
                value={databasePath}
                onChange={handleInputChange}
                className="mt-1 p-2 text-2xl border border-gray-300 rounded w-full"
                placeholder="Enter database path"
                required
              />
            </div>

          </div>

          <div className="mb-4">
            <label className="block text-2xl font-medium text-gray-700">Software</label>
            <input
              type="text"
              name="software"
              value={software}
              onChange={handleInputChange}
              onBlur={handleSoftwareBlur}  
              className="mt-1 p-2 text-2xl border border-gray-300 rounded w-full"
              placeholder="Enter software name"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-2xl font-medium text-gray-700">Package</label>
            <input
              list="packageOptions"
              value={selectedPackage}
              onChange={handlePackageChange}
              className="mt-1 p-2 text-2xl border border-gray-300 rounded w-full"
              placeholder="Select or enter a package"
              // disabled={!packages.length}
            />
            <datalist id="packageOptions">
              {packages.map((pkg, index) => (
                <option key={index} value={pkg} />
              ))}
            </datalist>
            {isPackageFound === null ? null : (
              <p className={`mt-2 text-${isPackageFound ? 'green' : 'red'}-500`}>
                {isPackageFound ? 'Package Found' : 'Package Not Found'}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 text-2xl"
          >
            Predict
          </button>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 text-2xl"
          >
            Design
          </button>
        </form>
      ) : (
        // 动作列表显示部分
        <div className="w-3/4">
          {loading ? (
            <p className="flex justify-center items-center text-5xl font-medium text-gray-700" style={{ fontFamily: 'Poppins', fontWeight: 800, fontStyle: 'italic' }}>Loading...</p>
          ) : (
            <div className="w-full">
              <h2 className="flex justify-center items-center text-3xl font-bold mb-4" style={{ fontFamily: 'Poppins', fontWeight: 800, fontStyle: 'italic' }}>Actions List</h2>
              {actions.length === 0 ? (
                <p className="text-xl text-gray-500" style={{ fontFamily: 'Poppins', fontWeight: 800, fontStyle: 'italic' }}>No actions available.</p>
              ) : (
                <div className="overflow-y-auto h-[400px] w-full">
                  {actions.map((action, index) => (
                    <div key={index} className="flex justify-between items-center bg-gray-100 p-2 my-1 rounded" style={{ fontFamily: 'Poppins', fontWeight: 800, fontStyle: 'italic' }}>
                      <input
                        type="text"
                        value={action}
                        onChange={(e) => editAction(index, e.target.value)} // 允许编辑
                        className="w-full p-1"
                      />
                      <button
                        onClick={() => deleteAction(index)} // 删除动作
                        className="ml-2 p-1 text-red-500 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex justify-between items-center w-full mt-4">
                <button
                  onClick={addAction} // 添加新动作
                  className="flex justify-start items-center bg-green-500 text-white px-10 py-2 rounded-full text-lg hover:bg-gray-800"
                  style={{ fontFamily: 'Poppins', fontWeight: 800, fontStyle: 'italic' }}
                >
                  Add Action
                </button>
                <button
                  onClick={saveActions} // 添加新动作
                  className="flex justify-end items-center bg-black text-white px-10 py-2 rounded-full text-lg hover:bg-gray-800"
                  style={{ fontFamily: 'Poppins', fontWeight: 800, fontStyle: 'italic' }}
                >
                  SAVE
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Table;
