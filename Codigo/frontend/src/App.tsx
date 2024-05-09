import Layout from "./Layout/Layout";
import { BrowserRouter as Router } from "react-router-dom";
import "./styles/global.css";

export const App: React.FC = () => {
  return (
    <Router>
        <Layout />
    </Router>
  );
}
