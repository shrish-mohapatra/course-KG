import {
  CommandDialog,
  CommandEmpty,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { GraphContext } from "@/context/GraphProvider";
import { useContext, useEffect, useState } from "react";

const SearchNode = () => {
  const { graphData, graphRef } = useContext(GraphContext);
  const [open, setOpen] = useState<boolean>(false);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  const selectNode = (nodeId: string) => {
    console.log("selected", nodeId)
    graphRef?.current.zoomToFit(400, 20, (node) => node.id == nodeId)
    setOpen(false)
  }

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Search for a node..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        {
            graphData.nodes.map((node, index) => (
                <CommandItem key={index} onSelect={selectNode}>
                    {node.id}
                </CommandItem>
            ))
        }
      </CommandList>
    </CommandDialog>
  );
};

export default SearchNode;
