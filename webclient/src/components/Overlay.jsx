import React, { useContext, useState } from 'react'
import { Input, Button, Drawer, Form } from 'antd'
import { GraphContext } from '../context/GraphContext'

const Overlay = () => {
    const {
        graphData,
        editMode,
        setEditMode,
        addNode,
        waitForLink,
        selectedNode,
        setSelectedNode,
    } = useContext(GraphContext)

    const onClose = () => setSelectedNode(null)

    const [nodeName, setNodeName] = useState()

    const handleAddClick = () => {
        addNode(nodeName)
        setNodeName(null)
    }

    const renderEditControls = () => {
        if (editMode) return (
            <div>
                <div style={{ display: "flex" }}>
                    <Input
                        size='small'
                        placeholder='Node name'
                        value={nodeName}
                        onChange={(e) => setNodeName(e.target.value)}
                    />
                    <Button size="small" onClick={handleAddClick}>
                        + node
                    </Button>
                </div>
                <Button size="small" onClick={waitForLink}>
                    + link
                </Button>
            </div>
        )
    }

    const handleExport = () => {
        const simplifiedData = {...graphData}
        simplifiedData.nodes = simplifiedData.nodes.map(node => ({
            id: node.id,
            group: node.group,
            value: node.value
        }))
        simplifiedData.links = simplifiedData.links.map(link => ({
            source: link.source.id,
            target: link.target.id,
        }))
        const textToCopy = JSON.stringify(simplifiedData)
        navigator.clipboard.writeText(textToCopy)
    }

    return (
        <>
            <div style={{
                position: "absolute",
                left: 10,
                top: 10,
                zIndex: 10
            }}>
                <p>course-KG</p>
            </div>
            <div style={{
                position: "absolute",
                left: 10,
                bottom: 10,
                zIndex: 10
            }}>
                <Button onClick={handleExport}>export</Button>
            </div>
            <div style={{
                position: "absolute",
                right: 10,
                top: 10,
                zIndex: 10,
                textAlign: 'right'
            }}>
                <Button onClick={() => setEditMode(toggle => !toggle)}>
                    {editMode ? "editing" : "viewing"}
                </Button>
                {renderEditControls()}
            </div>

            <Drawer
                title="Node details"
                onClose={onClose}
                open={selectedNode != null}
                mask={false}
            >
                {
                    selectedNode &&
                    <>
                        <Form layout="vertical">
                            <Form.Item label="Name">
                                <Input value={selectedNode.id} />
                            </Form.Item>
                            <Form.Item label="Notes">
                                <Input.TextArea placeholder='Details about the concept' />
                            </Form.Item>
                        </Form>
                    </>
                }
            </Drawer>
        </>
    )
}

export default Overlay