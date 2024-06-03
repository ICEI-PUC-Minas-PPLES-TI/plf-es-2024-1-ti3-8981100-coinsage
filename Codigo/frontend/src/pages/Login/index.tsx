import { Grid, Typography } from '@mui/material';
import LoginForm from '../../components/LoginForm';
import SignUpForm from '../../components/SignInForm';
import styles from './LoginPage.module.css';
import { useEffect, useState } from 'react';
import useAuth from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
    const [form, setForm] = useState<'login' | 'signIn'>('login');

    return (
        <Grid container component="main" className={styles.root} justifyContent="center" alignItems="center" spacing={2}>
            <Grid item xs={12} sm={6} md={4} lg={3} className={styles.image}>
                <div>
                    <Typography component="h1" variant="h3" className={styles.logo}>
                        CoinSage
                    </Typography>
                    <Typography component="h2" variant="h5" className={styles.tagline}>
                        Potencializando Decisões Inteligentes de Investimento em Criptomoedas
                    </Typography>
                </div>
            </Grid>
            <Grid item xs={12} sm={8} md={6} lg={4} className={styles.loginFormContainer}>
                {form === 'login' ? <LoginForm formNavigator={setForm}/> : <SignUpForm formNavigator={setForm}/>}
            </Grid>
        </Grid>
    );
}

export default Login;
