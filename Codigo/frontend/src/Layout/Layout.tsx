import React from 'react'
import styles from './Layout.module.css'
import Header from '../components/Header/Header'
import Footer from '../components/Footer/Footer';

interface ILayout {
  children: React.ReactNode;
}

const Layout: React.FC<ILayout> = ({ children }) => {
  return (
    <>
      <div className={styles.headerFixed}>
        <Header />
      </div>

      <div className={styles.content}>
        {children}
      </div>

      <div className={styles.footerFixed}>
        <Footer />
      </div>
    </>

  )
}

export default Layout;
