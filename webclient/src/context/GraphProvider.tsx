import { Dispatch, SetStateAction, createContext, useState, ReactNode } from "react";
import { GraphData, NodeObject } from "react-force-graph-2d";

const SAMPLE_GRAPH_DATA: GraphData = {
    "nodes": [
        {
            "id": "intro to JS",
            "group": 0,
            "value": 8
        },
        {
            "id": "DOM",
            "group": 1,
            "value": 8
        },
        {
            "id": "AJAX",
            "group": 1,
            "value": 8
        },
        {
            "id": "intro to node.js",
            "group": 2,
            "value": 8
        },
        {
            "id": "NPM",
            "group": 2,
            "value": 8
        },
        {
            "id": "GraphQL",
            "group": 2,
            "value": 8
        },
        {
            "id": "promises",
            "value": 8
        },
        {
            "id": "templates",
            "group": 2,
            "value": 8
        },
        {
            "id": "comp 2406",
            "group": 3,
            "value": 8
        },
        {
            "id": "middleware",
            "group": 2,
            "value": 8
        }
    ],
    "links": [
        {
            "source": "intro to JS",
            "target": "DOM"
        },
        {
            "source": "DOM",
            "target": "AJAX"
        },
        {
            "source": "intro to JS",
            "target": "intro to node.js"
        },
        {
            "source": "intro to node.js",
            "target": "NPM"
        },
        {
            "source": "intro to JS",
            "target": "promises"
        },
        {
            "source": "NPM",
            "target": "templates"
        },
        {
            "source": "comp 2406",
            "target": "intro to JS"
        },
        {
            "source": "NPM",
            "target": "middleware"
        }
    ]
}

interface GraphContextProps {
    graphData: GraphData;
    setGraphData: Dispatch<SetStateAction<GraphData>>;
    editMode: boolean;
    setEditMode: Dispatch<SetStateAction<boolean>>;
    selectedNode: NodeObject | undefined;
    setSelectedNode: Dispatch<SetStateAction<NodeObject | undefined>>;
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
})

export const GraphProvider: React.FC<GraphProviderProps> = ({ children }) => {
    const [graphData, setGraphData] = useState(SAMPLE_GRAPH_DATA)
    const [editMode, setEditMode] = useState(false)
    const [selectedNode, setSelectedNode] = useState<NodeObject | undefined>()

    return (
        <GraphContext.Provider
            value={{
                graphData, setGraphData,
                editMode, setEditMode,
                selectedNode, setSelectedNode,
            }}
        >
            {children}
        </GraphContext.Provider>
    )
}