import React , { useState } from 'react';
function PictureDisplay({ pictureurl,picture,metadata}) {
  const [showMetadata, setShowMetadata] = useState(false); // 用于控制metadata的显示状态

  const toggleMetadata = () => {
    setShowMetadata(!showMetadata);
  };

  const renderMetadata = (metadata) => {
    return (
      <div style={{ 
        position: 'fixed',       // 固定定位
        top: '20px',             // 距离页面顶部的距离
        right: '20px',           // 固定在页面右侧
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
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'start', alignItems: 'center', width: '100%', textAlign: 'center', height: '100vh' }}>
        <h2>{picture}</h2>
        <img
          src={pictureurl}
          alt="Fetched from API"
          onClick={toggleMetadata}
          style={{
            maxWidth: '100%',
            maxHeight: '500px',  
            width: 'auto',       
            height: 'auto',      
            padding: '10px',
            borderRadius: '8px',
            objectFit: 'contain' 
          }}
        />
         {showMetadata && renderMetadata(metadata)}
      </div>
    );
  }
  
  export default PictureDisplay;