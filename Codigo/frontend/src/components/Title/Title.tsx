import styles from './Title.module.css'

const Title: React.FC = () => {
  return(
    <div>
      <h1 className={styles.title}>Balanceamento inicial</h1>
      <p className={styles.text}>Última análise: 16/03/2024 às 20:54</p>
    </div>
  );
}

export default Title;