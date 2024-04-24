import axios from 'axios';

const api = axios.create({
  // baseURL: 'http://localhost:8000/'
  baseURL: 'https://coinsage-dev-api.onrender.com'
});

export default api;
