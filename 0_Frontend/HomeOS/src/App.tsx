
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from "./pages/auth/Login.tsx"
import Hello from "./pages/auth/Hello.tsx"

const App = () => {
  return (
    <BrowserRouter>
      
      <Routes>
        <Route path="/" element={<Hello />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      
    </BrowserRouter>
  );
}

export default App;
