import { Button } from '@mui/material';
import DownloadForOfflineRoundedIcon from '@mui/icons-material/DownloadForOfflineRounded';

import styles from './DownloadButton.module.css'

interface DownloadPartProps {
    title: string;
    handler: () => void;
    loading?: boolean;
}

const DownloadButton: React.FC<DownloadPartProps> = ({ title, handler, loading }) => {
    return (
        <div className={styles.button}>
            <h2>{title}</h2>
            <Button
                className={styles.downloadButton}
                disabled={loading}
                onClick={handler}
                size='small'
                variant='outlined'
                startIcon={<DownloadForOfflineRoundedIcon />}
            >
                Baixar
            </Button>
        </div>
    );
}

export default DownloadButton;
