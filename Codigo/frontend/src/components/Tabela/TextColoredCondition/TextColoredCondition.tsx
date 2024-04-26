const TextColoredCondition: React.FC<{ value: any, condition: 'bad' | 'good' | 'normal' }> = ({ value, condition }) => {
    const style = {
      color: condition === 'good' ? '#29D30D' : (condition === 'bad' ? 'red' : 'black'),
      fontWeight: condition == 'good' ? 'bold' : 'normal',
    }

    return (
      <span style={style}>{value}</span>
    );
}

export default TextColoredCondition;
