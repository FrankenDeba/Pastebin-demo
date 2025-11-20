export default function AllPastes({ allPastes }: { allPastes: any[] }) {
     return (<>{
        allPastes.length > 0 && (
          <div className="all-pastes">
            <h2>All Pastes:</h2>
            <ul>
              {allPastes.map((paste, index) => (
                <li key={index} className="paste-item">{paste.paste}</li>
              ))}
            </ul>
          </div>
        ) 
      }</>)
    }