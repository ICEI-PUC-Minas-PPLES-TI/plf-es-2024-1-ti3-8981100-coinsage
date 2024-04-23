import styles from './LogoSymbol.module.css';

interface LogoSymbolProps {
    logo: string;
    symbol: string;
}

const LogoSymbol: React.FC<LogoSymbolProps> = ({ logo, symbol }) => {
    return (
        <div style={{ display: 'flex', alignItems: 'center' }}>
            <div className={styles.logoSymbol}>
                <img src={logo} alt={symbol} style={{ width: '30px', height: '30px' }} />
                <span>{symbol}</span>
            </div>
        </div>
    );
};

export default LogoSymbol;
