import Graph from "./components/Graph"

const exampleKGData = {
  nodes: [
    { id: 1, name: 'Sorting' },
    { id: 2, name: 'Recursion' },
    { id: 3, name: 'Recursive Sorting' },
    { id: 4, name: 'Binary Search' },
  ],
  edges: [
    { source: 1, target: 3, label: 1 },
    { source: 2, target: 3, label: 1 },
    { source: 4, target: 1, label: 2 },
  ],
  labels: [
    { id: 1, name: "pre-req" },
    { id: 2, name: "requires" },
  ]
}

function App() {
  return (
    <>
      <Graph KGData={exampleKGData} />
    </>
  )
}

export default App
