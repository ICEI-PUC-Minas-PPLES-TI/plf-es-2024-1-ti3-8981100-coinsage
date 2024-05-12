import "./styles/global.css";

import { BrowserRouter as Router } from "react-router-dom";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import Layout from "./Layout/Layout";

export const App: React.FC = () => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Router>
        <Layout />
      </Router>
    </LocalizationProvider>
  );
}
