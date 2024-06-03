import "./styles/global.css";

import { BrowserRouter as Router } from "react-router-dom";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import Layout from "./Layout/Layout";
import { createContext, useState } from "react";

export const ShowHeaderContext = createContext<boolean>(true);

export const App: React.FC = () => {
  const [showHeader, setShowHeader] = useState<boolean>(true);

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Router>
        <ShowHeaderContext.Provider value={showHeader}>
          <Layout/>
        </ShowHeaderContext.Provider>
      </Router>
    </LocalizationProvider>
  );
}
