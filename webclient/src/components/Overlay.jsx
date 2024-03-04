import React, { useContext, useState } from 'react'
import { Input, Button, Drawer } from 'antd'
import { GraphContext } from '../context/GraphContext'

const Overlay = () => {
    const { editMode, setEditMode, addNode, waitForLink } = useContext(GraphContext)

    const [open, setOpen] = useState(false)
    const showDrawer = () => setOpen(true)
    const onClose = () => setOpen(false)

    const [nodeName, setNodeName] = useState()

    const handleAddClick = () => {
        addNode(nodeName)
        setNodeName(null)
    }

    const renderEditControls = () => {
        if (editMode) return (
            <div>
                <div style={{display: "flex"}}>
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
                title="Control Panel"
                onClose={onClose}
                open={open}
                mask={false}
            >
                <p>content</p>
            </Drawer>
        </>
    )
}

export default Overlay