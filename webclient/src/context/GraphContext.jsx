import React, { createContext, useState } from 'react'
import MyData from "./webdev-mindmap-shrish.json"
import LLMDataSM from "./llm-mindmap-sm.json"
import LLMDataLG from "./llm-kg-lg.json"

// const INITIAL_DATA = {
//     nodes: [
//         { group: 0, id: "intro to JS", value: 8 },
//         { group: 1, id: "DOM", value: 8 },
//         { group: 1, id: "AJAX", value: 8 },
//         { group: 2, id: "intro to node.js", value: 8 },
//         { group: 2, id: "NPM", value: 8 },
//         { group: 2, id: "GraphQL", value: 8 },
//     ],
//     links: [
//         { source: "intro to JS", target: "DOM" },
//         { source: "DOM", target: "AJAX" },
//         { source: "intro to JS", target: "intro to node.js" },
//         { source: "intro to node.js", target: "NPM" },
//         { source: "NPM", target: "GraphQL" },
//     ]
// }

const loadFromJson = (initData) => {
    // add value to nodes
    initData.nodes = initData.nodes.map(node => ({...node, value: node.value || 8}))
    return {...initData}
}


export const GraphContext = createContext()

export const GraphProvider = ({ children }) => {
    // const [graphData, setGraphData] = useState({ nodes: [], links: []})
    const [graphData, setGraphData] = useState(loadFromJson(MyData))
    // const [graphData, setGraphData] = useState(loadFromJson(LLMDataLG))
    // const [graphData, setGraphData] = useState(initData)
    const [editMode, setEditMode] = useState(true)
    const [pendingLink, setPendingLink] = useState(false)
    const [selectedNode, setSelectedNode] = useState()
    const [dagMode, setDagMode] = useState()

    const addNode = (name = null) => {
        setGraphData(curData => {
            const newID = "Node " + curData.nodes.length
            const defaultValue = 8
            return {
                nodes: [
                    ...curData.nodes,
                    {
                        id: name || newID,
                        value: defaultValue
                    }
                ],
                links: curData.links
            }
        })
    }

    const addLink = (source, target) => {
        if (source == target) return

        setGraphData(curData => ({
            nodes: curData.nodes,
            links: [
                ...curData.links,
                { source, target }
            ]
        }))
    }

    const removeLink = (link) => {
        setGraphData(curData => {
            const newLinks = [...curData.links]
            newLinks.splice(link.index, 1)
            return {
                nodes: curData.nodes,
                links: newLinks
            }
        })
    }

    const waitForLink = () => {
        setPendingLink(true)
    }

    return (
        <GraphContext.Provider
            value={{
                graphData,
                editMode, setEditMode,
                addNode, addLink,
                removeLink,

                pendingLink, setPendingLink, waitForLink,
                selectedNode, setSelectedNode,
                dagMode, setDagMode
            }}
        >
            {children}
        </GraphContext.Provider>
    )
}