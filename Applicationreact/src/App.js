import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUpForm from './components/SignUpForm';
import Hi from './components/Hi';
import './App.scss';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<SignUpForm />} />
          <Route path="/Hi" element={<Hi />} /> 
        </Routes>
      </div>
    </Router>
  );
}

export default App;
