import { host } from "../utils/api";
import PasteBox from "./PasteBox";
import Url from "./Url";
// import Globe from "./ui/globe";

export default function Home() {
function passPaste(paste: string) {
    console.log("Received paste:", paste);
    fetch(`${host}/write`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ pasteText: paste }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Paste submitted successfully:", data);
        // You can add more logic here to handle the response data
    })
    .catch(error => {
        console.error("Error submitting paste:", error);
    }); 
  }

  async function readAllPastes() {
    const resp = await fetch(`${host}/read_all`);

    const data = await resp.json();

    console.log("All pastes:", data);
    
  }


  return (
    <div>
      <h1>Welcome to Pastebin Demo</h1>
      <p>This is the home page of the Pastebin Demo application.</p>
      <PasteBox passPaste={passPaste}/>  

      <Url />

      <button onClick={readAllPastes}>Read All Pastes</button>
    </div>
  );
}