import styles from './EditarCarteira.module.css'

import FormBuilder from '../../../components/FormBuilder';
import NewTransactionForm from '../../../components/Forms/NewTransactionForm';

const EditarCarteira: React.FC = () => {
    return (
        <div>
            <h1 className={styles.mainPageTitle}>Editar dados da carteira</h1>
            <div className={styles.contentWrapper}>
                <FormBuilder title="Adicionar Nova Compra">
                    <NewTransactionForm />
                </FormBuilder>
                {/* Other forms here */}
            </div>
        </div>
    );
}

export default EditarCarteira;
