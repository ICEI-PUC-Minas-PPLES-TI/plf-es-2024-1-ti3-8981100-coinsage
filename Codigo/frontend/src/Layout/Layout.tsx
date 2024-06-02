import React, { useContext } from 'react'
import styles from './Layout.module.css'
import Header from '../components/Header/Header'
import Footer from '../components/Footer/Footer';
import PagesRouters from '../PagesRouters';
import { useLocation } from 'react-router-dom';

interface ILayout {
  children?: React.ReactNode;
}

const Layout: React.FC<ILayout> = ({ children }) => {
  const { pathname } = useLocation();
  const showHeader = pathname !== '/login';

  return (
    <>
      {showHeader &&
        <div className={styles.headerFixed}>
          <Header />
        </div>
      }

      <div className={showHeader ? styles.content : ''}>
        <PagesRouters />
      </div>

      <div className={styles.footerFixed}>
        <Footer />
      </div>
    </>

  )
}

export default Layout;
