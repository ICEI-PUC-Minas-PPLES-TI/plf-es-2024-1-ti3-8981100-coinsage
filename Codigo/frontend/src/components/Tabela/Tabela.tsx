import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableFooter from "@mui/material/TableFooter";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import { Unstable_Popup as BasePopup } from '@mui/base/Unstable_Popup';
import Paper from "@mui/material/Paper";
import { TableHead } from "@mui/material";
import LogoSymbol from "./Logo/LogoSymbol";
import EmasAlignedCell from "./EmasAlignedCell/EmasAlignedCell";
import { LinearProgress } from "@mui/material";
import TablePaginationActions from "./TablePaginationActions/TablePaginationActions";
import tableStyles from "./Tabela.module.css";
import TextColoredCondition from "./TextColoredCondition/TextColoredCondition";
import { useState } from "react";

interface Column {
  id: string;
  label: string;
  minWidth?: number;
  align?: "right";
  format?: (value: number) => string;
  renderCell?: (params: any) => JSX.Element;
}

const areEmasAligned = (value: boolean) =>
  value === true ? "SIM" : value === false ? "NÃO" : "-";

const columns: readonly Column[] = [
  { id: "setor", label: "Setor" },
  {
    id: "cripto",
    label: "Cripto",
    minWidth: 160,
  },
  { id: "ranking", label: "Ranking" },
  { id: "valorizacao", label: "% Valorização semanal" },
  { id: "emas", label: "EMAs (d) Alinhados" },
  {
    id: "ema8",
    // @ts-ignore
    label: (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <p>EMA8 (s)</p>
        <p>C(s){" > "}EMA8(s){" > "}O(s)</p>
      </div>
    ),
  },
];

const renderLogoSymbol = (logo: string, symbol: string, index: number) => (
  <LogoSymbol logo={logo} symbol={symbol} key={index} />
);

const renderEmasAligned = (value: boolean, index: number) => (
  <EmasAlignedCell
    value={value}
    conditionFn={areEmasAligned}
    key={index}
  />
);

interface Ema8RelationPopUpProps {
  item: any;
}

const Ema8RelationPopUp = ({ item }: Ema8RelationPopUpProps) => {
  const ema8Render = () => {
    // const color = item.ema8_greater_open && item.ema8_less_close ? '#29D30D' : (item.ema8_less_close || item.ema8_greater_open) ? '#ccd30d' : 'red';
    const color = 'black'
    return <span style={{ color }}>U${item.ema8}</span>
  }

  const openPriceRender = () => {
    const color = item.ema8_greater_open ? '#29D30D' : 'red';
    return <span style={{ color }}>U${item.open_price}</span>
  }

  const closingPriceRender = () => {
    const color = item.ema8_less_close ? '#29D30D' : 'red';
    return <span style={{ color }}>U${item.closing_price}</span>
  }

  return (
    <div className={tableStyles.ema8Relations}>
      <div className={tableStyles.ema8RelationsHeader}>
        {renderLogoSymbol(item.currency.logo, item.currency.symbol, item.currency.symbol)}
      </div>
      <p className={tableStyles.emaRelLine}><span className={tableStyles.emaRelLineTitle}>Preço de abertura: </span>{openPriceRender()}</p>
      <p className={tableStyles.emaRelLine}><span className={tableStyles.emaRelLineTitle}>EMA8: </span>{ema8Render()}</p>
      <p className={tableStyles.emaRelLine}><span className={tableStyles.emaRelLineTitle}>Preço de fechamento: </span>{closingPriceRender()}</p>
    </div>
  );
};

