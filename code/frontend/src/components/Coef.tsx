import React from 'react'
import { Progress } from './ui/progress';
interface CoefProps {
    coefficient: number;
}
const color = (coefficient: number) => {
    if (coefficient < 50) return "bg-green-500";
    if (coefficient < 75) return "bg-yellow-500";
    return "bg-red-500";
}
function Coef({coefficient}: CoefProps) {
  return (
    <Progress value={coefficient} indicatorColor={color(coefficient)} />
  )
}

export default Coef