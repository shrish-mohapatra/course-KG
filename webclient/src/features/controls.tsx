import { useContext } from "react";
import { GraphContext } from "@/context/GraphProvider";

import AddNodeIcon from "@/components/AddNodeIcon";
import AddEdgeIcon from "@/components/AddEdgeIcon";
import SortNodesIcon from "@/components/SortNodesIcon";

import AddNode from "./add-node";
import SortNodes from "./sort-nodes";
import AddEdge from "./add-edge";

const CONTROL_PANELS: { [key: string]: JSX.Element } = {
  node: <AddNode />,
  edge: <AddEdge />,
  sort: <SortNodes />,
};

const Controls = () => {
  const { editMode, setEditAction, editAction } = useContext(GraphContext);

  const handleClick = (actionType: string) => {
    setEditAction((prevActionType) =>
      prevActionType == actionType ? "" : actionType
    );
  };

  return (
    <div
      className="bg-black p-3 rounded-[24px]"
      style={{
        display: editMode ? "flex" : "none",
        width: editAction == "" ? 48 : 256,
      }}
    >
      <div className="flex flex-col gap-5">
        <div className="cursor-pointer" onClick={() => handleClick("node")}>
          <AddNodeIcon color={editAction == "node" ? "#da652f" : "#6B6B6B"} />
        </div>
        <div className="cursor-pointer" onClick={() => handleClick("edge")}>
          <AddEdgeIcon color={editAction == "edge" ? "#da652f" : "#6B6B6B"} />
        </div>
        <div className="cursor-pointer" onClick={() => handleClick("sort")}>
          <SortNodesIcon color={editAction == "sort" ? "#da652f" : "#6B6B6B"} />
        </div>
      </div>

      <div className="bg-background w-full rounded-[24px] ml-3 p-3">
        {CONTROL_PANELS[editAction]}
      </div>
    </div>
  );
};

export default Controls;
