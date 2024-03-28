import GraphModeSwitcher from "./graph-mode-switcher"
import ProjectSwitcher from "./project-switcher"

const Overlay = () => {
  return (
    <div className="top-0 left-0 absolute flex justify-between p-6 w-full">
      <ProjectSwitcher/>
      <GraphModeSwitcher/>
    </div>
  )
}

export default Overlay