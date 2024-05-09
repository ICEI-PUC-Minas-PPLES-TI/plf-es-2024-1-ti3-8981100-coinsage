import { Box, Button, Container, Grid, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const NotFoundPage: React.FC = () => {
    const navigate = useNavigate();

    return (
        <Box
            sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '50vh'
            }}
        >
            <Container maxWidth="sm">
                <Grid container spacing={1}>
                    <Grid xs={6}>
                        <Typography variant="h1">
                            404
                        </Typography>
                        <Typography variant="h6">
                            A página que você está procurando não foi encontrada.
                        </Typography>
                        <Button style={{
                            marginTop: '1rem',
                        }}
                        variant="contained"
                        color="warning"
                        onClick={() => navigate('/')}
                        >
                            Voltar para a página inicial
                        </Button>
                    </Grid>
                    <Grid xs={6}>
                        <img
                            src="https://cdn-icons-png.flaticon.com/512/284/284270.png"
                            alt=""
                            height={250}
                        />
                    </Grid>
                </Grid>
            </Container>
        </Box>
    );
}

export default NotFoundPage;
