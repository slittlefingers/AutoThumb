import React, { useState } from 'react';

const DatabaseDiffDisplay = ({ diffResult}) => {
  const [activeTab, setActiveTab] = useState('modified_tables');
  const [selectedTable, setSelectedTable] = useState(null); // 跟踪选中的表

  const tabs = [
    { label: 'Added table', value: 'missing_db1' },
    { label: 'Removed table', value: 'missing_db2' },
    { label: 'Modified Tables', value: 'modified_tables' }
  ];
  if (!diffResult || typeof diffResult !== 'object') {
    return <div>No differences found or data is still loading.</div>;
}

  return (
    <div className="flex">
      {/* Sidebar for Tabs */}
      <div className="w-1/4 p-4 bg-gray-200 overflow-y-auto " style={{ maxHeight: '340px' }} >
        <h2 className="text-lg font-bold mb-4">Database Diff</h2>
        <ul>
          {tabs.map(tab => (
            <li
              key={tab.value}
              className={`cursor-pointer p-2 mb-2 ${activeTab === tab.value ? 'bg-blue-500 text-white' : 'bg-white text-black'} hover:bg-blue-400 hover:text-white rounded-lg`}
              onClick={() => {
                setActiveTab(tab.value);
                setSelectedTable(null); // 清空选中表状态
              }}
            >
              {tab.label}
            </li>
          ))}
        </ul>

        {/* 如果是modified_tables选项，显示可点击的表名 */}
        {activeTab === 'modified_tables' && diffResult.modified_tables.length > 0 && (
          <div className="mt-4 overflow-y-auto " style={{ maxHeight: '500px' }}> {/* 左侧表名滚动 */}
            <h3 className="text-xl font-bold">Modified Tables</h3>
            <ul>
              {diffResult.modified_tables.map((tableDiff, tableIndex) => (
                <li
                  key={tableIndex}
                  className={`cursor-pointer p-2 mb-2 ${selectedTable === tableDiff ? 'bg-blue-300' : 'bg-white'} hover:bg-blue-200 rounded-lg`}
                  onClick={() => setSelectedTable(tableDiff)} // 选中表后显示右侧内容
                >
                  {tableDiff.table}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Content Section for Table Data */}
      <div className="w-3/4 p-4">
        {activeTab === 'missing_db1' && (
          <div>
            <h3 className="text-xl font-bold">Missing Tables in db1</h3>
            {diffResult.missing_tables_in_db1.length > 0 ? (
              <ul className="list-disc ml-5">
                {diffResult.missing_tables_in_db1.map((table, index) => (
                  <li key={index} className="text-red-500">{table}</li>
                ))}
              </ul>
            ) : (
              <p className="text-green-500">No missing tables in db1.</p>
            )}
          </div>
        )}

        {activeTab === 'missing_db2' && (
          <div>
            <h3 className="text-xl font-bold">Missing Tables in db2</h3>
            {diffResult.missing_tables_in_db2.length > 0 ? (
              <ul className="list-disc ml-5">
                {diffResult.missing_tables_in_db2.map((table, index) => (
                  <li key={index} className="text-red-500">{table}</li>
                ))}
              </ul>
            ) : (
              <p className="text-green-500">No missing tables in db2.</p>
            )}
          </div>
        )}

        {/* 显示右侧具体表的详细数据 */}
        {activeTab === 'modified_tables' && selectedTable && (
          <div className="overflow-y-auto h-80"> {/* 右侧表数据滚动 */}
            <h3 className="text-xl font-bold">Modified Table: {selectedTable.table}</h3>

            {/* Added Rows */}
            <div>
              <h5 className="text-green-600 font-bold">Added Rows:</h5>
              {selectedTable.added_rows.length > 0 ? (
                <ul className="list-disc ml-5">
                  {selectedTable.added_rows.map((row, rowIndex) => (
                    <li key={rowIndex} className="bg-green-100 p-2 rounded-lg">
                      {row.map((column, colIndex) => (
                        <span key={colIndex} className="block break-all">
                          {column.column}: {column.value.is_bytes ? (
                            <span className="text-sm text-blue-700" style={{ wordBreak: 'break-all', overflowWrap: 'break-word' }}>
                              [Hex: {column.value.value}]
                            </span>
                          ) : column.value.value}
                        </span>
                      ))}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No added rows.</p>
              )}
            </div>

            {/* Removed Rows */}
            <div>
              <h5 className="text-red-600 font-bold">Removed Rows:</h5>
              {selectedTable.removed_rows.length > 0 ? (
                <ul className="list-disc ml-5">
                  {selectedTable.removed_rows.map((row, rowIndex) => (
                    <li key={rowIndex} className="bg-red-100 p-2 rounded-lg">
                      {row.map((column, colIndex) => (
                        <span key={colIndex} className="block break-all">
                        {column.column}: {column.value.is_bytes ? (
                          <span className="text-sm text-blue-700" style={{ wordBreak: 'break-all', overflowWrap: 'break-word' }}>
                            [Hex: {column.value.value}]
                          </span>
                        ) : column.value.value}
                      </span>
                      ))}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No removed rows.</p>
              )}
            </div>

            {/* Modified Rows */}
            <div>
              <h5 className="text-yellow-600 font-bold">Modified Rows:</h5>
              {selectedTable.modified_rows.length > 0 ? (
                selectedTable.modified_rows.map((modRow, modRowIndex) => (
                  <div key={modRowIndex} className="mb-4">
                    <h6 className="font-bold">Original Row {modRowIndex + 1}:</h6>
                    <ul className="list-disc ml-5 bg-yellow-100 p-2 rounded-lg">
                      {modRow.original.map((column, colIndex) => (
                        <li key={colIndex} className="break-all">
                        <span className="block">
                          {column.column}: {column.value.is_bytes ? (
                            <span className="text-sm text-blue-700" style={{ wordBreak: 'break-all', overflowWrap: 'break-word' }}>
                              [Hex: {column.value.value}]
                            </span>
                          ) : column.value.value}
                        </span>
                      </li>
                      ))}
                    </ul>

                    <h6 className="font-bold">Modified Row {modRowIndex + 1}:</h6>
                    <ul className="list-disc ml-5 bg-yellow-200 p-2 rounded-lg">
                      {modRow.modified.map((column, colIndex) => (
                        <li key={colIndex} className="break-all">
                        <span className="block">
                          {column.column}: {column.value.is_bytes ? (
                            <span className="text-sm text-blue-700" style={{ wordBreak: 'break-all', overflowWrap: 'break-word' }}>
                              [Hex: {column.value.value}]
                            </span>
                          ) : column.value.value}
                        </span>
                      </li>
                      ))}
                    </ul>
                  </div>
                ))
              ) : (
                <p>No modified rows.</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};


export default DatabaseDiffDisplay;