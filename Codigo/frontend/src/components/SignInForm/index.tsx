import React, { useState } from 'react';
import { TextField, Button, Checkbox, FormControlLabel, Typography,  Box, Link as MuiLink } from '@mui/material';
import styles from './SignInForm.module.css';
import ProfilePic from '../Header/ProfilePic';
import { Link } from 'react-router-dom';
import { LoginFormProps } from '../LoginForm';

const SignInForm: React.FC<LoginFormProps> = ({formNavigator}) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // criar conta
    formNavigator('login');
  };

  return (
    <Box className={styles.container}>
      <Box className={styles.logoContainer}>
        <ProfilePic size={120} />
      </Box>
      <Typography component="h1" variant="h5" className={styles.header}>
        Criar conta
      </Typography>
      <form className={styles.form} onSubmit={handleSubmit}>
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          id="email"
          label="Email"
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
          id="name"
          label="Nome"
          name="name"
          autoComplete="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
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
        <TextField
          variant="outlined"
          margin="normal"
          required
          fullWidth
          name="password"
          label="Confirmar senha"
          type="password"
          id="password"
          autoComplete="current-password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
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
          Criar conta
        </Button>
        <Typography variant="body2" color="textSecondary" align="center" style={{ marginTop: '1rem' }}>
          Já possui uma conta?
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            marginTop: '0.5rem'
          }}>
            <MuiLink href="#" onClick={() => formNavigator('login')}>Fazer login</MuiLink>
            <Link to="/analise">Navegar sem fazer login</Link>
          </div>
        </Typography>
      </form>
    </Box>
  );
};

export default SignInForm;
