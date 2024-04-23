import * as React from "react";
import { useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableFooter from "@mui/material/TableFooter";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import IconButton from "@mui/material/IconButton";
import FirstPageIcon from "@mui/icons-material/FirstPage";
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import LastPageIcon from "@mui/icons-material/LastPage";
import { TableHead } from "@mui/material";
import api from "../../service/api";
import { Endpoints } from "../../constants/apiConfig.json";
import LogoSymbol from "./Logo/LogoSymbol";
import TextColoredCondition from "./TextColoredCondition/TextColoredCondition";
import { LinearProgress } from "@mui/material";
import titleStyles from "../../components/Title/Title.module.css";

const LoadingTableComponent: React.FC = () => {
  const [loadingText, setLoadingText] = React.useState<string>(
    "Carregando dados da última análise..."
  );

  React.useEffect(() => {
    const interval = setInterval(() => {
      setLoadingText((prev) => {
        if (prev === "Carregando dados da última análise...") {
          return "Por favor, aguarde...";
        } else {
          return "Carregando dados da última análise...";
        }
      });
    }, 1200);

    return () => clearInterval(interval);
  });

  return (
    <>
      <h1 className={titleStyles.title}>{loadingText}</h1>
      <Box sx={{ width: "100%" }}>
        <LinearProgress />
      </Box>
    </>
  );
};

interface TablePaginationActionsProps {
  count: number;
  page: number;
  rowsPerPage: number;
  onPageChange: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number
  ) => void;
}

interface Column {
  id: string;
  label: string;
  minWidth?: number;
  align?: "right";
  format?: (value: number) => string;
  renderCell?: (params: any) => JSX.Element;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
  const theme = useTheme();
  const { count, page, rowsPerPage, onPageChange } = props;

  const handleFirstPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, 0);
  };

  const handleBackButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, page - 1);
  };

  const handleNextButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, page + 1);
  };

  const handleLastPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
  };

  return (
    <Box sx={{ flexShrink: 0, ml: 2.5 }}>
      <IconButton
        onClick={handleFirstPageButtonClick}
        disabled={page === 0}
        aria-label="first page"
      >
        {theme.direction === "rtl" ? <LastPageIcon /> : <FirstPageIcon />}
      </IconButton>
      <IconButton
        onClick={handleBackButtonClick}
        disabled={page === 0}
        aria-label="previous page"
      >
        {theme.direction === "rtl" ? (
          <KeyboardArrowRight />
        ) : (
          <KeyboardArrowLeft />
        )}
      </IconButton>
      <IconButton
        onClick={handleNextButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="next page"
      >
        {theme.direction === "rtl" ? (
          <KeyboardArrowLeft />
        ) : (
          <KeyboardArrowRight />
        )}
      </IconButton>
      <IconButton
        onClick={handleLastPageButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="last page"
      >
        {theme.direction === "rtl" ? <FirstPageIcon /> : <LastPageIcon />}
      </IconButton>
    </Box>
  );
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

export default function CustomPaginationActionsTable() {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [rows, setRows] = React.useState<any[]>([]);
  const [initialLoading, setInitialLoading] = React.useState<boolean>(true);
  const [tableLoading, setTableLoading] = React.useState<boolean>(true);
  const [count, setCount] = React.useState<number>(0);

  React.useEffect(() => {
    setTableLoading(true);
    setRows([]);
    api
      .get(
        `${Endpoints.FirstStage}?limit=${rowsPerPage}&offset=${
          page * rowsPerPage ?? 0
        }`
      )
      .then((response: any) => {
        if (response.status >= 200 && response.status < 300) {
          const data = response.data;
          if (data) {
            setRows(dataRowsMapper(data.last_update.data.data));
            setCount(data.last_update.data.total);
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

  if (initialLoading) {
    return (
      <>
        <LoadingTableComponent />
      </>
    );
  }

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
          {rows.map((row) => (
            <TableRow key={row.id} style={{ height: 40}}>
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
              colSpan={10}
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
