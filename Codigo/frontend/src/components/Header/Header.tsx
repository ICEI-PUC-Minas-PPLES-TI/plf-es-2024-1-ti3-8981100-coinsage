import { Link, useLocation } from 'react-router-dom';
import styles from './Header.module.css'
import ProfilePic from './ProfilePic';


const Header: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string[]) => {
    return path.includes(location.pathname) ? styles.linkActive : styles.linkNotActive
  }

  return(
    <>
      <header className={styles.header}>
        <h1>CoinSage</h1>
        <div className={styles.links}>
          <Link to="/" className={isActive(['/', '/analise'])}>Análise</Link>
          <Link to="/carteira" className={isActive(['/carteira'])}>Carteira</Link>
          <ProfilePic />
        </div>
      </header>
    </>
  );
}

export default Header;
