import { Button } from '@mui/material';
import styles from './Carteira.module.css'
import { useNavigate } from 'react-router-dom';

const Carteira: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div>
            <h1>Carteira</h1>
            <Button
                className={styles.editLinkButton}
                variant="contained"
                color="warning"
                onClick={() => navigate('/carteira/editar')}
            >
                Editar dados
            </Button>
        </div>
    );
}

export default Carteira;
