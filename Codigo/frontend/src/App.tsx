import { Header } from "./components/Header/Header";
import { Title } from "./components/Title/Title";
import { DownloadButton } from './components/DownloadButton/DownloadButton';
import { Table } from './components/Table/Table';

import { DataGrid, GridColDef } from '@mui/x-data-grid';

import "./styles/global.css";
import styles from "./App.module.css";
import React, { useState } from 'react';


export function App() {

  return (
    <div>
      <Header />
      <Title/>
      <DownloadButton/>
      <Table/>
    </div>
  );
}