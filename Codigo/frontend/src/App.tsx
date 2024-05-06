import "./styles/global.css";
import Analise from "./pages/Analise/Analise";
import Layout from "./Layout/Layout";


export const App: React.FC = () => {
  return (
    <Layout>
      <Analise />
    </Layout>
  );
}
