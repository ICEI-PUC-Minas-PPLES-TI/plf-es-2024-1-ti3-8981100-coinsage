import React from 'react'
import  Title  from '../../components/Title/Title'
import  DownloadButton  from '../../components/DownloadButton/DownloadButton'
import styles from './Balanceamento.module.css'
import { DataGrid, GridColDef } from '@mui/x-data-grid'

const columns: GridColDef<(typeof rows)[number]>[] = [
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

const rows = [
  { id: 1, lastName: 'Snow', firstName: 'Jon', age: 14 },
  { id: 2, lastName: 'Lannister', firstName: 'Cersei', age: 31 },
  { id: 3, lastName: 'Lannister', firstName: 'Jaime', age: 31 },
  { id: 4, lastName: 'Stark', firstName: 'Arya', age: 11 },
  { id: 5, lastName: 'Targaryen', firstName: 'Daenerys', age: null },
  { id: 6, lastName: 'Melisandre', firstName: null, age: 150 },
  { id: 7, lastName: 'Clifford', firstName: 'Ferrara', age: 44 },
  { id: 8, lastName: 'Frances', firstName: 'Rossini', age: 36 },
  { id: 9, lastName: 'Roxie', firstName: 'Harvey', age: 65 },
];

const Balanceamento: React.FC = () => {
  return (
    <div className={styles.content}>
      <Title />
      <div className={styles.datagrid}>
        <DataGrid
          rows={rows}
          columns={columns}
        />
      </div>

    </div>

  )
}

export default Balanceamento;