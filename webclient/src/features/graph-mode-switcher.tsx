import MiniButton from "@/components/mini-button"
import { Switch } from "@/components/ui/switch"
import { GraphContext } from "@/context/GraphProvider"
import { useContext } from "react"

const GraphModeSwitcher = () => {
    const { editMode, setEditMode } = useContext(GraphContext)

    const handleSwitch = () => {
        setEditMode(curMode => !curMode)
    }

    return (
        <div className="flex gap-3">
            <MiniButton title={editMode ? "editing" : "viewing"}/>
            <Switch checked={editMode} onCheckedChange={handleSwitch} />
        </div>
    )
}

export default GraphModeSwitcher