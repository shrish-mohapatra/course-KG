import ForceGraph from "react-force-graph-2d"

const graphData = {
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

const COLORS = ["#68C651", "#5351C6", "#C6519E", "#C65151", "#51B1C6"]

const Graph = () => {
    return (
        <ForceGraph
            graphData={graphData}
            nodeCanvasObject={(node, ctx, globalScale) => {
                const label = node.id;
                const fontSize = (node.value || 8) * 2 / globalScale;
                ctx.font = `${fontSize}px Sans-Serif`;
                const textWidth = ctx.measureText(label).width;
                const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

                if(node.x && node.y) {
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
                if(node.x && node.y) {
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