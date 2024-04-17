import React from 'react'
import { DataGrid, GridColDef } from '@mui/x-data-grid'
import styles from './Tabela.module.css'

interface TableData {
  currency: {
    symbol: string;
    uuid: string;
    logo: string;
    main_sector: {
      uuid: string;
      title: string;
    };
  };
  week_increase_percentage: number;
  valorization_date: string;
  closing_price: number;
  open_price: number;
  last_week_closing_price: number;
  ema8: number;
  ema8_greater_open: boolean;
  ema8_less_close: boolean;
}

interface TabelaProps {
  tableData: TableData[];
}




const Tabela: React.FC<TabelaProps> = ({ tableData }) => {
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
  const rows = tableData.map((data, index) => ({
    id: index + 1,
    setor: data.currency.main_sector.title,
    cripto: data.currency.symbol,
    ranking: index + 1,
    valorizacao: `${data.week_increase_percentage}%`,
    preco: `${data.closing_price}`,
    emas: data.ema8_greater_open && data.ema8_less_close ? 'SIM' : 'NÃO',
    dataValorizacaoVolume: new Date(data.valorization_date).toLocaleDateString(),
    quantidadeVolumeValorizacao: `${data.open_price}`,
    quantidadeVolumeDiaAnterior: `${data.last_week_closing_price}`,
    percentDiaAnterior: `${((data.open_price - data.last_week_closing_price) / data.last_week_closing_price * 100).toFixed(2)}%`,
    ema8: data.ema8.toString(),
  }));

  return (
    <div className={styles.datagrid}>
        <DataGrid
          rows={rows}
          columns={columns}
        />
      </div>

  )
}

export default Tabela;
