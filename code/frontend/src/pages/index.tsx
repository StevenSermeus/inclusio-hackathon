import Head from "next/head";
import Link from "next/link";
import Editor from "~/components/Editor";
import Navbar from "~/components/Navbar";
import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";
export default function Home() {
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
      <main className="flex min-h-screen py-2">
        <h1>Editeur de texte inclusif</h1> 
      </main>
    </>
  );
}
