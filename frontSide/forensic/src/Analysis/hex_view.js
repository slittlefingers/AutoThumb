import React, { useState } from 'react';

function HexViewer({ hexData, asciiData,thumbnailUrl,metadata}) {
  const [showMetadata, setShowMetadata] = useState(false);

  // 读取文件并转换为 ArrayBuffer
  const toggleMetadata = () => {
    setShowMetadata(!showMetadata);
  };

  const renderMetadata = (metadata) => {
    return (
      <div style={{ 
        position: 'fixed',       // 固定定位
        top: '470px',             // 距离页面顶部的距离
        right: '100px',           // 固定在页面右侧
        width: '300px',          // 固定宽度
        height: '400px',         // 固定高度
        overflowY: 'auto',       // 超出内容允许垂直滚动
        padding: '10px', 
        border: '1px solid #ddd', 
        borderRadius: '4px', 
        backgroundColor: '#f9f9f9',
        textAlign: 'left',
        zIndex: 1000             // 提升层级，确保显示在最前
      }}>
        {Object.entries(metadata).map(([key, value], index) => (
          <div key={index} style={{ marginBottom: '5px' }}>
            <strong>{key}:</strong> {value.toString()}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="flex flex-row" style={{ padding: '10px', borderRadius: '8px', maxWidth: '900px' }}>
      <div 
        style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          fontFamily: 'monospace', 
          overflowY: 'auto',   // 允许垂直滚动
          maxHeight: '400px',  // 固定最大高度
          border: '1px solid #ddd', 
          padding: '10px', 
          borderRadius: '4px'
        }}
      >
        {hexData.map((hexLine, index) => (
          <div key={index} style={{ display: 'flex', padding: '5px 0', borderBottom: '1px solid #ddd' }}>
            {/* 行号 */}
            <div style={{ width: '50px', textAlign: 'right', paddingRight: '10px', color: '#888' }}>
              {index.toString(16).padStart(4, '0')}
            </div>
            {/* 十六进制数据 */}
            <div style={{ width: '600px', color: '#333', fontFamily: 'monospace' }}>{hexLine}</div>
            {/* ASCII 数据 */}
            <div style={{ width: '100x', paddingLeft: '10px', color: '#555', fontFamily: 'monospace'}}>{asciiData[index]}</div>
          </div>
        
        ))}
      </div>
      {thumbnailUrl && (
        <div style={{ marginTop: '10px' , marginLeft: '20px' }}>
          <img src={thumbnailUrl} alt="Thumbnail" style={{ maxWidth: '100%', height: 'auto' }} onClick={toggleMetadata} />
        {showMetadata && renderMetadata(metadata)}
        </div>
      )}
    </div>
  );
}

export default HexViewer;
