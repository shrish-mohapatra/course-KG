import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { GraphContext } from "@/context/GraphProvider";
import { updateKnowledgeGraph } from "@/context/api";
import { useContext, useEffect, useState } from "react";

const SaveAlert = () => {
  const { graphData } = useContext(GraphContext);
  const [open, setOpen] = useState<boolean>(false);
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "s" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        if(graphData && graphData.projectName) {
            setOpen(true);
        }
      }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, [graphData]);

  const handleSave = () => {
    updateKnowledgeGraph(graphData.projectName, graphData);
    setOpen(false);
  };

  const handleCancel = () => {
    setOpen(false);
  };

  return (
    <AlertDialog open={open}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Would you like to save changes?</AlertDialogTitle>
          <AlertDialogDescription>
            Changes to the knowledge graph including new/removed nodes/edges
            will be saved to the database.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={handleCancel}>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={handleSave}
            className="bg-accent text-white"
          >
            Continue
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
};

export default SaveAlert;
