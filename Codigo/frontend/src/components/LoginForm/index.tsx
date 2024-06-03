import React, { useEffect, useState } from 'react';
import LoadingButton from '@mui/lab/LoadingButton';
import { TextField, Typography, Box, Link as MuiLink } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';

import styles from './LoginForm.module.css';
import { Endpoints } from "../../constants/apiConfig.json";
import ProfilePic from '../Header/ProfilePic';
import api from "../../service/api";

export interface LoginFormProps {
  formNavigator: (form: 'login' | 'signIn') => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ formNavigator }) => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const navigate = useNavigate();

  const loginUser = async () => {
    setLoading(true);
    const formData = new URLSearchParams();
    formData.append('username', email ?? '');
    formData.append('password', password ?? '');

    api.post(`${Endpoints.Login}`, formData
    ).then((response: any) => {
      const data = response.data;
      if (data) {
        window.localStorage.setItem('token', data);
        navigate('/')
      }
    }).catch((error) => {
      if (error.response?.status === 400)
        setError("Erro ao fazer login, tente novamente em alguns minutos");
      else if (error.response?.status === 404)
        setError("Usuário ou senha inválidos");

    }).finally(() => {
      setLoading(false);
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loginUser();
  };

  return (
    <Box className={styles.container}>
      <Box className={styles.logoContainer}>
        <ProfilePic size={120} />
      </Box>
      <Typography component="h1" variant="h5" className={styles.header}>
        Login
      </Typography>
      <form className={styles.form} onSubmit={handleSubmit}>
        <TextField
          disabled={loading}
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="email"
          label="E-mail"
          name="email"
          autoComplete="email"
          autoFocus
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          disabled={loading}
          variant="outlined"
          margin="normal"
          required
          fullWidth
          name="password"
          label="Senha"
          type="password"
          id="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <LoadingButton
          style={{
            backgroundColor: 'black',
            color: 'white',
            margin: '1rem 0'
          }}
          type="submit"
          fullWidth
          variant="contained"
          color="inherit"
          className={styles.submit}
          loading={loading}
        >
          Fazer login
        </LoadingButton>
        {error && <Typography variant="body2" color="error" align="center">{error}</Typography>}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          width: '100%',
        }}>
          <Typography variant="body2" color="textSecondary" align="center" style={{ marginTop: '1rem' }}>
            Primeira vez na CoinSage?
          </Typography>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            marginTop: '0.5rem'
          }}>
            <MuiLink href="#" onClick={() => formNavigator('signIn')}>Criar uma conta</MuiLink>
            <Link to="/analise">Navegar sem fazer login</Link>
          </div>
        </div>
      </form>
    </Box>
  );
};

export default LoginForm;
