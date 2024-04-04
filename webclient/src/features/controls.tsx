import { useContext } from "react"
import { GraphContext } from "@/context/GraphProvider"

import AddNodeIcon from "@/assets/AddNode.svg"
import AddEdgeIcon from "@/assets/AddEdge.svg"
import SortNodesIcon from "@/assets/SortNodes.svg"

const Controls = () => {
    const { editMode } = useContext(GraphContext)

    if (!editMode) return

    return (
        <div className="bg-black w-12 flex flex-col p-3 gap-5 rounded-[24px]">
            <img src={AddNodeIcon} className="cursor-pointer" />
            <img src={AddEdgeIcon} />
            <img src={SortNodesIcon} />
        </div>
    )
}

export default Controls