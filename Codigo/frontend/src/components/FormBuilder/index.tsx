import styles from './FormBuilder.module.css'

interface FormBuilderProps {
    title: string
    children: React.ReactNode
}

const FormBuilder: React.FC<FormBuilderProps> = ({ children, title }) => {
    return (
        <section className={styles.formSection}>
            <div className={styles.formSectionTitleContainer}>
                <span>{title}</span>
            </div>
            <div className={styles.formContainer}>
                {children}
            </div>
        </section>
    )
}

export default FormBuilder
