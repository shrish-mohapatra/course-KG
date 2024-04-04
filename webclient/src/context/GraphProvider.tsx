import { ProjectList } from "@/types";
import { Dispatch, SetStateAction, createContext, useState, ReactNode, useEffect } from "react";
import { GraphData, NodeObject } from "react-force-graph-2d";
import { getKnowledgeGraph, getProjects } from "./api";

const SAMPLE_GRAPH_DATA: GraphData = {
    "nodes": [
        {
            "id": "course-kg",
            "group": 0,
            "value": 8
        },
        {
            "id": "developed by",
            "group": 0,
            "value": 8
        },
        {
            "id": "shrish mohapatra",
            "group": 0,
            "value": 8
        },
    ],
    "links": [
        {
            "source": "course-kg",
            "target": "developed by",
        },
        {
            "source": "developed by",
            "target": "shrish mohapatra"
        },
    ]
}

interface GraphContextProps {
    graphData: GraphData;
    setGraphData: Dispatch<SetStateAction<GraphData>>;
    editMode: boolean;
    setEditMode: Dispatch<SetStateAction<boolean>>;
    selectedNode: NodeObject | undefined;
    setSelectedNode: Dispatch<SetStateAction<NodeObject | undefined>>;
    projects: ProjectList | undefined;
    selectProject: (projectName: string) => void;
}

interface GraphProviderProps {
    children: ReactNode;
}

export const GraphContext = createContext<GraphContextProps>({
    graphData: { nodes: [], links: [] },
    setGraphData: () => { },
    editMode: false,
    setEditMode: () => { },
    selectedNode: {},
    setSelectedNode: () => { },
    projects: [],
    selectProject: () => { },
})

export const GraphProvider: React.FC<GraphProviderProps> = ({ children }) => {
    const [graphData, setGraphData] = useState(SAMPLE_GRAPH_DATA)
    const [editMode, setEditMode] = useState(false)
    const [selectedNode, setSelectedNode] = useState<NodeObject>()

    const [projects, setProjects] = useState<ProjectList>()

    useEffect(() => {
        getProjects().then(newProjects => setProjects(newProjects))
    }, [])

    const selectProject = async (projectName: string) => {
        const newKG = await getKnowledgeGraph(projectName)
        const newGraphData = {
            nodes: newKG.nodes.map(node => ({
                ...node,
                value: node.sources.length * 8
            })),
            links: newKG.edges,
        }

        setGraphData(newGraphData)
    }

    return (
        <GraphContext.Provider
            value={{
                graphData, setGraphData,
                editMode, setEditMode,
                selectedNode, setSelectedNode,
                projects, selectProject,
            }}
        >
            {children}
        </GraphContext.Provider>
    )
}