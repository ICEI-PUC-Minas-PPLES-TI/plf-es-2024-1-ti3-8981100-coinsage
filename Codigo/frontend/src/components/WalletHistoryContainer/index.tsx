import { useEffect, useState } from "react";

import WalletHistory from "../WalletHistory"
import { SortConfig } from "../Tabela/Tabela";
import { Endpoints } from "../../constants/apiConfig.json";
import api from "../../service/api";

const WalletHistoryContainer: React.FC = () => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [rows, setRows] = useState<any[]>([]);
    const [backupRows, setBackupRows] = useState<any[]>([]);
    const [initialLoading, setInitialLoading] = useState<boolean>(true);
    const [tableLoading, setTableLoading] = useState<boolean>(true);
    const [count, setCount] = useState<number>(0);
    const [sortConfig, setSortConfig] = useState<SortConfig[]>([]);

    useEffect(() => {
        // retryRequest();
        setTableLoading(true);
        setRows([]);
        const sortParams = sortConfig.map((sort) => `&sort=${sort.column},${sort.direction}`).join('');
        api
            .get(
                `${Endpoints.ListWallet}?limit=${rowsPerPage}&offset=${page * rowsPerPage ?? 0}${sortParams}`,
                {
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('token') || ''
                    }
                }
            )
            .then((response: any) => {
                if (response.status >= 200 && response.status < 300) {
                    const data = response.data;
                    if (data) {
                        const read = data.data
                        setRows(read.map((row: any) => {
                            // date in format dd/mm/yy/ hh:mm
                            const formatedBuyTime = row.profit.buy_date ?
                                new Intl.DateTimeFormat('en-GB', {
                                    year: "numeric",
                                    month: "numeric",
                                    day: "numeric",
                                    hour: "numeric",
                                    minute: "numeric",
                                    second: "numeric",
                                    timeZone: "America/Sao_Paulo"
                                }).format(new Date(row.profit.buy_date)) : '-';
                            return {
                                date: formatedBuyTime,
                                quantity: row.profit.buy_value,
                                price_on_purchase: row.profit.buy_price,
                                price_now: row.profit.current_price < 0 ? 'N/A' : row.profit.current_price,
                                current_profit: row.profit.current_price ? row.profit.profit : 'N/A',
                                currency: {
                                    logo: row.crypto.logo,
                                    symbol: row.crypto.symbol
                                },
                                uuid: row.transaction_uuid,
                            }
                        }));
                        setCount(data.total);
                    } else {
                    }
                }
            })
            .catch(() => {
            })
            .finally(() => {
                setInitialLoading(false);
                setTableLoading(false);
            });
    }, [page, rowsPerPage, sortConfig]);

    const sort = (column: string) => {
        setTableLoading(true);
        setTimeout(() => {
            setTableLoading(false);
            setSortConfig([{ column, direction: 'asc' }]);
        }, 1000);
    };

    return (
        <div style={{
            width: '100%',
            marginTop: '2rem',
        }}>
            <WalletHistory
                rows={rows}
                setSortConfig={sort}
                sortConfig={sortConfig}
                tableLoading={tableLoading}
                count={count}
                page={page}
                setPage={setPage}
                rowsPerPage={rowsPerPage}
                setRowsPerPage={setRowsPerPage}
                refresh={() => setPage(0)}
            />
        </div>
    );
}

export default WalletHistoryContainer;
