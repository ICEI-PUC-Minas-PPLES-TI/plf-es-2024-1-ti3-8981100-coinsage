import React, { useEffect, useState } from 'react'
import Title from '../../components/Title/Title'
// import  DownloadButton  from '../../components/DownloadButton'
import Tabela from '../../components/Tabela/Tabela'
import styles from './Balanceamento.module.css'
import { Endpoints } from '../../constants/apiConfig.json'
import api from '../../service/api'

// interface Currency {
//   symbol: string;
//   uuid: string;
//   logo: string;
//   main_sector: {
//     uuid: string;
//     title: string;
//   };
// }

// interface DataItem {
//   currency: Currency;
//   week_increase_percentage: number;
//   valorization_date: string;
//   closing_price: number;
//   open_price: number;
//   last_week_closing_price: number;
//   ema8: number;
//   ema8_greater_open: boolean;
//   ema8_less_close: boolean;
// }

// interface LastUpdate {
//   time: string;
//   data: {
//     page: number;
//     total: number;
//     remaining: number;
//     data: DataItem[];
//   };
// }

// interface ApiResponse {
//   next_update: string;
//   last_update: LastUpdate;
// }

const Balanceamento: React.FC = () => {
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [tableData, setTableData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    api
      .get(Endpoints.FirstStage)
      .then((response: any) => {
        if (response.status >= 200 && response.status < 300) {
          const data = response.data;
          if (data) {
            setLastUpdate(data.last_update.time);
            setTableData(data.last_update.data.data);
            console.log(response.data);
          } else {
            console.log('ERROR USUARIO NAO CADASTRADO');
          }
        } else {
          console.log('ERROR AO OBTER');
        }
      })
      .catch(() => {
        console.log('ULTIMO ERROR AO OBTER');
      })
      .finally(() => {
        setLoading(false);
      })
  }, []);

  return (
    <div className={styles.content}>
      {loading ? <h1>Carregando...</h1>
        :
        <>
          <Title lastUpdate={lastUpdate} />
          <Tabela tableData={tableData} />
        </>
      }
    </div>
  )
}

export default Balanceamento;
