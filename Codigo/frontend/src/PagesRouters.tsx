import { Routes, Route } from "react-router-dom";
import Analise from "./pages/Analise/Analise";
import NotFoundPage from "./pages/NotFoundPage";
import Carteira from "./pages/Carteira";
import EditarCarteira from "./pages/Carteira/Editar";

const PagesRouters: React.FC = () => {
    return (
        <Routes>
            <Route element={<Analise />} path="/" />
            <Route element={<Analise />} path="/analise" />
            <Route element={<Carteira />} path="/carteira" />
            <Route element={<EditarCarteira />} path="/carteira/editar" />
            <Route element={<NotFoundPage />} path="*" />
        </Routes>
    )
}

export default PagesRouters;
