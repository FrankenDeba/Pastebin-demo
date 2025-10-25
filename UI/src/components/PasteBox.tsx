import React from "react";

export default function PasteBox({passPaste}: {passPaste: (paste: string) => void}) {
    const [paste, setPaste] = React.useState("");
  return (
    <div className="paste-box">
      <textarea placeholder="Enter your paste here..." rows={10} cols={50} onChange={e => setPaste(e.target.value)}></textarea>
      <br />
      <div className="btn-holder" onClick={() => passPaste(paste)}><button>Submit Paste</button></div>
    </div>
  );
}