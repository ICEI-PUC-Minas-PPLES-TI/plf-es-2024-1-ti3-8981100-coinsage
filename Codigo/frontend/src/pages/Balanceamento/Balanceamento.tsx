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
  { id: 1, setor: 'Bitcoin', cripto: 'Bitcoin', ranking: 1, valorizacao: '10%', preco: '$50,000', emas: 'SIM', dataValorizacaoVolume: '01/04/2024', quantidadeVolumeValorizacao: '$10,000', quantidadeVolumeDiaAnterior: '$8,000', percentDiaAnterior: '25%', ema8: 'SIM' },
  { id: 2, setor: 'Ethereum', cripto: 'Ethereum', ranking: 2, valorizacao: '8%', preco: '$2,000', emas: 'NÃO', dataValorizacaoVolume: '02/04/2024', quantidadeVolumeValorizacao: '$8,000', quantidadeVolumeDiaAnterior: '$7,500', percentDiaAnterior: '10%', ema8: 'NÃO' },
  { id: 3, setor: 'Ripple', cripto: 'Ripple', ranking: 3, valorizacao: '12%', preco: '$2', emas: 'SIM', dataValorizacaoVolume: '03/04/2024', quantidadeVolumeValorizacao: '$5,000', quantidadeVolumeDiaAnterior: '$6,000', percentDiaAnterior: '-20%', ema8: 'SIM' },
  { id: 4, setor: 'Cardano', cripto: 'Cardano', ranking: 4, valorizacao: '15%', preco: '$1.5', emas: 'NÃO', dataValorizacaoVolume: '04/04/2024', quantidadeVolumeValorizacao: '$6,000', quantidadeVolumeDiaAnterior: '$5,500', percentDiaAnterior: '9%', ema8: 'NÃO' },
  { id: 5, setor: 'Litecoin', cripto: 'Litecoin', ranking: 5, valorizacao: '5%', preco: '$150', emas: 'SIM', dataValorizacaoVolume: '05/04/2024', quantidadeVolumeValorizacao: '$3,000', quantidadeVolumeDiaAnterior: '$3,500', percentDiaAnterior: '-14%', ema8: 'SIM' },
  { id: 6, setor: 'Polkadot', cripto: 'Polkadot', ranking: 6, valorizacao: '20%', preco: '$40', emas: 'NÃO', dataValorizacaoVolume: '06/04/2024', quantidadeVolumeValorizacao: '$4,000', quantidadeVolumeDiaAnterior: '$3,000', percentDiaAnterior: '33%', ema8: 'NÃO' },
  { id: 7, setor: 'Bitcoin Cash', cripto: 'Bitcoin Cash', ranking: 7, valorizacao: '18%', preco: '$500', emas: 'SIM', dataValorizacaoVolume: '07/04/2024', quantidadeVolumeValorizacao: '$7,000', quantidadeVolumeDiaAnterior: '$6,500', percentDiaAnterior: '8%', ema8: 'SIM' },
  { id: 8, setor: 'Chainlink', cripto: 'Chainlink', ranking: 8, valorizacao: '22%', preco: '$30', emas: 'NÃO', dataValorizacaoVolume: '08/04/2024', quantidadeVolumeValorizacao: '$5,500', quantidadeVolumeDiaAnterior: '$6,000', percentDiaAnterior: '-8%', ema8: 'NÃO' },
  { id: 9, setor: 'Stellar', cripto: 'Stellar', ranking: 9, valorizacao: '25%', preco: '$0.5', emas: 'SIM', dataValorizacaoVolume: '09/04/2024', quantidadeVolumeValorizacao: '$6,000', quantidadeVolumeDiaAnterior: '$5,000', percentDiaAnterior: '20%', ema8: 'SIM' },
  { id: 10, setor: 'Dogecoin', cripto: 'Dogecoin', ranking: 10, valorizacao: '30%', preco: '$0.1', emas: 'NÃO', dataValorizacaoVolume: '10/04/2024', quantidadeVolumeValorizacao: '$8,000', quantidadeVolumeDiaAnterior: '$9,000', percentDiaAnterior: '-11%', ema8: 'NÃO' },
  { id: 11, setor: 'Bitcoin SV', cripto: 'Bitcoin SV', ranking: 11, valorizacao: '28%', preco: '$200', emas: 'SIM', dataValorizacaoVolume: '11/04/2024', quantidadeVolumeValorizacao: '$9,000', quantidadeVolumeDiaAnterior: '$8,500', percentDiaAnterior: '6%', ema8: 'SIM' },
  { id: 12, setor: 'EOS', cripto: 'EOS', ranking: 12, valorizacao: '32%', preco: '$3', emas: 'NÃO', dataValorizacaoVolume: '12/04/2024', quantidadeVolumeValorizacao: '$9,500', quantidadeVolumeDiaAnterior: '$10,000', percentDiaAnterior: '-5%', ema8: 'NÃO' },
  { id: 13, setor: 'TRON', cripto: 'TRON', ranking: 13, valorizacao: '35%', preco: '$0.03', emas: 'SIM', dataValorizacaoVolume: '13/04/2024', quantidadeVolumeValorizacao: '$7,500', quantidadeVolumeDiaAnterior: '$7,000', percentDiaAnterior: '7%', ema8: 'SIM' },
  { id: 14, setor: 'Tezos', cripto: 'Tezos', ranking: 14, valorizacao: '38%', preco: '$5', emas: 'NÃO', dataValorizacaoVolume: '14/04/2024', quantidadeVolumeValorizacao: '$8,500', quantidadeVolumeDiaAnterior: '$9,500', percentDiaAnterior: '-11%', ema8: 'NÃO' },
  { id: 15, setor: 'Monero', cripto: 'Monero', ranking: 15, valorizacao: '40%', preco: '$100', emas: 'SIM', dataValorizacaoVolume: '15/04/2024', quantidadeVolumeValorizacao: '$8,500', quantidadeVolumeDiaAnterior: '$8,000', percentDiaAnterior: '6%', ema8: 'SIM' },
  { id: 16, setor: 'VeChain', cripto: 'VeChain', ranking: 16, valorizacao: '42%', preco: '$0.2', emas: 'NÃO', dataValorizacaoVolume: '16/04/2024', quantidadeVolumeValorizacao: '$10,500', quantidadeVolumeDiaAnterior: '$11,000', percentDiaAnterior: '-4%', ema8: 'NÃO' },
  { id: 17, setor: 'Neo', cripto: 'Neo', ranking: 17, valorizacao: '45%', preco: '$10', emas: 'SIM', dataValorizacaoVolume: '17/04/2024', quantidadeVolumeValorizacao: '$10,000', quantidadeVolumeDiaAnterior: '$10,500', percentDiaAnterior: '-5%', ema8: 'SIM' },
  { id: 18, setor: 'Cosmos', cripto: 'Cosmos', ranking: 18, valorizacao: '48%', preco: '$15', emas: 'NÃO', dataValorizacaoVolume: '18/04/2024', quantidadeVolumeValorizacao: '$11,500', quantidadeVolumeDiaAnterior: '$12,000', percentDiaAnterior: '-4%', ema8: 'NÃO' },
  { id: 19, setor: 'Zcash', cripto: 'Zcash', ranking: 19, valorizacao: '50%', preco: '$50', emas: 'SIM', dataValorizacaoVolume: '19/04/2024', quantidadeVolumeValorizacao: '$11,000', quantidadeVolumeDiaAnterior: '$11,500', percentDiaAnterior: '-4%', ema8: 'SIM' },
  { id: 20, setor: 'Dash', cripto: 'Dash', ranking: 20, valorizacao: '55%', preco: '$70', emas: 'NÃO', dataValorizacaoVolume: '20/04/2024', quantidadeVolumeValorizacao: '$12,000', quantidadeVolumeDiaAnterior: '$11,500', percentDiaAnterior: '4%', ema8: 'NÃO' },
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
