import styles from './AnaliseDownloadContainer.module.css'
import DownloadButton from './DownloadButton/DownloadButton';

interface DownloadContainerProps {
    buttonComponent?: React.ReactNode;
}

const DownloadContainer: React.FC<DownloadContainerProps> = ({ buttonComponent =  <DownloadButton title='Planilha excel' />}) => {
    return (
        <div className={styles.buttonsContainer}>
            {buttonComponent}
        </div>
    );
}

export default DownloadContainer;
