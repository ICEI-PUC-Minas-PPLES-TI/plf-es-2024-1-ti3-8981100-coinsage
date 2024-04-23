import React, { useEffect, useState } from 'react'
import { Fade, Zoom } from '@mui/material';
import titleStyles from '../../components/Title/Title.module.css'
import Title from '../../components/Title/Title'
// import  DownloadButton  from '../../components/DownloadButton'
import CustomPaginationActionsTable from '../../components/Tabela/Tabela'
import styles from './Balanceamento.module.css'
import { Endpoints } from '../../constants/apiConfig.json'
import api from '../../service/api'
import { Box, LinearProgress } from '@mui/material'

const LoadingTableComponent: React.FC = () => {
  const [loadingText, setLoadingText] = useState<string>('Carregando dados da última análise...');

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingText((prev) => {
        if (prev === 'Carregando dados da última análise...') {
          return 'Por favor, aguarde...';
        } else {
          return 'Carregando dados da última análise...';
        }
      });
    }, 1200);

    return () => clearInterval(interval);
  })


  return (
    <>
      <h1 className={titleStyles.title}>{loadingText}</h1>
      <Box sx={{ width: '100%' }}>
        <LinearProgress />
      </Box>
    </>
  );
}

const Balanceamento: React.FC = () => {
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [tableData, setTableData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  // useEffect(() => {
  //   setLoading(true);
  //   api
  //     .get(Endpoints.FirstStage)
  //     .then((response: any) => {
  //       if (response.status >= 200 && response.status < 300) {
  //         const data = response.data;
  //         if (data) {
  //           setLastUpdate(data.last_update.time);
  //           setTableData(data.last_update.data.data);
  //         } else {
  //           console.log('ERROR USUARIO NAO CADASTRADO');
  //         }
  //       } else {
  //         console.log('ERROR AO OBTER');
  //       }
  //     })
  //     .catch(() => {
  //       console.log('ULTIMO ERROR AO OBTER');
  //     })
  //     .finally(() => {
  //       setLoading(false);
  //     })
  // }, []);

  return (
    <div className={styles.content}>
      {/* {loading ?
        <>
          <LoadingTableComponent />
        </>
        :
        <>
          <Title lastUpdate={lastUpdate} />
        </>
      } */}
      <CustomPaginationActionsTable />
    </div>
  )
}

export default Balanceamento;
