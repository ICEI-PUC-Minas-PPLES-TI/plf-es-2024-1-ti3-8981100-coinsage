import React from "react";

const TextColoredCondition: React.FC<{ value: any, condition: 'bad' | 'good' | 'normal', openMoreInfo?: (event: React.MouseEvent<HTMLElement>) => void }> = ({ value, condition, openMoreInfo }) => {
  const style = {
    color: condition === 'good' ? '#29D30D' : (condition === 'bad' ? 'red' : 'black'),
    fontWeight: condition == 'good' ? 'bold' : 'normal',
  }

  return (
    openMoreInfo === undefined ? <span style={style}>{value}</span> : <span onMouseEnter={openMoreInfo} onMouseLeave={openMoreInfo} style={style}>{value}</span>
  );
}

export default TextColoredCondition;
