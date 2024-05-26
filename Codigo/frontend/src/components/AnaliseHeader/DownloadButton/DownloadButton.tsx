import LoadingButton from '@mui/lab/LoadingButton';
import DownloadForOfflineRoundedIcon from '@mui/icons-material/DownloadForOfflineRounded';
import { Endpoints } from "../../../constants/apiConfig.json";
import api from "../../../service/api";

import styles from './DownloadButton.module.css'
import { useState } from 'react';

interface DownloadPartProps {
    title: string;
}

const DownloadButton: React.FC<DownloadPartProps> = ({ title }) => {
    const [loading, setLoading] = useState<boolean>(false)

    const handleDownload = async () => {
        setLoading(true)
        try {
            const response = await api.get(Endpoints.Workbook, {
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
            if (link.parentNode) {
                link.parentNode.removeChild(link);
            }
        } catch (error) {
            console.error('Erro ao baixar o arquivo:', error);
        }
        setLoading(false)
    };

    return (
        <div className={styles.button}>
            <h2>{title}</h2>
            <LoadingButton
                className={styles.downloadButton}
                loading={loading}
                onClick={handleDownload}
                size='small'
                variant='outlined'
                startIcon={<DownloadForOfflineRoundedIcon />}
            >
                Baixar
            </LoadingButton>
        </div>
    );
}

export default DownloadButton;
