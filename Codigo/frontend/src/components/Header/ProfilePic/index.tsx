import styles from './ProfilePic.module.css'
import DefaultProfilePic from '/profile.svg'
import { useState } from 'react';
import { Snackbar, Alert, Slide, SlideProps, SnackbarOrigin } from '@mui/material';

interface State extends SnackbarOrigin {
    open: boolean;
}

function SlideTransition(props: SlideProps) {
    return <Slide {...props} direction="down" />;
}

const ProfilePic: React.FC = () => {
    const [alert, setAlert] = useState<State>({
        open: false,
        vertical: 'top',
        horizontal: 'center',
    })

    const notImplemented = () => {
        setAlert({
            ...alert,
            open: true,
        });
    }

    // const { user } = useAuth(); // TODO: Get user from context
    // const { profilePic } = user;

    return (
        <>
            <Snackbar
                className={styles.snackbar}
                open={alert.open}
                onClose={() => setAlert({ ...alert, open: false })}
                autoHideDuration={2000}
                anchorOrigin={{ vertical: alert.vertical, horizontal: alert.horizontal }}
                key={alert.vertical + alert.horizontal}
                TransitionComponent={SlideTransition}
            >
                <Alert severity="warning">Funcionalidade ainda não implementada</Alert>
            </Snackbar>
            <img className={styles.profilePicContainer} src={DefaultProfilePic} alt="Profile" onClick={notImplemented} />
            {/* <img className={styles.profilePicContainer} src={profilePic ?? DefaultProfilePic} alt="Profile" /> // TODO: Use user profile pic */}
        </>
    );
}

export default ProfilePic;
