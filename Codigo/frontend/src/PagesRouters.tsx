import { Routes, Route, Navigate } from "react-router-dom";
import Analise from "./pages/Analise/Analise";
import NotFoundPage from "./pages/NotFoundPage";
import Carteira from "./pages/Carteira";
import EditarCarteira from "./pages/Carteira/Editar";
import Login from "./pages/Login";
import ProtectedRoute from "./ProtectedRoute";
import useAuth from "./hooks/useAuth";

const PagesRouters: React.FC = () => {
    const isAuthenticated = useAuth();

    return (
        <Routes>
            <Route element={<Analise />} path="/" />
            <Route element={
                <>
                    {isAuthenticated ? <Navigate to="/" /> : <Login />}
                </>
            } path="/login" />
            <Route element={<Analise />} path="/analise" />
            <Route element={
                <ProtectedRoute>
                    <Carteira />
                </ProtectedRoute>
            } path="/carteira" />
            <Route element={
                <ProtectedRoute>
                    <EditarCarteira />
                </ProtectedRoute>
            } path="/carteira/editar" />
            <Route element={<NotFoundPage />} path="*" />
        </Routes>
    )
}

export default PagesRouters;