const renderEma8Validation = (item: any, index: number) => {
  const [anchor, setAnchor] = useState<null | HTMLElement>(null);

  const validator: 'good' | 'bad' | 'normal' = (item.ema8_greater_open) && (item.ema8_less_close) ? 'good' : 'normal';
  const open = Boolean(anchor);
  const id = open ? 'simple-popper' : undefined;

  const handleHover = (event: React.MouseEvent<HTMLElement>) => {
    if (event.type === 'mouseleave') {
      setAnchor(null);
      return;
    }
    setAnchor(anchor ? null : event.currentTarget);
  }

  return (
    <div>
      <BasePopup id={id} open={open} anchor={anchor}>
        <Ema8RelationPopUp item={item} />
      </BasePopup>
      <div style={{
        cursor: 'help'
      }}>
        <TextColoredCondition value={item.ema8 ? item.ema8.toFixed(2) : 'N/A'} condition={validator} key={index} openMoreInfo={handleHover} />
      </div>
    </div>
  )
}

const renderValorizationPercentage = (value: any, index: number, symbol: string) => {
  const validator: 'good' | 'bad' | 'normal' = symbol === 'BTC' ? (value >= 10.0 ? 'good' : (value < 0) ? 'bad' : 'normal') : (value >= 10.0 ? 'good' : (value < 0) ? 'bad' : 'normal');

  return <TextColoredCondition value={value !== null && value !== undefined ? value : 'N/A'} condition={validator} key={index} />;
}

const dataRowsMapper = (data: any) => {
  const newData = data.map((item: any, index: number) => ({
    id: index + 1,
    setor: item.currency.main_sector.title,
    cripto: renderLogoSymbol(item.currency.logo, item.currency.symbol, index),
    ranking: item.ranking, 
    valorizacao: renderValorizationPercentage(item.week_increase_percentage ? item.week_increase_percentage.toFixed(2) : null, index, item.currency.symbol),
    emas: renderEmasAligned(item.ema_aligned, index),
    ema8: item.ema8 ? renderEma8Validation(item, index) : "N/A",
    currency: item.currency,
    ema_aligned: item.ema_aligned,
  }));

  return newData;
};

export default function CustomPaginationActionsTable(
  {
    rowsRaw,
    page,
    setPage,
    rowsPerPage,
    setRowsPerPage,
    count,
    tableLoading,
  }: {
    rowsRaw: any[];
    page: number;
    setPage: React.Dispatch<React.SetStateAction<number>>;
    rowsPerPage: number;
    setRowsPerPage: React.Dispatch<React.SetStateAction<number>>;
    count: number;
    tableLoading: boolean;
  }
) {
  const rows = dataRowsMapper(rowsRaw);

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <TableContainer component={Paper} style={{
      padding: '0 1.2rem'
    }}>
      <Table aria-label="custom pagination table">
        <TableHead>
          <TableRow>
            {columns.map((column) => (
              <TableCell
                key={column.id}
                align={column.align}
                style={{ minWidth: column.minWidth }}
              >
                {column.label}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {tableLoading ? (
            <TableRow style={{ height: 40 }}>
              <TableCell colSpan={10}>
                <LinearProgress color="warning" />
              </TableCell>
            </TableRow>
          ) : (rows.map((row: any) => (
            <TableRow key={row.id} style={{ height: 40 }} className={tableStyles.oddRowStyle}>
              <TableCell component="th" scope="row">
                {row.setor}
              </TableCell>
              <TableCell style={{ width: 160 }} align="left">
                {row.cripto}
              </TableCell>
              <TableCell align="left">{row.ranking}</TableCell>
              <TableCell align="left">{row.valorizacao}</TableCell>
              <TableCell align="left">{row.emas}</TableCell>
              <TableCell align="left">{row.ema8}</TableCell>
            </TableRow>
          )))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TablePagination
              rowsPerPageOptions={[10, 20, 50, 100]}
              colSpan={columns.length}
              count={count}
              rowsPerPage={rowsPerPage}
              page={page}
              slotProps={{
                select: {
                  inputProps: {
                    "aria-label": "rows per page",
                  },
                  native: true,
                },
              }}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
              ActionsComponent={TablePaginationActions}
            />
          </TableRow>
        </TableFooter>
      </Table>
    </TableContainer>
  );
}
