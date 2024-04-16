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
import { getKnowledgeGraph, getProjects, updateKnowledgeGraph } from "./api";

const SAMPLE_GRAPH_DATA: GraphData = {
  nodes: [
    {
      id: "COMP 4905",
      group: 0,
      value: 2,
    },
    {
      id: "course-kg",
      group: 0,
      value: 2,
    },
    {
      id: "shrish mohapatra",
      group: 0,
      value: 2,
    },
  ],
  links: [
    {
      source: "course-kg",
      target: "COMP 4905",
      relationship: "developed for",
    },
    {
      source: "course-kg",
      target: "shrish mohapatra",
      relationship: "developed by",
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
    const { nodes, edges, contributors, project_name } = newKG;

    const node_id_to_index: { [key: number]: number } = {};

    for (let i = 0; i < nodes.length; i++) {
      node_id_to_index[nodes[i].id] = i;
      nodes[i].contributors = contributors
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
      projectName,
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
