import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { GraphContext } from "@/context/GraphProvider"
import { useContext } from "react"

const projects = ["COMP 1405", "COMP 2406", "COMP 4601"]

const ProjectSwitcher = () => {
    const { editMode } = useContext(GraphContext)

    return (
        <Select disabled={editMode}>
            <SelectTrigger className="w-[180px]">
                <span className="text-foreground">project</span>
                <SelectValue />
            </SelectTrigger>
            <SelectContent>
                {
                    projects.map((project, index) => (
                        <SelectItem value={project} key={index}>{project}</SelectItem>
                    ))
                }
            </SelectContent>
        </Select>
    )
}

export default ProjectSwitcher