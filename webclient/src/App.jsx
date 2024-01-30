import Graph from "./components/Graph"

const exampleKGData = {
  nodes: [
    { id: 1, name: 'Sorting' },
    { id: 2, name: 'Recursion' },
    { id: 3, name: 'Recursive Sorting' },
    { id: 4, name: 'Binary Search' },
  ],
  edges: [
    { source: 1, target: 3, label: "pre-req" },
    { source: 2, target: 3, label: "pre-req" },
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
