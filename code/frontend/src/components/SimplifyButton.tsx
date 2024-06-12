import React from 'react'
import { Button } from './ui/button'
import { apiUrl } from '~/lib/api';
import { useState } from 'react';
import { toast} from 'react-toastify';
interface SimplifyButtonProps {
    id: number;
    handleSimplify: (id: number, phrase: string) => Promise<void>;
    phrase: string;
}

function SimplifyButton({id, handleSimplify, phrase}: SimplifyButtonProps) {

    const [loading, setLoading] = useState<boolean>(false);
    

  return (
    <Button onClick={() => {
        handleSimplify(id, phrase);
    }}>Simplify</Button>
  )
}

export default SimplifyButton