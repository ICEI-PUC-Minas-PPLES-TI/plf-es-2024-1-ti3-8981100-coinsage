import styles from './Header.module.css'


export function Header() {
  return(
    <div>
      <header className={styles.header}>
        <h1>CoinSage</h1>
      </header>
    </div>
  );
}