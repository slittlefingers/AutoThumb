import React, { useState } from 'react';

const DatabaseDiffDisplay = ({ diffResult1 }) => {
  const [selectedTable, setSelectedTable] = useState(null); // 跟踪选中的表

  if (!diffResult1 || typeof diffResult1 !== 'object') {
    return <div>No data found or data is still loading.</div>;
  }

  return (
    <div className="flex">
      {/* Sidebar for table names */}
      <div className="w-1/4 p-4 bg-gray-200 overflow-y-auto" style={{ maxHeight: '500px' }}>
        <h2 className="text-lg font-bold mb-4">Database Tables</h2>
        <ul>
          {Object.keys(diffResult1).map((tableName, tableIndex) => (
            <li
              key={tableIndex}
              className={`cursor-pointer p-2 mb-2 ${selectedTable === tableName ? 'bg-blue-500 text-white' : 'bg-white text-black'} hover:bg-blue-400 hover:text-white rounded-lg`}
              onClick={() => setSelectedTable(tableName)} // 选中表后显示右侧内容
            >
              {tableName}
            </li>
          ))}
        </ul>
      </div>

      {/* Content Section for Table Data */}
      <div className="w-3/4 p-4">
        {selectedTable ? (
          <div className="overflow-y-auto h-80">
            <h3 className="text-xl font-bold">Table: {selectedTable}</h3>
            {diffResult1[selectedTable].length > 0 ? (
              <div className="flex flex-col gap-4">
                {diffResult1[selectedTable].map((row, rowIndex) => (
                  <div
                    key={rowIndex}
                    className="bg-green-100 p-4 rounded-lg shadow-md border border-green-300"
                    style={{ backgroundColor: '#d4edda' }} // 绿色背景
                  >
                    <h4 className="font-bold mb-2">Record {rowIndex + 1}</h4>
                    {Object.keys(row).map((column, colIndex) => (
                      <div key={colIndex} className="mb-1 break-all">
                        <span className="font-semibold">{column}:</span>{' '}
                        {/* 处理对象类型的数据 */}
                        {typeof row[column] === 'object' ? (
                          row[column].is_bytes ? (
                            <span
                              className="text-sm text-blue-700"
                              style={{
                                wordWrap: 'break-word',    // 自动换行
                                whiteSpace: 'pre-wrap',    // 保留空白字符和换行符
                                overflowWrap: 'break-word' // 确保超长单词也会换行
                              }}
                            >
                              [Hex: {row[column].value}]
                            </span>
                          ) : (
                            <span>{row[column].value}</span> // 渲染对象的值
                          )
                        ) : (
                          <span>{row[column]}</span> // 渲染非对象类型的值
                        )}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            ) : (
              <p>No data in this table.</p>
            )}
          </div>
        ) : (
          <div>Select a table to view its data</div>
        )}
      </div>
    </div>
  );
};

export default DatabaseDiffDisplay;
