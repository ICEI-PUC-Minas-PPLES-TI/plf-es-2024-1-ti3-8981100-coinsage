import React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import styles from './Tabela.module.css';
import LogoSymbol from './Logo/LogoSymbol';
import TextColoredCondition from './TextColoredCondition/TextColoredCondition';

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
  ema_aligned: boolean;
}

interface TabelaProps {
  tableData: TableData[];
}

const Tabela: React.FC<TabelaProps> = ({ tableData=[] }) => {
  const areEmasAligned = (value: boolean) => value === true ? 'SIM' : (value === false ? 'NÃO' : '-')

  const columns: GridColDef[] = [
    { field: 'setor', headerName: 'Setor', flex: 1 },
    {
      field: 'cripto',
      headerName: 'Cripto',
      width: 160,
      renderCell: (params) => (
        <LogoSymbol logo={params.row.currency.logo} symbol={params.row.currency.symbol} />
      ),
    },
    { field: 'valorizacao', headerName: '% Valorização', flex: 1 },
    { field: 'preco', headerName: 'Preço na Avaliação', flex: 1 },
    {
      field: 'emas',
      headerName: 'EMAs (d) Alinhados',
      renderCell: (params) => (
        <TextColoredCondition value={params.row.ema_aligned} conditionFn={areEmasAligned} />
      )
    },
    { field: 'dataValorizacaoVolume', headerName: 'Data Valorização Volume (d)', flex: 1 },
    { field: 'quantidadeVolumeValorizacao', headerName: 'Quantidade Volume Valorização', flex: 1 },
    { field: 'quantidadeVolumeDiaAnterior', headerName: 'Quantidade Volume Dia Anterior', flex: 1 },
    { field: 'percentDiaAnterior', headerName: '% Dia/Dia Anterior', flex: 1 },
    { field: 'ema8', headerName: 'EMA8 (s)', flex: 1 },
  ];

  const rows = tableData.map((data, index) => ({
    id: index + 1,
    setor: data.currency.main_sector.title,
    cripto: '',
    valorizacao: `${data.week_increase_percentage}%`,
    preco: `${data.closing_price}`,
    emas: '',
    dataValorizacaoVolume: data.valorization_date,
    quantidadeVolumeValorizacao: `${data.open_price}`,
    quantidadeVolumeDiaAnterior: `${data.last_week_closing_price}`,
    percentDiaAnterior: `${((data.open_price - data.last_week_closing_price) / data.last_week_closing_price * 100).toFixed(2)}%`,
    ema8: data.ema8 ? data.ema8.toString() : "N/A",
    currency: data.currency,
    ema_aligned: data.ema_aligned,
  }));

  return (
    <div className={styles.datagrid}>
      <DataGrid rows={rows} columns={columns}/>
    </div>
  );
};

export default Tabela;
