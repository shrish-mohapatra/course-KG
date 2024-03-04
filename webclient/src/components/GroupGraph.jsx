import React, { useContext, useState } from 'react'
import ForceGraph3D from 'react-force-graph-3d'
import ForceGraph2D from 'react-force-graph-2d'
import SpriteText from 'three-spritetext'
import { GraphContext } from '../context/GraphContext'

const GroupGraph = () => {
  const { graphData, editMode, addLink, removeLink, pendingLink, setPendingLink } = useContext(GraphContext)
  const [linkQueue, setLinkQueue] = useState([])

  const handleClick = (node) => {
    if (!editMode) return
    if (!pendingLink) return
    if (linkQueue.length == 0) {
      setLinkQueue([node.id])
    } else {
      console.log(`creating link from ${linkQueue[0]} to ${node.id}`)
      addLink(linkQueue[0], node.id)
      setLinkQueue([])
      setPendingLink(false)
    }
  }

  const handleRightClick = (link) => {
    if (!editMode) return
    removeLink(link)
  }

  return (
    <ForceGraph2D
      graphData={graphData}
      nodeAutoColorBy="group"

      // nodeThreeObject={node => {
      //   const sprite = new SpriteText(node.id);
      //   sprite.color = node.color;
      //   sprite.textHeight = node.value;
      //   return sprite;
      // }}

      nodeCanvasObject={(node, ctx, globalScale) => {
        const label = node.id;
        const fontSize = node.value * 2 / globalScale;
        ctx.font = `${fontSize}px Sans-Serif`;
        const textWidth = ctx.measureText(label).width;
        const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2); // some padding

        ctx.fillStyle = 'rgba(0, 0, 0, 0)';
        ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = node.color;
        ctx.fillText(label, node.x, node.y);

        node.__bckgDimensions = bckgDimensions; // to re-use in nodePointerAreaPaint
      }}
      nodePointerAreaPaint={(node, color, ctx) => {
        ctx.fillStyle = color;
        const bckgDimensions = node.__bckgDimensions;
        bckgDimensions && ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
      }}

      linkDirectionalArrowLength={4}
      linkColor={() => "rgba(255, 255, 255, 0.2)"}

      showNavInfo={false}
      backgroundColor='#141414'
      // enableNavigationControls={!editMode}
      // enableNodeDrag={!editMode}
      d3VelocityDecay={editMode ? 0.8 : 0.4}

      onNodeClick={handleClick}
      onLinkRightClick={handleRightClick}

      dagMode={editMode ? "" : "td"}
      dagLevelDistance={20}
    />
  )
}

export default GroupGraph