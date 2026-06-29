
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from "./pages/auth/Login.tsx"
import Hello from "./pages/auth/Hello.tsx"
import Dashboard from "./pages/dashboard/Dahsborad.tsx"
import AdminPanel from "./pages/dashboard/AdminPanel.tsx"
import Profile from "./pages/dashboard/Profile.tsx"

const App = () => {
  return (
    <BrowserRouter>
      
      <Routes>
        <Route path="/" element={<Hello />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
      
    </BrowserRouter>
  );
}

export default App;
