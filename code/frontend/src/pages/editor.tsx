import Head from "next/head";
import Link from "next/link";
import { Loader2 } from "lucide-react"
import Editor from "~/components/Editor";
import Navbar from "~/components/Navbar";
import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";
import { useState, useEffect } from "react";
import {toast} from "react-toastify";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import { Button } from "~/components/ui/button";
import { Progress } from "~/components/ui/progress";
import { apiUrl } from "~/lib/api";
import SimplifyButton from "~/components/SimplifyButton";
import Coef from "~/components/Coef";
interface PhrasesEstimated {
    sentence: string;
    coeff: number;
}

interface Proposition {
    id: number;
    sentence: string;
}

export default function Home() {
  const [text, setValue] = useState(`Il était une fois, une belle princesse qui s’appelait Morelle. Elle vivait avec son père et sa mère. Ils habitaient dans un grand château rempli d’or. La princesse était tellement belle que deux chevaliers d’un château lointain en étaient tombés amoureux.
Un jour, les deux princes Charles et George décidèrent d’aller lui demander sa main.Il était un fois, une petite fille très pauvre mais qui était très belle. Elle avait de jolis yeux, la peau douce et elle était intelligente et aussi très courageuse. Elle adorait chanter pour sa grand-mère. Mais sa grand-mère voulait être riche.
Un jour, sa grand-mère tomba malade et mourut. Isabelle se sentit terriblement mal et seule sans personne. Mais, elle reprit des forces plus vite que l’on ne crut.`);
  const [phrases, setPhrases] = useState<string[]>([]);
  const [PhraseEstimated, setApiResponse] = useState<PhrasesEstimated[]>([]);
  useEffect(() => {
    const timeOutID = setTimeout(() => {
        const image = text.match(/!\[image\]\(.*\)/g)
        const new_txt = text.replace(/!\[image\]\(.*\)/g, "");
        const phrases = new_txt.match(/(#+.*)|([^!?;.\n]+.)/g
        )?.map((phrase) => phrase.trim()) || [];
        setPhrases(phrases);
        }, 500);
        return () => clearTimeout(timeOutID);
  }, [text]);


  const generate_image = async (sentence: string) => {
    try{
    const response = fetch(`${apiUrl}/get_image`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({ "phrase": sentence }),
    });
    toast.promise(response, {
        pending: "Génération de l'image...",
        success: "Image générée avec succès.",
        error: "Erreur lors de la génération de l'image. Veuillez réessayer plus tard.",
    });
    const response_result = await response;
    const data = await response_result.json();
    console.log(data);
    const newText = text.replace(sentence, `${sentence} \n \n ![image](${apiUrl}/static/${data.url})\n \n`);
    setValue(newText);
    }
    catch (error) {
        toast.error("Erreur lors de la génération de l'image. Veuillez réessayer plus tard.");
    }
    }

  const evalutation = async (phrases: string[]) => {
    console.log(phrases);
    try{
    const response = await fetch(`${apiUrl}/check`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({ "sentences": phrases }),
    });
    const apiRes = await response.json();
    console.log(apiRes);
    setApiResponse(apiRes);
    }catch (error) {
        toast.error("Erreur lors de l'évaluation. Veuillez réessayer plus tard.");
    }
  }

  const handleSimplify = async (id: number, phrase: string) => {
    try{
    const response =  fetch(`${apiUrl}/simplify`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Allow-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({ phrase }),
    });
    toast.promise(response, {
        pending: "Simplification de la phrase...",
        success: "Phrase simplifiée avec succès.",
        error: "Erreur lors de la simplification de la phrase. Veuillez réessayer plus tard.",
    });
    const response_result = await response;
    const data = await response_result.json();
    // Replace the phrase with the simplified one
    const newText = text.replace(phrase, data.phrase);

    setValue(newText);

 
  
    }catch (error) {
    console.error(error);
}
  }

  useEffect(() => {
    evalutation(phrases);
  }
 , [phrases]);
  return (
    <>
      <Head>
        <title>Inclusio</title>
        <meta name="description" content="Editeur de text inclusif" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="flex justify-center">
        <Navbar />
      </div>
      <main className="min-h-screen py-2">
        <div className="container">
            <Editor value={text} setValue={setValue} />
        </div>
        <h1 className="text-center text-xl font-bold py-4">Simplification</h1>
        <Table>
        <TableHeader>
            <TableRow>
            <TableHead className="w-[100px]">ID</TableHead>
            <TableHead>Phrases</TableHead>
            <TableHead className="w-[200px]">Coefficien 0 - 100</TableHead>
            <TableHead className="w-[100px]">Simplify</TableHead>
            <TableHead className="w-[100px]">Image</TableHead>
            </TableRow>
        </TableHeader>
        <TableBody>
            {
                PhraseEstimated.map((phrase, index) => (
                    <TableRow key={index}>
                        <TableCell>{index}</TableCell>
                        <TableCell>{phrase.sentence}</TableCell>
                        <TableCell className="center-text text-center"><Coef coefficient={phrase.coeff} />
                        </TableCell>
                        <TableCell><SimplifyButton id={index} handleSimplify={handleSimplify} phrase={phrase.sentence}/></TableCell>
                        <TableCell><Button onClick={()=> {
                            generate_image(phrase.sentence);
                        }}>Image</Button></TableCell>
                    </TableRow>
                ))
            }
        </TableBody>
        </Table>
      </main>
    </>
  )
}
