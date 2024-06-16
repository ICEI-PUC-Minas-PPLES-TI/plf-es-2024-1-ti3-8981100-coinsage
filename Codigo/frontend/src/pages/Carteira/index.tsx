import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import styles from './Carteira.module.css'
import analysisStyles from '../Analise/Analise.module.css';

import Title from "../../components/Title/Title";
import DownloadContainer from '../../components/AnaliseHeader/AnaliseDownloadContainer';
import DownloadButton from '../../components/AnaliseHeader/DownloadButton/DownloadButton';
import WalletHistoryContainer from '../../components/WalletHistoryContainer';
import { useSessionExpired } from '../../hooks/useAuth';
import { useEffect } from 'react';

const Carteira: React.FC = () => {
    const navigate = useNavigate();
    const isSessionExpired = useSessionExpired()

    useEffect(() => {
        if (isSessionExpired) {
            navigate('/login');
        }
    }, [isSessionExpired]);

    return (
        <div>
            <div className={`${analysisStyles.analyseHeader} ${analysisStyles.completeLogContainer}`}>
                <Title title="Carteira" lastUpdateTitle={false} /> {/* TODO: remove mock */}
                <DownloadContainer buttonComponent={<DownloadButton title='Acompanhamento da Carteira' />} />
            </div>

            <div className={`${analysisStyles.analyseHeader} ${analysisStyles.completeLogContainer}`}>
                <Title title="Histórico" />
                <WalletHistoryContainer />
            </div>
            <div className={`${analysisStyles.analyseHeader} ${analysisStyles.completeLogContainer}`}
                style={{
                    display: 'flex',
                    justifyContent: 'start',
                    alignItems: 'start',
                    marginTop: '20px',
                }}>
                <Button
                    className={styles.editLinkButton}
                    variant="contained"
                    color="warning"
                    onClick={() => navigate('/carteira/editar')}
                >
                    Editar dados
                </Button>
            </div>
        </div>
    );
}

export default Carteira;
