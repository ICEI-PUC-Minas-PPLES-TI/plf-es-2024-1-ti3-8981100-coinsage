import { Box, LinearProgress } from "@mui/material";
import { useState, useEffect } from "react";
import titleStyles from "../../../components/Title/Title.module.css";

const LoadingTableComponent: React.FC = () => {
  const [loadingText, setLoadingText] = useState<string>(
    "Carregando dados da última análise..."
  );

  useEffect(() => {
    const interval = setInterval(() => {
      setLoadingText((prev) => {
        if (prev === "Carregando dados da última análise...") {
          return "Por favor, aguarde...";
        } else {
          return "Carregando dados da última análise...";
        }
      });
    }, 1200);

    return () => clearInterval(interval);
  });

  return (
    <>
      <h1 className={titleStyles.title} style={{marginBottom: '1rem'}}>{loadingText}</h1>
      <Box sx={{ width: "100%" }}>
        <LinearProgress color="warning" />
      </Box>
    </>
  );
};

export default LoadingTableComponent;
