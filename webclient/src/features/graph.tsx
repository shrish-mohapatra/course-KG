import { GraphContext } from "@/context/GraphProvider"
import { useContext } from "react"
import ForceGraph from "react-force-graph-2d"

const COLORS = ["#68C651", "#5351C6", "#C6519E", "#C65151", "#51B1C6"]

const Graph = () => {
    const { graphData } = useContext(GraphContext)

    return (
        <ForceGraph
            graphData={graphData}
            nodeCanvasObject={(node, ctx, globalScale) => {
                const label = node.id;
                if (!label || typeof label !== "string") return
                
                const fontSize = (node.value || 8) * 2 / globalScale;
                ctx.font = `${fontSize}px Sans-Serif`;
                const textWidth = ctx.measureText(label).width;
                const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

                if (node.x && node.y) {
                    ctx.fillStyle = 'rgba(0, 0, 0, 0)';
                    ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = node.group ? COLORS[node.group] : COLORS[0];
                    ctx.fillText(label, node.x, node.y);
                }

                node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
            }}
            nodePointerAreaPaint={(node, color, ctx) => {
                ctx.fillStyle = color;
                const bckgDimensions = node.__bckgDimensions;
                if (node.x && node.y) {
                    bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
                }
            }}
            linkDirectionalArrowLength={4}
            linkColor={() => "rgba(255, 255, 255, 0.2)"}
            backgroundColor='#141414'
        />
    )
}

export default Graph