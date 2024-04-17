import "./styles/global.css";
import Balanceamento from "./pages/Balanceamento/Balanceamento";
import Layout from "./layout/Layout";


export const App: React.FC = () => {
  return (
    <Layout>
      <Balanceamento />
    </Layout>
  );
}