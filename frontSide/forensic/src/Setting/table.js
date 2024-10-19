import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Table() {
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

  // 处理软件输入完成后的操作
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

  // 处理 package 选择
  const handlePackageChange = (e) => {
    const selectedPkg = e.target.value;
    setSelectedPackage(selectedPkg);

    // 验证包是否存在
    if (selectedPkg && software) {
      axios.post('http://localhost:5000/api/check-package', { software, package: selectedPkg })
        .then(response => {
          const data = response.data;
          setIsPackageFound(data.check === true);
        })
        .catch(error => {
          console.error('Error:', error);
          setIsPackageFound(false);
        });
    } else {
      setIsPackageFound(null);
    }
  };

  // Predict 按钮提交表单数据并生成 actions
  const handleSubmitPredict = (e) => {
    e.preventDefault();
    setLoading(true);
    setFormVisible(false);

    const formData = { experimentName, databasePath, software, selectedPackage };
    axios.post('http://localhost:5000/api/submit-form', formData)
      .then(response => {
        localStorage.setItem('databasePath', response.data.databasePath);
        setActions(response.data.action_list || ["Action 1", "Action 2", "Action 3"]); // 使用后端返回的 action_list
        setLoading(false);
      })
      .catch(error => {
        console.error('Error submitting form:', error);
        setLoading(false);
        setFormVisible(true);
      });
  };

  // Design button only submit form data
  const handleSubmitDesign = (e) => {
    e.preventDefault();
    setLoading(true);
    setFormVisible(false);

    const formData = { experimentName, databasePath, software, selectedPackage };
    axios.post('http://localhost:5000/api/design-form', formData) // 调用另一个 API
      .then(response => {
        localStorage.setItem('databasePath', response.data.databasePath);
        console.log(response.data.databasePath);
        setActions([]); // 清空 actions，允许用户手动输入
        setLoading(false);
      })
      .catch(error => {
        console.error('Error submitting form:', error);
        setLoading(false);
        setFormVisible(true);
      });
  };

  // 添加动作
  const addAction = () => {
    setActions([...actions, "New Action"]);
  };

  // 删除动作
  const deleteAction = (index) => {
    const newActions = actions.filter((_, i) => i !== index);
    setActions(newActions);
  };

  // 编辑动作
  const editAction = (index, newValue) => {
    const newActions = [...actions];
    newActions[index] = newValue;
    setActions(newActions);
  };

  // 保存动作
  const saveActions = () => {
    const databasePath = localStorage.getItem('databasePath');
    console.log({ actions, databasePath });
    console.log('Actions:', actions);
    axios.post('http://localhost:5000/api/save-actions', { 'Actions':actions, 'databasePath':databasePath })
      .then(response => {
        navigate('/operation');
      })
      .catch(error => {
        console.error('Error saving actions:', error);
        alert('Failed to save actions.');
      });
  };

  return (
    <div className="flex flex-col items-center justify-start p-4 w-full">
      {formVisible ? (
        <form className="w-1/2">
          {/* 表单内容 */}
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

          {/* Predict 按钮 */}
          <button
            onClick={handleSubmitPredict}
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600 text-2xl mb-2"
          >
            Predict
          </button>

          {/* Design 按钮 */}
          <button
            onClick={handleSubmitDesign}
            className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600 text-2xl"
          >
            Design
          </button>
        </form>
      ) : (
        <div className="w-3/4">
          {loading ? (
            <p className="text-5xl font-medium text-gray-700">Loading...</p>
          ) : (
            <div>
              <h2 className="text-3xl font-bold mb-4">Actions List</h2>
              {actions.length === 0 ? (
                <p className="text-xl text-gray-500">No actions available. Add actions manually.</p>
              ) : (
                <div className="overflow-y-auto h-[400px] w-full">
                  {actions.map((action, index) => (
                    <div key={index} className="flex justify-between items-center bg-gray-100 p-2 my-1 rounded">
                      <input
                        type="text"
                        value={action}
                        onChange={(e) => editAction(index, e.target.value)}
                        className="w-full p-1"
                      />
                      <button
                        onClick={() => deleteAction(index)}
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
                  onClick={addAction}
                  className="bg-green-500 text-white px-10 py-2 rounded-full text-lg hover:bg-green-600"
                >
                  Add Action
                </button>
                <button
                  onClick={saveActions}
                  className="bg-black text-white px-10 py-2 rounded-full text-lg hover:bg-gray-800"
                >
                  Save
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
