import styles from './NewTransactionForm.module.css'

import { Autocomplete, Box, Button, FormLabel, TextField, Tooltip, Select, MenuItem } from '@mui/material'
import { RefreshOutlined, CheckOutlined } from '@mui/icons-material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import InputAdornment from '@mui/material/InputAdornment';
import dayjs, { Dayjs } from 'dayjs';
import { useEffect, useState } from 'react';
import api from '../../../service/api';
import { Endpoints } from "../../../constants/apiConfig.json";
import LogoSymbol from '../../Tabela/Logo/LogoSymbol';

interface SymbolInfo {
    label: string
    uuid: string
    name: string
    logo: string
}

const NewTransactionForm: React.FC = () => {
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

    const isValidForm = !cryptoSelected || !priceAtTimestamp || !userInputPrice || isNaN(parseFloat(userInputPrice)) || !buyedValue || isNaN(parseFloat(buyedValue)) || parseFloat(buyedValue) < 0 || parseFloat(userInputPrice) < 0

    const handleBuyDateUpdate = (date: Dayjs | null) => {
        if (!cryptoSelected) return
        setLoadingPriceAtTimestamp(true)
        setBuyDate(date)
        api.get(`${Endpoints.PriceAtTimestamp}/${cryptoSelected}/${date?.format('DD-MM-YYYY HH:MM')}`)
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

    const handleSearchCrypto = (reason: any, value: any) => {
        if (reason === 'clear') {
            setCryptoSelected(null)
            setCryptoSearch(null)
            setPriceAtTimestamp(null)
            setBuyedSelectorType('quantity')
            setBuyedValue(null)
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
                date: buyDate?.format('DD-MM-YYYY HH:MM'),
                quantity: buyedSelectorType === 'quantity' && buyedValue ? parseFloat(buyedValue) : null,
                amount: buyedSelectorType === 'price' && buyedValue ? parseFloat(buyedValue) : null,
                price_on_purchase: userInputPrice ? parseFloat(userInputPrice) : null
            })
            .catch(error => {
                alert('Erro ao criar transação')
                setCreating(false)
            })
            .then(response => {
                setCreating(false)
            })
    }

    const handleChangeBuyedValue = (e: any) => {
        setBuyedValue(e.target.value.replace(',', '.').replace(/[^0-9.]/g, ''))
    }

    const handleChangeUserInputPrice = (e: any) => {
        setUserInputPrice(e.target.value.replace(',', '.').replace(/[^0-9.]/g, ''))
    }


    return (
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
                            <Box {...props} component="li" className={styles.choiceItemContainer} key={option.label} onClick={(e) => {
                                setCryptoSelected(option.label)
                                // @ts-ignore
                                props.onClick(e)
                            }}>
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
                        <DateTimePicker
                            loading={loadingPriceAtTimestamp}
                            disabled={!cryptoSelected}
                            disableFuture
                            format='DD/MM/YYYY HH:MM'
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
    )
}

export default NewTransactionForm
