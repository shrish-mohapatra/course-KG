import Controls from "./controls"
import GraphModeSwitcher from "./graph-mode-switcher"
import ProjectSwitcher from "./project-switcher"

const Overlay = () => {
  return (
    <>
      <div className="absolute top-6 left-6">
        <ProjectSwitcher />
      </div>
      <div className="absolute top-6 right-6">
        <GraphModeSwitcher />
      </div>
      <div className="absolute top-[calc(50%-74px)] left-6">
        <Controls/>
      </div>
    </>
  )
}

export default Overlay