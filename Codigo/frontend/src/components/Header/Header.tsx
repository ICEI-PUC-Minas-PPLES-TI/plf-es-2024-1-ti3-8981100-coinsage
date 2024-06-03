import { Link, useLocation } from 'react-router-dom';
import styles from './Header.module.css'
import useAuth from '../../hooks/useAuth';
import ProfileMenu from './ProfileMenu';


const Header: React.FC = () => {
  const isUserLoggedIn = useAuth();
  const location = useLocation();

  const isActive = (path: string[]) => {
    return path.includes(location.pathname) ? styles.linkActive : styles.linkNotActive
  }

  return (
    <>
      <header className={styles.header}>
        <h1>CoinSage</h1>
        <div className={styles.links}>
          <Link to="/" className={isActive(['/', '/analise'])}>Análise</Link>
          {isUserLoggedIn ? (
            <>
              <Link to="/carteira" className={isActive(['/carteira'])}>Carteira</Link>
              <ProfileMenu />
            </>
          ) : (
            <Link to="/login" className={isActive(['/login'])}>Fazer Login</Link>
          )}
        </div>
      </header>
    </>
  );
}

export default Header;
