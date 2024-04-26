import styles from './Footer.module.css'


const Footer: React.FC = () => {
  return (
    <>
      <footer className={styles.footer}>
        <span>All copyrights reserved by</span>
        <h1>CoinSage®</h1>
      </footer>
    </>
  );
}

export default Footer;
