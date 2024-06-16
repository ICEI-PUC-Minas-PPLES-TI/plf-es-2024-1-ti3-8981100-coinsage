import { useEffect, useState } from "react";

import WalletHistory from "../WalletHistory"
import { SortConfig } from "../Tabela/Tabela";
import { Endpoints } from "../../constants/apiConfig.json";
import api from "../../service/api";
import { useNavigate } from "react-router-dom";
import { useSessionExpired } from "../../hooks/useAuth";

const WalletHistoryContainer: React.FC = () => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [rows, setRows] = useState<any[]>([]);
    const [backupRows, setBackupRows] = useState<any[]>([]);
    const [initialLoading, setInitialLoading] = useState<boolean>(true);
    const [tableLoading, setTableLoading] = useState<boolean>(true);
    const [count, setCount] = useState<number>(0);
    const [sortConfig, setSortConfig] = useState<SortConfig[]>([]);
    const navigate = useNavigate();
    const isSessionExpired = useSessionExpired()

    useEffect(() => {
        if (isSessionExpired) {
            navigate('/login');
        }
    }, [isSessionExpired]);

    const request = (sortParams: any = '') => {
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
                        console.log(read)
                        const formatedData = read.map((row: any) => {
                            let formatedBuyTime = 'Invalid Date';
                            try {
                                if (row.profit.buy_date) {
                                    let [datePart, timePart] = row.profit.buy_date.split(' ');
                                    let [day, month, year] = datePart.split('-');
                                    let formattedDate = `${year}-${month}-${day}T${timePart}`;
                                    formatedBuyTime = new Intl.DateTimeFormat('en-GB', {
                                        year: "numeric",
                                        month: "numeric",
                                        day: "numeric",
                                        hour: "numeric",
                                        minute: "numeric",
                                        second: "numeric",
                                        timeZone: "America/Sao_Paulo"
                                    }).format(new Date(formattedDate));
                                } else {
                                    formatedBuyTime = '-';
                                }
                            } catch (e) {
                                console.error(e);
                            }

                            return {
                                date: formatedBuyTime,
                                quantity: row.profit.buy_value,
                                price_on_purchase: row.profit.buy_price,
                                price_now: row.profit.current_price < 0 ? 'N/A' : row.profit.current_price,
                                current_profit: row.profit.current_price >= 0 ? row.profit.profit : 'N/A',
                                currency: {
                                    logo: row.crypto.logo,
                                    symbol: row.crypto.symbol
                                },
                                uuid: row.transaction_uuid,
                            }
                        })
                        console.log(`formatedData: ${formatedData}`)
                        setRows(formatedData);
                        setCount(data.total);
                    } else {
                    }
                }
            })
            .catch((error) => {
                if (error.response.status === 401) {
                    localStorage.removeItem('token')
                    navigate('/login')
                }
            })
            .finally(() => {
                setInitialLoading(false);
                setTableLoading(false);
            });
    }

    useEffect(() => {
        // retryRequest();
        setTableLoading(true);
        setRows([]);
        const sortParams = sortConfig.map((sort) => `&sort=${sort.column},${sort.direction}`).join('');
        request(sortParams)

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
                refresh={request}
            />
        </div>
    );
}

export default WalletHistoryContainer;
