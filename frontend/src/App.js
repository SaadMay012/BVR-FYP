import './App.css';
import Singup from './singup/singup.jsx';
import Login from './login/login.jsx';
import AudioUploader from './audio-ploader.js';

import { RouterProvider, createBrowserRouter } from "react-router-dom";

function App() {
  const route = createBrowserRouter([
    {
      path: "/",
      element: <Singup />,
    },
    {
      path: "/login",
      element: <Login />,
    },
  ]);
  return (
    <div className="App">
      <AudioUploader/>
      <RouterProvider router={route}></RouterProvider>
    </div>
  );
}

export default App;