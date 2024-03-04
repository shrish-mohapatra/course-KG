import { ConfigProvider, theme } from "antd"
import Graph from "./components/Graph"
import GroupGraph from "./components/GroupGraph"
import Overlay from "./components/Overlay"
import PackCircles from "./components/PackCircles"
import { GraphProvider } from "./context/GraphContext"

const example1405KG = {
  nodes: [
    { id: 1, name: "Computational Thinking and Problem Solving" },
    { id: 2, name: "Data Representation" },
    { id: 3, name: "Intro to Python" },
    { id: 4, name: "Control Structures and Branching" },
    { id: 5, name: "Logical Operators and Boolean Values" },
    { id: 6, name: "Control Structures and Looping" },
    { id: 7, name: "Nested Looping Structures" },
    { id: 8, name: "File Input and Output" },
    { id: 9, name: "Functions and Function Scope" },
    { id: 10, name: "Linear Collections" },
    { id: 11, name: "String Operations" },
    { id: 12, name: "Associative Collections" },
    { id: 13, name: "Complexity Analysis" },
    { id: 14, name: "Binary Searching" },
    { id: 15, name: "Sorting" },
    { id: 16, name: "Recursion" },
    { id: 17, name: "Recursive Sorting", }
  ],
  labels: [
    { id: 1, name: "pre-req" },
    { id: 2, name: "related" },
  ],
  edges: [
    { source: 1, target: 2, label: 1 },
    { source: 3, target: 4, label: 1 },
    { source: 3, target: 5, label: 1 },
    { source: 3, target: 6, label: 1 },
    { source: 3, target: 8, label: 1 },
    { source: 3, target: 11, label: 1 },
    { source: 3, target: 9, label: 1 },
    { source: 6, target: 7, label: 1 },
    { source: 10, target: 12, label: 2 },
    { source: 16, target: 17, label: 1 },
    { source: 15, target: 17, label: 1 },
    { source: 9, target: 16, label: 1 },
    { source: 14, target: 15, label: 2 },
  ],
}

function App() {
  return (
    <>
      {/* <Graph KGData={example1405KG} /> */}
      <GraphProvider>
        <ConfigProvider theme={{ algorithm: theme.darkAlgorithm }}>
          <Overlay />
        </ConfigProvider>
        <GroupGraph />
      </GraphProvider>
    </>
  )
}

export default App
