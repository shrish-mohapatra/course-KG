import MiniButton from "@/components/mini-button";
import { GraphContext } from "@/context/GraphProvider";
import { useContext, useState } from "react";

const AddNode = () => {
  const [nodeName, setNodeName] = useState("");
  const { setGraphData, graphRef } = useContext(GraphContext);
  const handleAdd = () => {
    if (!nodeName || !graphRef || !graphRef.current) return;
    console.log("adding node", nodeName);
    // console.log(graphRef.current.getGraphBbox())
    setGraphData((curData) => {
      console.log(curData);
      return {
        nodes: [
          ...curData.nodes,
          {
            id: nodeName,
            value: 1,
          },
        ],
        links: curData.links,
      };
    });
    setNodeName("");
    setTimeout(
      () => graphRef.current.zoomToFit(400, 300, (node) => node.id == nodeName),
      200
    );
  };

  return (
    <div className="h-full flex flex-col justify-between">
      <div>
        <h1 className="text-accent">add node</h1>
        <p className="text-xs text-zinc-300">
          Provide a name for the new node to add to the graph.
        </p>
      </div>
      <div className="flex justify-between mb-2">
        <input
          className="text-white text-xs focus:text-accent bg-transparent border-b border-white focus:border-accent outline-none w-[120px]"
          placeholder="Enter name of node"
          value={nodeName}
          onChange={(e) => setNodeName(e.target.value)}
        />
        <MiniButton title="add" onClick={handleAdd} />
      </div>
    </div>
  );
};

export default AddNode;
