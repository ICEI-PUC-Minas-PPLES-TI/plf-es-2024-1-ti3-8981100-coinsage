import { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode'

const useAuth = () => {
    const token = localStorage.getItem('token');
    return !!token;
};

export default useAuth;

const useUserDetails = () => {
    const [userName, setUserName] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token && token !== 'undefined') {
            const data = jwtDecode(token);
            // @ts-ignore
            const name = data?.name;
            setUserName(name);
        }
    }, []);

    return { userName};
}

export { useUserDetails };
