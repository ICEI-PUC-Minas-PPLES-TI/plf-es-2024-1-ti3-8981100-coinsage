import { Button } from '@mui/material';
import DownloadForOfflineRoundedIcon from '@mui/icons-material/DownloadForOfflineRounded';
import { Endpoints } from "../../../constants/apiConfig.json";
import axios from 'axios'; 

import styles from './DownloadButton.module.css'

interface DownloadPartProps {
    title: string;
    loading?: boolean;
}

const DownloadButton: React.FC<DownloadPartProps> = ({ title, loading }) => {
    const handleDownload = async () => {
        try {
            const response = await axios.get(Endpoints.Workbook, {
                responseType: 'blob',
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            
            const date = new Date();
            const formattedDate = `${date.getDate().toString().padStart(2, '0')}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getFullYear().toString().slice(-2)}`;
            const filename = `análise ${formattedDate}.xlsx`;
    
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error('Erro ao baixar o arquivo:', error);
        }
    };

    return (
        <div className={styles.button}>
            <h2>{title}</h2>
            <Button
                className={styles.downloadButton}
                disabled={loading}
                onClick={handleDownload}
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
