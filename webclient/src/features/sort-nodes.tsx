import MiniButton from "@/components/mini-button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { GraphContext } from "@/context/GraphProvider";
import { DagMode } from "@/types";
import { useContext, useState } from "react";

type DAG_ALGO = {
  dag: string;
  label: string;
};

const DAG_ALGOS: DAG_ALGO[] = [
  { dag: "td", label: "Top Down" },
  { dag: "bu", label: "Bottom Up" },
  { dag: "lr", label: "Left-right" },
  { dag: "rl", label: "Right-left" },
  { dag: "radialout", label: "Radial Out" },
  { dag: "radialin", label: "Radial In" },
  { dag: "-", label: "None" },
];

const SortNodes = () => {
  const { setSortMode } = useContext(GraphContext);
  const [algo, setAlgo] = useState<string>();

  const handleSort = () => {
    console.log("sorting nodes", algo);
    let sortMode = algo;
    if (sortMode == "-") {
      sortMode = undefined;
    }
    setSortMode(sortMode as DagMode);
  };

  const handleAlgoChange = (newAlgo: string) => {
    setAlgo(newAlgo);
  };

  return (
    <div className="h-full flex flex-col justify-between">
      <div>
        <h1 className="text-accent">sort nodes</h1>
        <p className="text-xs text-zinc-300">
          Sort graph using preset DAG sorting algorithms.
        </p>
      </div>
      <div className="flex justify-between">
        <Select onValueChange={handleAlgoChange}>
          <SelectTrigger className="text-xs m-0 p-1 h-6 w-[120px]">
            <SelectValue placeholder="Select algo" />
          </SelectTrigger>
          <SelectContent>
            {DAG_ALGOS.map((dagAlgo, index) => (
              <SelectItem value={dagAlgo.dag} key={index}>
                {dagAlgo.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <MiniButton title="sort" onClick={handleSort} />
      </div>
    </div>
  );
};

export default SortNodes;
