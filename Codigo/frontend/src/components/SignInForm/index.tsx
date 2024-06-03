import React, { useState } from 'react';
import { TextField, Button, Typography, Box, Link as MuiLink } from '@mui/material';
import styles from './SignInForm.module.css';
import ProfilePic from '../Header/ProfilePic';
import { Link } from 'react-router-dom';
import { LoginFormProps } from '../LoginForm';
import api from "../../service/api";
import { Endpoints } from "../../constants/apiConfig.json";
import { LoadingButton } from '@mui/lab';

const SignUpForm: React.FC<LoginFormProps> = ({ formNavigator }) => {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [emailInvalid, setEmailInvalid] = useState<boolean>(false);
  const [passwordInvalid, setPasswordInvalid] = useState<boolean>(false);
  const [confirmPasswordInvalid, setConfirmPasswordInvalid] = useState<boolean>(false);

  const signUpUser = async () => {
    setLoading(true);

    api.post(`${Endpoints.SignUp}`, {
      email: email,
      name: name,
      password: password,
    }
    ).then((response: any) => {
      const data = response.data;
      if (data) {
        window.localStorage.setItem('token', data);
        formNavigator('login');
      }
    }).catch((error) => {
      if (error.response?.status !== 200)
        setError("Erro ao criar conta, tente novamente em alguns minutos");
    }).finally(() => {
      setLoading(false);
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!emailInvalid && !passwordInvalid && !confirmPasswordInvalid){
      setError(null);
      signUpUser();
      return
    }

    setError("Preencha os campos corretamente");
  };

  // @ts-ignore
  const handleEmailFormat: boolean = (value: string) => {
    setEmail(value);
    if (value === '') {
      setEmailInvalid(false);
      return false;
    }
    const pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (value.match(pattern)) {
      setEmailInvalid(false);
      return false;
    }
    setEmailInvalid(true);
    return true;
  }

  // @ts-ignore
  const handlePasswordFormat: boolean = (value: string) => {
    setPassword(value);
    if (value === '') {
      setPasswordInvalid(false);
      return false;
    }
    if (value.length >= 6) {
      setPasswordInvalid(false);
      return false;
    }
    setPasswordInvalid(true);
    return true;
  }

  // @ts-ignore
  const handlePasswordMatch = (value: string) => {
    setConfirmPassword(value);
    if (value === password) {
      setConfirmPasswordInvalid(false);
      return false;
    }
    setConfirmPasswordInvalid(true);
    return true;
  }

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
          error={emailInvalid}
          helperText={emailInvalid ? "E-mail inválido" : ""}
          // @ts-ignore
          onChange={(e) => handleEmailFormat(e.target.value)}
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
          error={name === ''}
          helperText={name === '' ? "Nome é obrigatório" : ""}
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
          error={passwordInvalid}
          helperText={passwordInvalid ? "Senha precisa ter no mínimo 6 caracteres" : ""}
          // @ts-ignore
          onChange={(e) => handlePasswordFormat(e.target.value)}
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
          error={confirmPasswordInvalid}
          helperText={confirmPasswordInvalid ? "Senhas não conferem" : ""}
          // @ts-ignore
          onChange={(e) => handlePasswordMatch(e.target.value)}
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
          Criar conta
        </LoadingButton>
        {error && <Typography variant="body2" color="error" align="center">{error}</Typography>}
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

export default SignUpForm;
