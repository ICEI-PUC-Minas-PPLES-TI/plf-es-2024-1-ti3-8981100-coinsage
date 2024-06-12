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
    TableSortLabel
} from "@mui/material";
import { Unstable_Popup as BasePopup } from '@mui/base/Unstable_Popup';
import tableStyles from "../Tabela/Tabela.module.css";
import EmasAlignedCell from "../Tabela/EmasAlignedCell/EmasAlignedCell";
import LogoSymbol from "../Tabela/Logo/LogoSymbol";
import React from "react";
import TablePaginationActions from "../Tabela/TablePaginationActions/TablePaginationActions";
import { renderValorizationPercentage } from "../Tabela/Tabela";

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
];

// remove righ zeros
const removeRightZeros = (value: string) => {
    return value.replace(/0+$/, '');
}

// Function to render logo symbol
const renderLogoSymbol = (logo: string, symbol: string, index: number) => (
    <LogoSymbol logo={logo} symbol={symbol} key={index} />
);

// Function to render each row of data
const renderRow = (row: any, index: number) => (
    <TableRow key={index} style={{ height: 40 }} className={tableStyles.oddRowStyle}>
        <TableCell>{row.date}</TableCell>
        <TableCell>{row.crypto}</TableCell>
        <TableCell>{removeRightZeros(row.quantity)}</TableCell>
        <TableCell>{removeRightZeros(row.price_on_purchase)}</TableCell>
        <TableCell>{removeRightZeros(row.price_now)}</TableCell>
        {/* <TableCell>{row.current_profit}</TableCell> */}
        <TableCell>{renderValorizationPercentage(row.current_profit, index, 'symbol', 0)}</TableCell>
    </TableRow>
);

const rowsDataMapper = (rows: any) => {
    return rows.map((row: any, index: number) => ({
        ...row,
        crypto: renderLogoSymbol(row.currency.logo, row.currency.symbol, index),
    }))
}

const WalletHistory: React.FC<WalletHistoryProps> = ({ rows, tableLoading, sortConfig, setSortConfig, page, setPage, rowsPerPage, setRowsPerPage, count }) => {

    const mappedRows = rowsDataMapper(rows)

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
    );
};

export default WalletHistory;
