import Controls from "./controls"
import GraphModeSwitcher from "./graph-mode-switcher"
import NodeDetails from "./node-details"
import ProjectSwitcher from "./project-switcher"
import SaveAlert from "./save-alert"
import SearchNode from "./search-node"

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
        <Controls />
      </div>
      <div className="absolute top-0 left-0">
        <NodeDetails />
      </div>
      <SearchNode/>
      <SaveAlert/>
    </>
  )
}

export default Overlay