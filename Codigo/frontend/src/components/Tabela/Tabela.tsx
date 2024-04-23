import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableFooter from "@mui/material/TableFooter";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { TableHead } from "@mui/material";
import LogoSymbol from "./Logo/LogoSymbol";
import TextColoredCondition from "./TextColoredCondition/TextColoredCondition";
import { LinearProgress } from "@mui/material";
import TablePaginationActions from "./TablePaginationActions/TablePaginationActions";
import tableStyles from "./Tabela.module.css";

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
  { id: "valorizacao", label: "% Valorização" },
  { id: "preco", label: "Preço na Avaliação" },
  { id: "emas", label: "EMAs (d) Alinhados" },
  {
    id: "dataValorizacaoVolume",
    label: "Data Valorização Volume (d)",
  },
  {
    id: "quantidadeVolumeValorizacao",
    label: "Quantidade Volume Valorização",
  },
  {
    id: "quantidadeVolumeDiaAnterior",
    label: "Quantidade Volume Dia Anterior",
  },
  { id: "percentDiaAnterior", label: "% Dia Atual/Dia Anterior" },
  { id: "ema8", label: "EMA8 (s)" },
];

const renderLogoSymbol = (logo: string, symbol: string, index: number) => (
  <LogoSymbol logo={logo} symbol={symbol} key={index} />
);

const renderEmasAligned = (value: boolean, index: number) => (
  <TextColoredCondition
    value={value}
    conditionFn={areEmasAligned}
    key={index}
  />
);

const dataRowsMapper = (data: any) => {
  const newData = data.map((item: any, index: number) => ({
    id: index + 1,
    setor: item.currency.main_sector.title,
    cripto: renderLogoSymbol(item.currency.logo, item.currency.symbol, index),
    valorizacao: `${item.week_increase_percentage.toFixed(2)}%`,
    preco: `${item.closing_price.toFixed(2)}`,
    emas: renderEmasAligned(item.ema_aligned, index),
    dataValorizacaoVolume: item.valorization_date,
    quantidadeVolumeValorizacao: `${item.open_price.toFixed(2)}`,
    quantidadeVolumeDiaAnterior: `${item.last_week_closing_price.toFixed(2)}`,
    percentDiaAnterior: `${(
      ((item.open_price - item.last_week_closing_price) /
        item.last_week_closing_price) *
      100
    ).toFixed(2)}%`,
    ema8: item.ema8 ? item.ema8.toFixed(2).toString() : "N/A",
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
  const emptyRows = rowsPerPage - Math.min(rowsPerPage, rows.length);

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
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 500 }} aria-label="custom pagination table">
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
          {rows.map((row: any) => (
            <TableRow key={row.id} style={{ height: 40}} className={tableStyles.oddRowStyle}>
              <TableCell component="th" scope="row">
                {row.setor}
              </TableCell>
              <TableCell style={{ width: 160 }} align="left">
                {row.cripto}
              </TableCell>
              <TableCell align="left">{row.valorizacao}</TableCell>
              <TableCell align="left">{row.preco}</TableCell>
              <TableCell align="left">{row.emas}</TableCell>
              <TableCell align="left">{row.dataValorizacaoVolume}</TableCell>
              <TableCell align="left">
                {row.quantidadeVolumeValorizacao}
              </TableCell>
              <TableCell align="left">
                {row.quantidadeVolumeDiaAnterior}
              </TableCell>
              <TableCell align="left">{row.percentDiaAnterior}</TableCell>
              <TableCell align="left">{row.ema8}</TableCell>
            </TableRow>
          ))}
          {tableLoading && (
            <TableRow style={{ height: 40}}>
            <TableCell colSpan={10}>
              <LinearProgress />
            </TableCell>
          </TableRow>
          )}
          {emptyRows > 0 && (
            <TableRow style={{ height: 40 * emptyRows }}>
              <TableCell colSpan={6} />
            </TableRow>
          )}
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
