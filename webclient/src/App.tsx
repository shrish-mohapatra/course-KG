import { ThemeProvider } from "./components/theme-provider"
import Graph from "./features/graph"
import Overlay from "./features/overlay"

function App() {

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Graph/>
      <Overlay/>
    </ThemeProvider>
  )
}

export default App
