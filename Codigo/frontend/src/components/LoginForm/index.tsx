import React, { useState } from 'react';
import { TextField, Button, Checkbox, FormControlLabel, Typography, Box, Link as MuiLink } from '@mui/material';
import styles from './LoginForm.module.css';
import ProfilePic from '../Header/ProfilePic';
import { Link, useNavigate } from 'react-router-dom';

export interface LoginFormProps {
  formNavigator: (form: 'login' | 'signIn') => void;
}

const LoginForm: React.FC<LoginFormProps> = ({formNavigator}) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    window.localStorage.setItem('token', '1234');
    navigate('/')
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
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="email"
          label="Nome do usuário ou e-mail"
          name="email"
          autoComplete="email"
          autoFocus
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
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
        <Button
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
        >
          Fazer login
        </Button>
        <Typography variant="body2" color="textSecondary" align="center" style={{ marginTop: '1rem' }}>
          Primeira vez na CoinSage?
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            marginTop: '0.5rem'
          }}>
            <MuiLink href="#" onClick={() => formNavigator('signIn')}>Criar uma conta</MuiLink>
            <Link to="/analise">Navegar sem fazer login</Link>
          </div>
        </Typography>
      </form>
    </Box>
  );
};

export default LoginForm;
