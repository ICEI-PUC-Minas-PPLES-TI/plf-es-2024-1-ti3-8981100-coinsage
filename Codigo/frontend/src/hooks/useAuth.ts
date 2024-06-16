import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'

const useAuth = () => {
    const token = localStorage.getItem('token');
    return !!token;
};

const useSessionExpired = () => {
    const token = localStorage.getItem('token');
    if (token && token !== 'undefined') {
        const data = jwtDecode(token);
        // @ts-ignore
        return Date.now() >= data?.exp * 1000;
    }
    return true;
}

const useUserDetails = () => {
    const [userName, setUserName] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token && token !== 'undefined') {
            if (useSessionExpired()) {
                localStorage.removeItem('token');
                return;
            }
            const data = jwtDecode(token);
            // @ts-ignore
            const name = data?.name;
            setUserName(name);
        }
    }, []);

    return { userName};
}

export default useAuth;
export { useUserDetails, useSessionExpired };
