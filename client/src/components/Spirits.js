import { useContext, useState } from "react"
import { SpiritContext } from "../context/SpiritContext"
import NewSpiritForm from "./NewSpiritForm"


function Spirits() {
    const { spirits } = useContext(SpiritContext)
    const [showSpiritForm, setShowSpiritForm] = useState(false)

    console.log(spirits)

    return (
        <div>
            <h2>Spirits</h2>
            {spirits?.map(spirit => <p>{spirit.name}</p>)}
            {/* change above to individual spirit elements */}
            {showSpiritForm ? (
                <NewSpiritForm setShowSpiritForm={setShowSpiritForm}/>
            ) : (
                <button onClick={() => setShowSpiritForm(true)}>+ Add Spirit</button>
            )}
        </div>
    )
}

export default Spirits