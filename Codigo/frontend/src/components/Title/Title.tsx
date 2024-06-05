import styles from './Title.module.css'

interface TitleProps {
  title: string;
  lastUpdate?: string;
  lastUpdateTitle?: boolean;
}

const Title: React.FC<TitleProps> = ({ lastUpdate, title, lastUpdateTitle }) => {
  const formatedDate = lastUpdate ? `${lastUpdate.split(' ')[0].replaceAll('-', '/')} ${lastUpdate.split(' ')[1].split(':').slice(0, 2).join(':')}` : 'Unknown'
  return (
    <div className={styles.titleContainer}>
      <h1 className={styles.title}>{title}</h1>
      {lastUpdate && <span className={styles.text}>{lastUpdateTitle ? 'Última análise: ' : ''}{formatedDate}</span>}
    </div>
  );
}

export default Title;
