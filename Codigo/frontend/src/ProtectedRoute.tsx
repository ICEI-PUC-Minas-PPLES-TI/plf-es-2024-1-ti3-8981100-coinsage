import { Route, Navigate } from 'react-router-dom';
import useAuth from './hooks/useAuth';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const isAuthenticated = useAuth();

    return (
        <>
            {isAuthenticated ? children : <Navigate to="/login" />}
        </>
    );
}

export default ProtectedRoute;
