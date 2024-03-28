import MiniButton from "@/components/mini-button"
import { Switch } from "@/components/ui/switch"

const GraphModeSwitcher = () => {
    return (
        <div className="flex gap-3">
            <MiniButton title="viewing"/>
            <Switch id="airplane-mode" />
        </div>
    )
}

export default GraphModeSwitcher