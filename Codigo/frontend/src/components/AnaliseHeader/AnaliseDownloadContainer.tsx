import { useState } from 'react';
import styles from './AnaliseDownloadContainer.module.css'
import DownloadButton from './DownloadButton/DownloadButton';
import { Alert, Slide, SlideProps, Snackbar, SnackbarOrigin } from '@mui/material';

interface State extends SnackbarOrigin {
    open: boolean;
}

function SlideTransition(props: SlideProps) {
    return <Slide {...props} direction="down" />;
}

const AnaliseDownloadContainer: React.FC = () => {
    const [downloadAlert, setDownloadAlert] = useState<State>({
        open: false,
        vertical: 'top',
        horizontal: 'center',
    })

    const notImplemented = () => {
        setDownloadAlert({
            ...downloadAlert,
            open: true,
        });
    }

    return (
        <div className={styles.buttonsContainer}>
            <DownloadButton title='Planilha excel' handler={notImplemented} />
            <Snackbar
                className={styles.snackbar}
                open={downloadAlert.open}
                onClose={() => setDownloadAlert({ ...downloadAlert, open: false })}
                autoHideDuration={2000}
                anchorOrigin={{ vertical: downloadAlert.vertical, horizontal: downloadAlert.horizontal }}
                key={downloadAlert.vertical + downloadAlert.horizontal}
                TransitionComponent={SlideTransition}
            >
                <Alert severity="warning">Funcionalidade ainda não implementada</Alert>
            </Snackbar>
        </div>
    );
}

export default AnaliseDownloadContainer;
