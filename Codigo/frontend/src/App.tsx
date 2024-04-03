import { Header } from "./components/Header/Header";
import { Title } from "./components/Title/Title";
import { DownloadButton } from './components/DownloadButton/DownloadButton';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

import "./styles/global.css";
import styles from "./App.module.css";
import React, { useState } from 'react';


export function App() {
  const [rows, setRows] = useState<any[]>([]);

const columns: GridColDef[] = [
{ field: 'setor', headerName: 'Setor', width: 150 },
{ field: 'cripto', headerName: 'Cripto', width: 150 },
{ field: 'ranking', headerName: 'Ranking', width: 150 },
{ field: 'valorizacao', headerName: '% Valorização', width: 180 },
{ field: 'preco', headerName: 'Preço Agora', width: 150 },
{ field: 'emas', headerName: 'EMAs (d) Alinhados', width: 200 },
{ field: 'dataValorizacaoVolume', headerName: 'Data Valorização Volume (d)', width: 250 },
{ field: 'quantidadeVolumeValorizacao', headerName: 'Quantidade Volume Valorização', width: 280 },
{ field: 'quantidadeVolumeDiaAnterior', headerName: 'Quantidade Volume Dia Anterior', width: 280 },
{ field: 'percentDiaAnterior', headerName: '% Dia/Dia Anterior', width: 250 },
{ field: 'ema8', headerName: 'EMA8 (s)', width: 150 },
];

  return (
    <div>
      <Header />
      <Title/>
      <DownloadButton/>
      <div style={{ marginLeft: '10px', marginTop: '20px' }}>
        <h2>Estágio 1</h2>
      </div>
            <DataGrid
                columns={columns}
                rows={rows}
                rowHeight={38}
                disableRowSelectionOnClick 
                autoHeight
            />
    </div>
  );
}