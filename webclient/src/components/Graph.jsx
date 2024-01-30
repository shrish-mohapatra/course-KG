import React, { useEffect, useRef } from 'react'
import * as d3 from "d3"

function drag(simulation) {
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}

const Graph = ({ KGData }) => {
    const svgRef = useRef()

    useEffect(() => {
        const svg = d3.select(svgRef.current)

        // Clear svg before rendering new graph
        svg.selectAll("*").remove()

        // Specify zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.5, 10])
        // .on("zoom", zoomed);

        // Specify the dimensions of the chart
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Create copies of edges and nodes since force
        // simulation will modify them
        const edges = KGData.edges.map(d => ({ ...d }));
        const nodes = KGData.nodes.map(d => ({ ...d }));
        console.log({ edges, nodes })

        // Create simulation with forces
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(edges).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("x", d3.forceX())
            .force("y", d3.forceY())

        // Create SVG container
        svg
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [-width / 2, -height / 2, width, height])
            .attr("style", "max-width: 100%; height: 100%;")
            .call(zoom)

        // Create a group element to hold the SVG elements
        const g = svg.append("g")

        // Add a rectangle to the SVG as a background
        g.append("rect")
            .attr("width", width)
            .attr("height", height)
            .style("fill", "none")
            .style("pointer-events", "all")

        // Add lines for each edge
        const link = svg.append("g")
            .attr("stroke", "#000")
            .attr("stroke-opacity", 0.6)
            .selectAll()
            .data(edges)
            .join("line")

        const node = svg.append("g")
            .attr("fill", "currentColor")
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
            .selectAll("g")
            .data(nodes)
            .join("g")
            .call(drag(simulation));

        node.append("circle")
            .attr("stroke", "white")
            .attr("stroke-width", 1.5)
            .attr("r", 4);

        node.append("text")
            .attr("x", 8)
            .attr("y", "0.31em")
            .text(d => d.name)
            .clone(true).lower()
            .attr("fill", "none")
            .attr("stroke", "white")
            .attr("stroke-width", 3);

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y)

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        })

    }, [KGData])

    return (
        <svg ref={svgRef} />
    )
}

export default Graph