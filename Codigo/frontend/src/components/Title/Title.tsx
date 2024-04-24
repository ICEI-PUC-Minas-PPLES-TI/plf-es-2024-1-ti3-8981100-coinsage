import styles from './Title.module.css'

interface TitleProps {
  lastUpdate: string;
}

const Title: React.FC<TitleProps> = ({ lastUpdate }) => {
  return(
    <div>
      <h1 className={styles.title}>Balanceamento inicial</h1>
      <p className={styles.text}>Última análise: {lastUpdate}</p>
    </div>
  );
}

export default Title;