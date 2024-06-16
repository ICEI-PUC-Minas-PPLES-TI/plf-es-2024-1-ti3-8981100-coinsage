import styles from './NewTransactionForm.module.css'

import {
    Autocomplete,
    Box,
    Button,
    FormLabel,
    TextField,
    Tooltip,
    Select,
    MenuItem,
    Slide,
    SlideProps,
    Dialog,
    DialogActions,
    DialogContent,
    AlertTitle,
    Alert,
    IconButton,
    Typography,
    Collapse
} from '@mui/material'
import { RefreshOutlined, CheckOutlined, CloseOutlined } from '@mui/icons-material';
import InputAdornment from '@mui/material/InputAdornment';
import { Dayjs } from 'dayjs';
import { forwardRef, Ref, useEffect, useState } from 'react';
import api from '../../../service/api';
import { Endpoints } from "../../../constants/apiConfig.json";
import LogoSymbol from '../../Tabela/Logo/LogoSymbol';
import { JSX } from 'react/jsx-runtime';
import { useNavigate } from 'react-router-dom';
import { StaticDateTimePicker } from '@mui/x-date-pickers';
import Snackbar from '@mui/material/Snackbar';
import React from 'react';

interface SymbolInfo {
    label: string
    uuid: string
    name: string
    logo: string
}

const Transition = forwardRef(function Transition(props: JSX.IntrinsicAttributes & SlideProps, ref: Ref<unknown> | undefined) {
    return <Slide direction="up" ref={ref} {...props} />;
});

