import { useState } from "react";
import WalletHistory from "../WalletHistory"

const WalletHistoryContainer: React.FC = () => {
    const mockData = [
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
        {
            date: "2024-06-04", quantity: 10, amount: 100, price_on_purchase: 10, currency: {
                logo: 'https://cryptologos.cc/logos/bitcoin-btc-logo.png',
                symbol: 'BTC'
            }
        },
    ];

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [sortConfig, setSortConfig] = useState<any>([]);

    const sort = (column: string) => {
        setIsLoading(true);
        setTimeout(() => {
            setIsLoading(false);
            setSortConfig([{ column, direction: 'asc' }]);
        }, 1000);
    };

    return (
        <div style={{
            width: '100%',
            marginTop: '2rem',
        }}>
            <WalletHistory
                rows={mockData}
                setSortConfig={sort}
                sortConfig={sortConfig}
                tableLoading={isLoading}
                count={mockData.length}
                page={0}
                setPage={() => { }}
                rowsPerPage={5}
                setRowsPerPage={() => { }}
            />
        </div>
    );
}

export default WalletHistoryContainer;
