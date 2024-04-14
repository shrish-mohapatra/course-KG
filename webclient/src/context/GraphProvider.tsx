import { DagMode, ProjectList } from "@/types";
import {
  Dispatch,
  SetStateAction,
  createContext,
  useState,
  ReactNode,
  useEffect,
  useRef,
  MutableRefObject,
} from "react";
import { ForceGraphMethods, GraphData, NodeObject } from "react-force-graph-2d";
import { getKnowledgeGraph, getProjects } from "./api";

const SAMPLE_GRAPH_DATA: GraphData = {
  nodes: [
    {
      id: "course-kg",
      group: 0,
      value: 8,
    },
    {
      id: "developed by",
      group: 0,
      value: 8,
    },
    {
      id: "shrish mohapatra",
      group: 0,
      value: 8,
    },
  ],
  links: [
    {
      source: "course-kg",
      target: "developed by",
    },
    {
      source: "developed by",
      target: "shrish mohapatra",
    },
  ],
};

interface GraphContextProps {
  graphData: GraphData;
  setGraphData: Dispatch<SetStateAction<GraphData>>;
  editMode: boolean;
  setEditMode: Dispatch<SetStateAction<boolean>>;
  selectedNode: NodeObject | undefined;
  setSelectedNode: Dispatch<SetStateAction<NodeObject | undefined>>;
  projects: ProjectList | undefined;
  selectProject: (projectName: string) => void;
  editAction: string;
  setEditAction: Dispatch<SetStateAction<string>>;
  graphRef: MutableRefObject<ForceGraphMethods> | null;
  sortMode: DagMode;
  setSortMode: Dispatch<SetStateAction<DagMode>>;
  sourceNode: string;
  setSourceNode: Dispatch<SetStateAction<string>>;
}

interface GraphProviderProps {
  children: ReactNode;
}

export const GraphContext = createContext<GraphContextProps>({
  graphData: { nodes: [], links: [] },
  setGraphData: () => {},
  editMode: false,
  setEditMode: () => {},
  selectedNode: {},
  setSelectedNode: () => {},
  projects: [],
  selectProject: () => {},
  editAction: "",
  setEditAction: () => {},
  graphRef: null,
  sortMode: undefined,
  setSortMode: () => {},
  sourceNode: "",
  setSourceNode: () => {},
});

export const GraphProvider: React.FC<GraphProviderProps> = ({ children }) => {
  const [graphData, setGraphData] = useState(SAMPLE_GRAPH_DATA);
  const [editMode, setEditMode] = useState(false);
  const [selectedNode, setSelectedNode] = useState<NodeObject>();
  const [editAction, setEditAction] = useState("");
  const [sortMode, setSortMode] = useState<DagMode>();
  const [sourceNode, setSourceNode] = useState("");

  const [projects, setProjects] = useState<ProjectList>();

  const graphRef = useRef<any>(null);

  useEffect(() => {
    getProjects().then((newProjects) => setProjects(newProjects));
  }, []);

  const selectProject = async (projectName: string) => {
    const newKG = await getKnowledgeGraph(projectName);
    const { nodes, edges } = newKG;

    const node_id_to_index: { [key: number]: number } = {};

    for (let i = 0; i < nodes.length; i++) {
      node_id_to_index[nodes[i].id] = i;
    }

    // Assign node value based on # of source edges
    for (let edge of edges) {
      const id1 = edge.source;
      const node_index = node_id_to_index[id1];
      if (!nodes[node_index].value) {
        nodes[node_index].value = 0;
      }
      nodes[node_index].value += 1;
    }

    const newGraphData = {
      nodes,
      links: edges,
    };

    setGraphData(newGraphData);
  };

  return (
    <GraphContext.Provider
      value={{
        graphRef,
        graphData,
        setGraphData,
        editMode,
        setEditMode,
        selectedNode,
        setSelectedNode,
        projects,
        selectProject,
        editAction,
        setEditAction,
        sortMode,
        setSortMode,
        sourceNode,
        setSourceNode,
      }}
    >
      {children}
    </GraphContext.Provider>
  );
};
