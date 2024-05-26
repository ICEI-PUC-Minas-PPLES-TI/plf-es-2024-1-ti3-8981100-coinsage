import styles from './AnaliseDownloadContainer.module.css'
import DownloadButton from './DownloadButton/DownloadButton';

const AnaliseDownloadContainer: React.FC = () => {
    return (
        <div className={styles.buttonsContainer}>
            <DownloadButton title='Planilha excel' />
        </div>
    );
}

export default AnaliseDownloadContainer;
