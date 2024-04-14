import Draggable from 'react-draggable'

import MiniButton from "@/components/mini-button"
import AddNodeIcon from "@/assets/AddNode.svg"
import { useContext, useEffect, useRef, useState } from 'react'
import { GraphContext } from '@/context/GraphProvider'

const SAMPLE_NODE = {
    id: "Express",
    notes: "Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for building web applications and APIs. It is designed to make the process of building web applications and APIs simpler and more streamlined by providing a layer of abstraction over the core functionality of Node.js. Express.js allows developers to easily create routes, handle requests and responses, and manage middleware to enhance the functionality of their applications. It is widely used in the industry for building web applications and APIs due to its simplicity, flexibility, and scalability.",
    metadata: {
        sources: [
            "express-2 lecture slides.pdf",
            "express-2 transcript.csv",
        ],
        contributors: "gemma:7b, shrish",
        dateCreated: "2024-01-09 12:49",
        dateEdited: "2024-04-02 16:22",
    }
}

const POSITION_OFFSET = {
    x: 24,
    y: 96
}

const INIT_DRAG_BOUNDS = {
    top: 0,
    left: 0,
    right: window.innerWidth - 420,
    bottom: window.innerHeight,
}

const NodeDetails = () => {
    const { selectedNode, setSelectedNode } = useContext(GraphContext)
    const [dragBounds, setDragBounds] = useState(INIT_DRAG_BOUNDS)
    const modalRef = useRef<HTMLInputElement>(null)

    useEffect(() => {
        if (modalRef.current) {
            setDragBounds({
                ...dragBounds,
                bottom: window.innerHeight - modalRef.current.clientHeight
            })
        }
    }, [selectedNode])

    if (!selectedNode || !selectedNode.sources) return

    const handleCollapse = () => {
        setSelectedNode(undefined)
    }

    const renderSource = (source: str) => {
        const lastIndex = source.lastIndexOf("/")
        return source.substring(lastIndex + 1)
    }

    return (
        <Draggable
            handle='.handle'
            bounds={dragBounds}
            defaultPosition={POSITION_OFFSET}
        >
            <div className="bg-black w-[420px] min-h-96 rounded-[24px] p-2 flex flex-col gap-1" ref={modalRef}>
                <div className="flex justify-between h-10 px-4 items-center handle cursor-move">
                    <div className="flex gap-2">
                        <img src={AddNodeIcon} className="w-3" />
                        <p className="text-sm text-zinc-300">node details</p>
                    </div>
                    <MiniButton title="collapse" onClick={handleCollapse} />
                </div>
                <div className="flex flex-col flex-grow gap-1 bg-background rounded-[24px] p-4">
                    <p className="text-2xl text-accent">{selectedNode.id}</p>
                    <p className="text-zinc-500 pt-2">notes</p>
                    <p className="text-sm text-zinc-300 text-justify">{selectedNode.notes}</p>
                    <p className="text-zinc-500 pt-2">sources</p>
                    <div>
                        {
                            selectedNode.sources.map((source, index) => (
                                <p
                                    className="text-accent underline"
                                    key={`source-${index}`}
                                >
                                    {renderSource(source)}
                                </p>
                            ))
                        }
                    </div>
                    <div className="font-mono text-xs text-zinc-500 pt-4 flex justify-between">
                        <div>
                            <p>contributors</p>
                            <p>date created</p>
                            <p>date edited</p>
                        </div>
                        <div>
                            <p>{SAMPLE_NODE.metadata.contributors}</p>
                            <p>{SAMPLE_NODE.metadata.dateCreated}</p>
                            <p>{SAMPLE_NODE.metadata.dateEdited}</p>
                        </div>
                    </div>
                </div>
            </div>
        </Draggable>
    )
}

export default NodeDetails