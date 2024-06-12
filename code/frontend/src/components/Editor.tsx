import React from "react";

import rehypeSanitize from "rehype-sanitize";
import { ICommand } from "@uiw/react-md-editor";
import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";
import dynamic from "next/dynamic";
import { comma } from "postcss/lib/list";
import { useTheme } from "next-themes";

const MDEditor = dynamic(
  () => import("@uiw/react-md-editor").then((mod) => mod.default),
  { ssr: false },
);

interface EditorProps {
    value: string;
    setValue: (value: string) => void;
    }

export default function Editor({ value, setValue }: EditorProps) {
    const { theme, setTheme } = useTheme();

  return (
    <div data-color-mode={theme || "light"}>
      <MDEditor
        commandsFilter={(command: ICommand, isExtra: boolean)=> {
            if (command.name === "italic") return false;
            return command;
        }}
        value={value}
        onChange={(value) => {
          setValue(value || "");
        }}
        previewOptions={{
          rehypePlugins: [[rehypeSanitize]],
        }}
        height={500}
      />
    </div>
  );
}
