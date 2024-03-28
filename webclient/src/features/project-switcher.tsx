import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

const projects = ["COMP 1405", "COMP 2406", "COMP 4601"]

const ProjectSwitcher = () => {
    return (
        <Select value="COMP 2406">
            <SelectTrigger className="w-[180px]">
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