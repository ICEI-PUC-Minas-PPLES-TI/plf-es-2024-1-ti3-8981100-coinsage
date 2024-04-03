import styles from './Title.module.css'

export function Title() {
  return(
    <div>
      <h1 className={styles.title}>Balanceamento inicial</h1>
      <p className={styles.title}>Última análise: 16/03/2024 às 20:54</p>
    </div>
  );
}