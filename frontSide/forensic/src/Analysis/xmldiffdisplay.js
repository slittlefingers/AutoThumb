import React, { useState } from 'react';

const XMLDiffDisplay = ({ diffResult }) => {
  const [activeTab, setActiveTab] = useState('modified');  // 默认显示modified
  const [selectedDiff, setSelectedDiff] = useState(null); // 选中的差异节点

  const tabs = [
    { label: 'Added Elements', value: 'added' },
    { label: 'Removed Elements', value: 'removed' },
    { label: 'Modified Elements', value: 'modified' }
  ];

  if (!diffResult || typeof diffResult !== 'object') {
    return <div>No differences found or data is still loading.</div>;
  }

  return (
    <div className="flex">
      {/* Sidebar for Tabs */}
      <div className="w-1/4 p-4 bg-gray-200 overflow-y-auto " style={{ maxHeight: '340px' }}>
        <h2 className="text-lg font-bold mb-4">XML Diff</h2>
        <ul>
          {tabs.map(tab => (
            <li
              key={tab.value}
              className={`cursor-pointer p-2 mb-2 ${activeTab === tab.value ? 'bg-blue-500 text-white' : 'bg-white text-black'} hover:bg-blue-400 hover:text-white rounded-lg`}
              onClick={() => {
                setActiveTab(tab.value);
                setSelectedDiff(null); // 清空选中表状态
              }}
            >
              {tab.label}
            </li>
          ))}
        </ul>

        {/* 根据选项显示可点击的差异路径 */}
        {activeTab === 'modified' && diffResult.modified.length > 0 && (
          <div className="mt-4 overflow-y-auto " style={{ maxHeight: '500px' }}>
            <h3 className="text-xl font-bold">Modified Elements</h3>
            <ul>
              {diffResult.modified.map((modDiff, index) => (
                <li
                  key={index}
                  className={`cursor-pointer p-2 mb-2 ${selectedDiff === modDiff ? 'bg-blue-300' : 'bg-white'} hover:bg-blue-200 rounded-lg`}
                  onClick={() => setSelectedDiff(modDiff)}
                >
                  {modDiff.path}
                </li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'added' && diffResult.added.length > 0 && (
          <div className="mt-4 overflow-y-auto " style={{ maxHeight: '500px' }}>
            <h3 className="text-xl font-bold">Added Elements</h3>
            <ul>
              {diffResult.added.map((addDiff, index) => (
                <li
                  key={index}
                  className={`cursor-pointer p-2 mb-2 ${selectedDiff === addDiff ? 'bg-green-300' : 'bg-white'} hover:bg-green-200 rounded-lg`}
                  onClick={() => setSelectedDiff(addDiff)}
                >
                  {addDiff.path}
                </li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'removed' && diffResult.removed.length > 0 && (
          <div className="mt-4 overflow-y-auto " style={{ maxHeight: '500px' }}>
            <h3 className="text-xl font-bold">Removed Elements</h3>
            <ul>
              {diffResult.removed.map((remDiff, index) => (
                <li
                  key={index}
                  className={`cursor-pointer p-2 mb-2 ${selectedDiff === remDiff ? 'bg-red-300' : 'bg-white'} hover:bg-red-200 rounded-lg`}
                  onClick={() => setSelectedDiff(remDiff)}
                >
                  {remDiff.path}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Content Section for Detailed Differences */}
      <div className="w-3/4 p-4">
        {activeTab === 'modified' && selectedDiff && (
          <div className="overflow-y-auto h-80">
            <h3 className="text-xl font-bold">Modified Element at: {selectedDiff.path}</h3>

            {selectedDiff.tag && (
              <div className="mt-4">
                <h4 className="text-yellow-600">Tag Change:</h4>
                <p>Before: {selectedDiff.tag.before}</p>
                <p>After: {selectedDiff.tag.after}</p>
              </div>
            )}

            {selectedDiff.attributes && (
              <div className="mt-4">
                <h4 className="text-yellow-600">Attributes Change:</h4>
                <p>Before: {JSON.stringify(selectedDiff.attributes.before)}</p>
                <p>After: {JSON.stringify(selectedDiff.attributes.after)}</p>
              </div>
            )}

            {selectedDiff.text && (
              <div className="mt-4">
                <h4 className="text-yellow-600">Text Change:</h4>
                <p>Before: {selectedDiff.text.before}</p>
                <p>After: {selectedDiff.text.after}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'added' && selectedDiff && (
          <div className="overflow-y-auto h-80">
            <h3 className="text-xl font-bold">Added Element at: {selectedDiff.path}</h3>
            <pre>{selectedDiff.element}</pre>
          </div>
        )}

        {activeTab === 'removed' && selectedDiff && (
          <div className="overflow-y-auto h-80">
            <h3 className="text-xl font-bold">Removed Element at: {selectedDiff.path}</h3>
            <pre>{selectedDiff.element}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default XMLDiffDisplay;