import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { GraphContext } from "@/context/GraphProvider"
import { useContext } from "react"

const ProjectSwitcher = () => {
    const { projects, editMode, selectProject } = useContext(GraphContext)

    const handleValueChange = (newValue: string) => {
        selectProject(newValue)
    }

    const formatProject = (projectValue: string) => {
        const mask = "2024-04-04 02:47:17.119678"
        const end = projectValue.length - mask.length
        return projectValue.slice(0, end)
    }

    if (!projects) return

    return (
        <Select
            disabled={editMode}
            onValueChange={handleValueChange}
        >
            <SelectTrigger className="w-[220px] backdrop-filter backdrop-blur-lg">
                <span className="text-foreground">project</span>
                <SelectValue placeholder="select a project"/>
            </SelectTrigger>
            <SelectContent>
                {
                    projects.map((project, index) => (
                        <SelectItem value={project} key={index}>
                            {formatProject(project)}
                        </SelectItem>
                    ))
                }
            </SelectContent>
        </Select>
    )
}

export default ProjectSwitcher