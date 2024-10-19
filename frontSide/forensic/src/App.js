
import { BrowserRouter as Router, Route, Routes,Link } from 'react-router-dom';
import './App.css';
import Home from './Home/Home'; // 导入 Home 组件
import About from './Setting/Setting'; // 导入 Setthing 组件
import Operation from './Operation/Operation';
import LogViewer from './test/test';
import Analysis from './Analysis/Analysis';
function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/setting" element={<About />} />
          <Route path="/operation" element={<Operation />} />
          <Route path="/logviewer" element={<LogViewer />} />
          <Route path="/analysis" element={<Analysis />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
