import { ThemeProvider } from "@/context/ThemeProvider"
import Graph from "./features/graph"
import Overlay from "./features/overlay"
import { GraphProvider } from "./context/GraphProvider"

function App() {

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <GraphProvider>
        <Graph />
        <Overlay />
      </GraphProvider>
    </ThemeProvider>
  )
}

export default App
