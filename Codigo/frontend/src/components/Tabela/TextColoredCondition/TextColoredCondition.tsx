const TextColoredCondition: React.FC<{ value: boolean, conditionFn: (value: boolean) => string }> = ({ value, conditionFn }) => {
    const text = conditionFn(value);

    const style = {
      color: text === 'SIM' ? '#29D30D' : (text === 'NÃO' ? 'red' : 'black'),
      fontWeight: text === 'SIM' ? 'bold' : 'normal',
    }

    return (
      <span style={style}>{text}</span>
    );
}

export default TextColoredCondition;
