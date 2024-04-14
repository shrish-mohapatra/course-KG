import { GraphContext } from "@/context/GraphProvider";
import { useContext } from "react";

const AddEdge = () => {
  const { sourceNode } = useContext(GraphContext);

  return (
    <div className="h-full flex flex-col justify-between">
      <div>
        <h1 className="text-accent">add edge</h1>
        <p className="text-xs text-zinc-300">
          Creating an edge involves selecting source and target nodes.
        </p>
      </div>
      <div className="text-xs">
        <p>
          Please select a <b className="text-accent">{sourceNode ? "target" : "source"}</b> node
        </p>
      </div>
    </div>
  );
};

export default AddEdge;