const NewTransactionForm: React.FC = () => {
    const navigate = useNavigate()
    const [userInputPrice, setUserInputPrice] = useState<string | null>(null)
    const [loadingCryptoSearch, setLoadingCryptoSearch] = useState<boolean>(false)
    const [loadingPriceAtTimestamp, setLoadingPriceAtTimestamp] = useState<boolean>(false)
    const [priceAtTimestamp, setPriceAtTimestamp] = useState<number | null>(null)
    const [buyDate, setBuyDate] = useState<Dayjs | null>(null)
    const [cryptoSelected, setCryptoSelected] = useState<string | null>(null)
    const [cryptoSearch, setCryptoSearch] = useState<string | null>(null)
    const [buyedSelectorType, setBuyedSelectorType] = useState<string>('quantity')
    const [buyedValue, setBuyedValue] = useState<string | null>(null)
    const [symbolsList, setSymbolsList] = useState<SymbolInfo[] | []>([])
    const [creating, setCreating] = useState<boolean>(false)
    const [openSuccess, setOpenSuccess] = useState<boolean>(false)
    const [openFeedback, setOpenFeedback] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)

    const isValidForm = !cryptoSelected || !priceAtTimestamp || !userInputPrice || isNaN(parseFloat(userInputPrice)) || !buyedValue || isNaN(parseFloat(buyedValue)) || parseFloat(buyedValue) < 0 || parseFloat(userInputPrice) < 0

    const handleBuyDateUpdate = (date: Dayjs | null) => {
        if (!cryptoSelected) return
        setLoadingPriceAtTimestamp(true)
        setBuyDate(date)
        api.get(`${Endpoints.PriceAtTimestamp}/${cryptoSelected}/${date?.format('DD-MM-YYYY H:m')}`)
            .then(response => {
                setPriceAtTimestamp(response.data)
                setUserInputPrice(response.data.toString())
                setLoadingPriceAtTimestamp(false)
            })
    }

    useEffect(() => {
        setLoadingCryptoSearch(true)
        api.get(`${Endpoints.QuerySymbol}/${cryptoSearch ?? ''}`)
            .then(response => {
                setSymbolsList(response.data.map((symbol: any) => ({
                    label: symbol.symbol,
                    uuid: symbol.uuid,
                    name: symbol.name,
                    logo: symbol.logo
                })))
                setLoadingCryptoSearch(false)
            })
    }, [cryptoSearch])

    const clearAll = () => {
        setCryptoSelected(null)
        setCryptoSearch(null)
        setPriceAtTimestamp(null)
        setBuyedSelectorType('quantity')
        setBuyedValue(null)
    }

    const handleSearchCrypto = (reason: any, value: any) => {
        if (reason === 'clear') {
            clearAll()
        }

        if (reason === 'reset') {
            setCryptoSearch(value)
        }
    }

    const buyedInputRender = () => {
        if (buyedSelectorType === 'price') {
            return (
                <InputAdornment position="start">
                    <span>U$</span>
                </InputAdornment>
            )
        }
        return null
    }

    const handleCreation = () => {
        setCreating(true)
        api
            .post(Endpoints.CreateWalletBuy, {
                crypto: cryptoSelected,
                date: buyDate?.format('DD-MM-YYYY H:m'),
                quantity: buyedSelectorType === 'quantity' && buyedValue ? parseFloat(buyedValue) : null,
                amount: buyedSelectorType === 'price' && buyedValue ? parseFloat(buyedValue) : null,
                price_on_purchase: userInputPrice ? parseFloat(userInputPrice) : null
            }, {
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token') || ''
                }
            })
            .then(response => {
                setOpenSuccess(true)
            })
            .catch(error => {
                setOpenFeedback(true)
                setError(error.response.data.detail || error.response.statusText)
                if(error.response.status === 401) {
                    localStorage.removeItem('token')
                    navigate('/login')
                }
            })
            .finally(() => {
                setCreating(false)
            })
    }

    const handleChangeBuyedValue = (e: any) => {
        setBuyedValue(e.target.value.replace(',', '.').replace(/[^0-9.]/g, ''))
    }

    const handleChangeUserInputPrice = (e: any) => {
        setUserInputPrice(e.target.value.replace(',', '.').replace(/[^0-9.]/g, ''))
    }

    const handleClose = () => {
        clearAll()
        setOpenSuccess(false)
    }

    const goToHistory = () => {
        clearAll()
        navigate('/carteira')
    }

    return (
        <>
            <Dialog
                open={openSuccess}
                TransitionComponent={Transition}
                keepMounted
                onClose={handleClose}
                aria-describedby="alert-dialog-slide-description"
            >
                <DialogContent>
                    <Alert severity="success">
                        <AlertTitle>Sucesso!</AlertTitle>
                        A transação foi criada com sucesso...
                    </Alert>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Criar uma nova</Button>
                    <Button onClick={goToHistory}>Visualizar histórico</Button>
                </DialogActions>
            </Dialog>
            <form className={styles.form}>
                <div className={styles.formInputs}>
                    <div className={styles.formItemContainer}>
                        <FormLabel className={styles.inputLabel}>Moeda</FormLabel>
                        <Autocomplete
                            // @ts-ignore
                            onInputChange={(_, value, reason) => handleSearchCrypto(reason, value)}
                            onReset={() => setCryptoSelected(null)}
                            disablePortal
                            options={symbolsList}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label='Moeda' />}
                            renderOption={(props, option) => (
                                // @ts-ignore
                                <Box
                                    {...props}
                                    component="li"
                                    className={styles.choiceItemContainer}
                                    key={option.label}
                                    onClick={(e) => {
                                        setCryptoSelected(option.label)
                                        // @ts-ignore
                                        props.onClick(e)
                                    }}
                                >
                                    <LogoSymbol logo={option.logo} symbol={option.label} />
                                </Box>
                            )}
                            isOptionEqualToValue={(option, value) => option.label === value.label}
                            loading={loadingCryptoSearch}
                            disabled={loadingPriceAtTimestamp}
                            autoSelect={false}
                        />
                    </div>
                    {cryptoSelected &&
                        <div className={styles.formItemContainer}>
                            <FormLabel className={styles.inputLabel}>Momento de compra</FormLabel>
                            <StaticDateTimePicker
                                loading={loadingPriceAtTimestamp}
                                disabled={!cryptoSelected}
                                disableFuture
                                onAccept={handleBuyDateUpdate}
                            />
                        </div>
                    }
                    {priceAtTimestamp &&
                        <>
                            <div className={styles.formItemContainer}>
                                <FormLabel className={styles.inputLabel}>Preço no momento de compra</FormLabel>
                                <TextField
                                    InputProps={{
                                        startAdornment: (
                                            <InputAdornment position="start">
                                                <span>U$</span>
                                            </InputAdornment>
                                        ),
                                        endAdornment: (
                                            <Tooltip title='Retomar preço automático' arrow>
                                                <Button onClick={() => setUserInputPrice(priceAtTimestamp.toString())}>
                                                    <RefreshOutlined />
                                                </Button>
                                            </Tooltip>
                                        )
                                    }}
                                    value={userInputPrice ?? priceAtTimestamp}
                                    onChange={handleChangeUserInputPrice}
                                    placeholder='Ex.: 65.87'
                                    helperText={userInputPrice ? !isNaN(parseFloat(userInputPrice)) ? null : 'Exemplo de formato válido: 65.87' : null}
                                    error={userInputPrice ? isNaN(parseFloat(userInputPrice)) : false}
                                    datatype='number'
                                />
                            </div>

                            {userInputPrice &&
                                <div className={styles.formItemContainer}>
                                    <FormLabel className={styles.inputLabel}>
                                        Quantidade ou valor total comprado
                                    </FormLabel>
                                    <Tooltip
                                        title='Você pode adicionar a quantidade comprada ou o valor total da compra'
                                        arrow
                                        placement='right-end'
                                    >
                                        <Select
                                            defaultValue={buyedSelectorType}
                                            sx={{
                                                width: 300,
                                            }}
                                            onChange={(e) => setBuyedSelectorType(e.target.value)}
                                        >
                                            <MenuItem value="quantity">Quatidade</MenuItem>
                                            <MenuItem value="price">Valor Comprado</MenuItem>
                                        </Select>
                                    </Tooltip>
                                    <TextField
                                        sx={{
                                            width: 300,
                                        }}
                                        InputProps={{
                                            startAdornment: buyedInputRender(),
                                        }}
                                        value={buyedValue ?? 0}
                                        onChange={handleChangeBuyedValue}
                                        placeholder='Ex.: 5.87'
                                        helperText={buyedValue ? !isNaN(parseFloat(buyedValue)) ? null : 'Exemplo de formato válido: 5.87' : null}
                                        error={buyedValue ? isNaN(parseFloat(buyedValue)) || parseFloat(buyedValue) < 0 : false}
                                        datatype='number'
                                    />
                                </div>
                            }
                        </>
                    }
                </div>
                <Button
                    disabled={isValidForm || creating}
                    onClick={handleCreation}
                    variant='contained'
                    color='warning'
                    endIcon={<CheckOutlined />}
                >
                    Submit
                </Button>
            </form>
            <Snackbar
                open={openFeedback}
                autoHideDuration={5000}
                onClose={() => setOpenFeedback(false)}
                message={error}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Collapse in={openFeedback}>
                    <Alert
                        action={
                            <IconButton
                                aria-label="close"
                                color="inherit"
                                size="small"
                                onClick={() => {
                                    setOpenFeedback(false);
                                }}
                            >
                                <CloseOutlined fontSize="inherit" />
                            </IconButton>
                        }
                        sx={{ mb: 2 }}
                        severity="error"
                    >
                        {error}
                    </Alert>
                </Collapse>
            </Snackbar>
        </>
    )
}

export default NewTransactionForm
