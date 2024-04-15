import { GraphContext } from "@/context/GraphProvider";
import { useContext } from "react";
import ForceGraph, { LinkObject, NodeObject } from "react-force-graph-2d";

const COLORS = [
  "#cccccc",
  "#68C651",
  "#5351C6",
  "#C6519E",
  "#C65151",
  "#51B1C6",
];

const Graph = () => {
  const {
    graphRef,
    graphData,
    setGraphData,
    setSelectedNode,
    editMode,
    editAction,
    sortMode,
    sourceNode,
    setSourceNode,
  } = useContext(GraphContext);

  const handleNodeClick = (node: NodeObject) => {
    if (!editMode || editAction != "edge") return;
    if (sourceNode != "") {
      console.log("create edge from", sourceNode, node.id);
      setGraphData((curData) => ({
        nodes: curData.nodes,
        links: [...curData.links, { source: sourceNode, target: node.id }],
      }));
      setSourceNode("");
    } else {
      setSourceNode(node.id as string);
    }
  };

  const handleNodeRightClick = (node: NodeObject) => {
    if (editMode) {
      console.log("removing node", node);
      setGraphData((curData) => {
        const newNodes = [...curData.nodes];
        let newLinks = [...curData.links];

        newLinks = newLinks.filter((link) => {
          console.log(link);
          return link.source != node && link.target != node;
        });
        newNodes.splice(node.index, 1);

        return {
          nodes: newNodes,
          links: newLinks,
        };
      });
    } else {
      setSelectedNode(node);
    }
  };

  const handleLinkRightClick = (link: LinkObject) => {
    if (!editMode) return;
    console.log("removing link", link);
    setGraphData((curData) => {
      const newLinks = [...curData.links];
      newLinks.splice(link.index, 1);
      return {
        nodes: curData.nodes,
        links: newLinks,
      };
    });
  };

  return (
    <ForceGraph
      ref={graphRef ? graphRef : undefined}
      graphData={graphData}
      nodeCanvasObject={(node, ctx, globalScale) => {
        const label = node.id;
        const value = node.value || 1;
        if (!label || typeof label !== "string") return;

        // const fontSize = (node.value || 8) * 2 / globalScale;
        const fontSize = (10 * (1 + value / 5)) / globalScale;

        if (value < 1 / globalScale) {
          ctx.fillStyle = node.group ? COLORS[node.group] : COLORS[0];
          if (node.id == sourceNode) {
            console.log("condition met");
            ctx.fillStyle = "#da652f";
          }
          ctx.beginPath();
          ctx.arc(node.x, node.y, value * 2, 0, 2 * Math.PI, false);
          ctx.fill();
          return;
        }
        // console.log(label, fontSize)
        // const fontSize = (8) * 2 / globalScale;
        ctx.font = `${fontSize}px Sans-Serif`;
        const textWidth = ctx.measureText(label).width;
        const bckgDimensions = [textWidth, fontSize].map(
          (n) => n + fontSize * 0.2
        ); // some padding

        if (node.x && node.y) {
          ctx.fillStyle = "rgba(0, 0, 0, 0)";
          ctx.fillRect(
            node.x - bckgDimensions[0] / 2,
            node.y - bckgDimensions[1] / 2,
            ...bckgDimensions
          );

          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillStyle = node.group ? COLORS[node.group] : COLORS[0];
          ctx.fillText(label, node.x, node.y);
        }

        node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
      }}
      nodePointerAreaPaint={(node, color, ctx) => {
        ctx.fillStyle = color;
        const bckgDimensions = node.__bckgDimensions;
        if (node.x && node.y) {
          bckgDimensions &&
            ctx.fillRect(
              node.x - bckgDimensions[0] / 2,
              node.y - bckgDimensions[1] / 2,
              ...bckgDimensions
            );
        }
      }}
      linkLabel={(link) => {
        return link.relationship
      }}
      linkDirectionalArrowLength={4}
      linkColor={() => "rgba(255, 255, 255, 0.2)"}
      backgroundColor="#141414"
      onNodeClick={handleNodeClick}
      onNodeRightClick={handleNodeRightClick}
      onLinkRightClick={handleLinkRightClick}
      d3VelocityDecay={editMode ? 0.8 : 0.4}
      dagMode={sortMode}
    />
  );
};

export default Graph;
