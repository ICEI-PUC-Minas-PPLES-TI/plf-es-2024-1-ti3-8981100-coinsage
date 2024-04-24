import styles from './Title.module.css'
import { format } from "date-fns";
import React from "react";

interface TitleProps {
  lastUpdate: string;
}

const Title: React.FC<TitleProps> = ({ lastUpdate }) => {
  console.log("Valor de lastUpdate", lastUpdate);
  const parts = lastUpdate.split('-');
  const formattedDate = parts.join('/');

  return(
    <div>
      <h1 className={styles.title}>Balanceamento inicial</h1>
      <p className={styles.text}>Última análise: {formattedDate}</p>
    </div>
  );
}

export default Title;