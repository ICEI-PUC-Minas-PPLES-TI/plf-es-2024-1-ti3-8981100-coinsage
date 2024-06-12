import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableFooter,
    TableHead,
    TablePagination,
    TableRow,
    Paper,
    LinearProgress,
    TableSortLabel,
    IconButton,
    Snackbar,
    Alert,
    Tooltip
} from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import { Unstable_Popup as BasePopup } from '@mui/base/Unstable_Popup';
import tableStyles from "../Tabela/Tabela.module.css";
import EmasAlignedCell from "../Tabela/EmasAlignedCell/EmasAlignedCell";
import LogoSymbol from "../Tabela/Logo/LogoSymbol";
import React, { useState } from "react";
import TablePaginationActions from "../Tabela/TablePaginationActions/TablePaginationActions";
import { renderValorizationPercentage } from "../Tabela/Tabela";
import { Endpoints } from "../../constants/apiConfig.json";
import api from "../../service/api";

interface WalletHistoryProps {
    rows: any;
    tableLoading: boolean;
    sortConfig: any;
    setSortConfig: any;
    page: number;
    setPage: React.Dispatch<React.SetStateAction<number>>;
    rowsPerPage: number;
    setRowsPerPage: React.Dispatch<React.SetStateAction<number>>;
    count: number;
    refresh: () => void;
}

// Define columns
const columns = [
    { id: "date", label: "Data da Compra", minWidth: 100 },
    { id: "crypto", label: "Moeda", minWidth: 100 },
    { id: "quantity", label: "Valor comprado (USD)", minWidth: 100 },
    // { id: "amount", label: "Amount", minWidth: 100 },
    { id: "price_on_purchase", label: "Preço na Compra (USD)", minWidth: 100 },
    { id: "current_price", label: "Preço Atual (USD)", minWidth: 100 },
    { id: "current_profit", label: "Lucro Atual (%)", minWidth: 100 },
    { id: "actions", label: "Ações", minWidth: 50 },
];

// remove righ zeros
const removeRightZeros = (value: string) => {
    return value.replace(/0+$/, '');
}

// Function to render logo symbol
const renderLogoSymbol = (logo: string, symbol: string, index: number) => (
    <LogoSymbol logo={logo} symbol={symbol} key={index} />
);

const rowsDataMapper = (rows: any) => {
    return rows.map((row: any, index: number) => ({
        ...row,
        crypto: renderLogoSymbol(row.currency.logo, row.currency.symbol, index),
    }))
}

const WalletHistory: React.FC<WalletHistoryProps> = ({ rows, tableLoading, sortConfig, setSortConfig, page, setPage, rowsPerPage, setRowsPerPage, count, refresh }) => {
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [alertDetail, setAlertDetail] = useState<{
        msg: string,
        type: string
    } | null>(null);

    const handleDeleteTransaction = (uuid: string) => {
        api.delete(`${Endpoints.DeleteTransaction}/${uuid}`, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token') || ''
            }
        })
            .then(() => {
                setAlertDetail({
                    msg: 'Transação deletada com sucesso',
                    type: 'success'
                });
                setOpenSnackbar(true);
                refresh()
            })
            .catch((error) => {
                setAlertDetail({
                    msg: 'Falha ao deletar transação, por favor tente novamente',
                    type: 'error'
                });
                setOpenSnackbar(true);
            });
    };

    const mappedRows = rowsDataMapper(rows)

    const renderRow = (row: any, index: number) => (
        <TableRow key={index} style={{ height: 40 }} className={tableStyles.oddRowStyle}>
            <TableCell>{row.date}</TableCell>
            <TableCell>{row.crypto}</TableCell>
            <TableCell>{removeRightZeros(row.quantity)}</TableCell>
            <TableCell>{removeRightZeros(row.price_on_purchase)}</TableCell>
            <TableCell>{removeRightZeros(row.price_now)}</TableCell>
            {/* <TableCell>{row.current_profit}</TableCell> */}
            <TableCell>{renderValorizationPercentage(row.current_profit, index, 'symbol', 0)}</TableCell>
            <TableCell>
                <Tooltip title="Deletar transação" arrow>
                    <IconButton onClick={() => handleDeleteTransaction(row.uuid)} aria-label="delete">
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>
            </TableCell>
        </TableRow>
    );

    const handleSortRequest = (column: string) => {
        // Handle sort request logic here
    };

    const handleChangePage = (
        event: React.MouseEvent<HTMLButtonElement> | null,
        newPage: number
    ) => {
        setSortConfig([]);
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
    ) => {
        setSortConfig([]);
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    return (
        <>
            <TableContainer component={Paper} style={{ padding: '0 1.2rem' }}>
                <Table aria-label="custom pagination table">
                    <TableHead>
                        <TableRow>
                            {columns.map((column) => (
                                <TableCell
                                    key={column.id}
                                    align="left"
                                    style={{ minWidth: column.minWidth }}
                                >
                                    <TableSortLabel
                                        active={sortConfig.some((sort: any) => sort.column === column.id)}
                                        direction={
                                            sortConfig.find((sort: any) => sort.column === column.id)?.direction || 'asc'
                                        }
                                        onClick={() => handleSortRequest(column.id)}
                                    >
                                        {column.label}
                                    </TableSortLabel>
                                </TableCell>
                            ))}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {tableLoading ? (
                            <TableRow style={{ height: 40 }}>
                                <TableCell colSpan={4}>
                                    <LinearProgress color="warning" />
                                </TableCell>
                            </TableRow>
                        ) : (
                            mappedRows.map((row: any, index: number) => renderRow(row, index))
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
            <Snackbar open={openSnackbar} autoHideDuration={2000} onClose={() => setOpenSnackbar(false)}>
                {/* @ts-ignore */}
                <Alert onClose={() => setOpenSnackbar(false)} severity={alertDetail?.type || 'info'} sx={{ width: '100%' }}>
                    {alertDetail?.msg}
                </Alert>
            </Snackbar>
        </>
    );
};

export default WalletHistory;
