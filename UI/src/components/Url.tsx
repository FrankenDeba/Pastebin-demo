import { useState } from "react";
import "./style.css";

export default function Url({pasteUrl}: {pasteUrl: string  }) {
    const [copySuccess, setCopySuccess] = useState(false);

    async function copyToClipboard(){
        try{
            await navigator.clipboard.writeText(pasteUrl);
            setCopySuccess(true)
            setTimeout(() => {setCopySuccess(false)}, 2500)
        } catch(err){
            console.error("Failed to copy: ", err);
            setCopySuccess(false);
        }
    }

    return <div className="url" onClick={copyToClipboard}>{`${pasteUrl} ${copySuccess ? "Copied!" : "📋"}`}
    </div>;  
}