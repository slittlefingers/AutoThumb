import React , { useState } from 'react';

function HexViewer2({ hexData1, asciiData1, hexData2, asciiData2, whichone, fetchThumbnail,thumbnailUrl,metadata }) {
  const [showMetadata, setShowMetadata] = useState(false); // 用于切换显示metadata

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
    <div style={{ padding: '10px', borderRadius: '8px', maxWidth: '600px' }}>
      <div 
        style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          fontFamily: 'monospace', 
          overflowY: 'auto',   // 允许垂直滚动
          maxHeight: '400px',  // 固定最大高度
          border: '1px solid #ddd', 
          padding: '10px', 
          borderRadius: '4px',
          fontSize: '10px'
        }}
      > 
        {/* 显示两个文件的十六进制数据 */}
        <div>{whichone}</div>
        {hexData1.map((hexLine, index) => (
          <div key={index} style={{ display: 'flex', padding: '5px 0', borderBottom: '1px solid #ddd' }}>
            {/* 行号 */}
            <div style={{ width: '50px', textAlign: 'right', paddingRight: '10px', color: '#888' }}>
              {index.toString(16).padStart(4, '0')}
            </div>
            {/* 十六进制数据 - 每两个字符分隔 */}
            <div style={{ width: '600px', color: '#333', fontFamily: 'monospace' }}>
              {hexData1[index].split(' ').map((byte, i) => (
                <span 
                  key={i} 
                  style={{ 
                    backgroundColor: byte !== (hexData2[index]?.split(' ')[i] || '') ? 'yellow' : 'transparent',
                    marginRight: (i % 2 === 1) ? '8px' : '4px' // 每两个字节之后增加额外的间隔
                  }}
                >
                  {byte}
                </span>
              ))}
            </div>
            {/* ASCII 数据 - 每两个字符分隔 */}
            <div style={{ paddingLeft: '10px', color: '#555', fontFamily: 'monospace' }}>
              {asciiData1[index].split('').map((char, i) => (
                <span 
                  key={i} 
                  style={{ 
                    backgroundColor: char !== (asciiData2[index]?.[i] || '') ? 'yellow' : 'transparent',
                    marginRight: (i % 2 === 1) ? '8px' : '4px' // 每两个字符之后增加额外的间隔
                  }}
                >
                  {char}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
      <button 
        onClick={() => fetchThumbnail()} 
        style={{ width: '100%', marginTop: '10px', padding: '10px', borderRadius: '4px', border: '1px solid #ccc', backgroundColor: '#f8f8f6', color: '#333' }}>
        Fetch Thumbnail
      </button>

      {/* 如果有图片数据，显示图片 */}
      {thumbnailUrl && (
        <div style={{ marginTop: '20px' }}>
          <img src={thumbnailUrl} alt="Thumbnail" style={{ maxWidth: '100%', height: 'auto' }} onClick={toggleMetadata}/>
          {showMetadata && (
            <div>
              <h4>Metadata</h4>
              {renderMetadata(metadata)}
            </div>
          )}
        </div>
      )}
    
    </div>
  );
}

export default HexViewer2;
