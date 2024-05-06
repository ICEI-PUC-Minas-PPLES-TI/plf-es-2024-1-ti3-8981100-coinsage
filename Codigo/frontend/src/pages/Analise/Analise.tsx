import React, { useEffect, useState } from "react";
import Title from "../../components/Title/Title";
import CustomPaginationActionsTable from "../../components/Tabela/Tabela";
import styles from "./Analise.module.css";
import { Endpoints } from "../../constants/apiConfig.json";
import api from "../../service/api";
import LoadingTableComponent from "../../components/Tabela/LoadingTableComponent/LoadingTableComponent";
import AnaliseDownloadContainer from "../../components/AnaliseHeader/AnaliseDownloadContainer";


const Analise: React.FC = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [rows, setRows] = useState<any[]>([]);
  const [initialLoading, setInitialLoading] = useState<boolean>(true);
  const [tableLoading, setTableLoading] = useState<boolean>(true);
  const [count, setCount] = useState<number>(0);
  const [lastUpdate, setLastUpdate] = useState<string>("");

  useEffect(() => {
    setTableLoading(true);
    setRows([]);
    api
      .get(
        `${Endpoints.FirstStage}?limit=${rowsPerPage}&offset=${page * rowsPerPage ?? 0
        }`
      )
      .then((response: any) => {
        if (response.status >= 200 && response.status < 300) {
          const data = response.data;
          if (data) {
            setRows(data.last_update.data.data);
            setCount(data.last_update.data.total);
            setLastUpdate(data.last_update.time);
          } else {
            console.log("ERROR USUARIO NAO CADASTRADO");
          }
        } else {
          console.log("ERROR AO OBTER");
        }
      })
      .catch(() => {
        console.log("ULTIMO ERROR AO OBTER");
      })
      .finally(() => {
        setInitialLoading(false);
        setTableLoading(false);
      });
  }, [page, rowsPerPage]);

  return (
    <>
      {!initialLoading &&
        <div className={styles.analyseHeader}>
          <Title title="Análise" lastUpdate={lastUpdate} />
        </div>
      }
      <div className={styles.content}>
        {initialLoading ? (
          <>
            <LoadingTableComponent />
          </>
        ) : (
            <CustomPaginationActionsTable
              rowsRaw={rows}
              page={page}
              setPage={setPage}
              rowsPerPage={rowsPerPage}
              setRowsPerPage={setRowsPerPage}
              count={count}
              tableLoading={tableLoading}
            />
        )}
      </div>
      {!initialLoading &&
        <div className={`${styles.analyseHeader} ${styles.completeLogContainer}`}>
          <Title title="Relatório Completo" />
          <AnaliseDownloadContainer />
        </div>
      }
    </>
  );
};

export default Analise;
