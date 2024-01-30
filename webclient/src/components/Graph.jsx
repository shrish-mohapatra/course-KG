import React, { useEffect, useRef } from 'react'
import * as d3 from "d3"

function linkArc(d) {
    const r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y);
    return `
      M${d.source.x},${d.source.y}
      A${r},${r} 0 0,1 ${d.target.x},${d.target.y}
    `;
}

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
        const labels = KGData.labels.map(d => ({ ...d }));
        console.log({ edges, nodes, labels })

        const color = d3.scaleOrdinal(labels, d3.schemeCategory10);

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(edges).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("x", d3.forceX())
            .force("y", d3.forceY());

        svg
            .attr("viewBox", [-width / 2, -height / 2, width, height])
            .attr("width", width)
            .attr("height", height)
            .attr("style", "max-width: 100%; height: auto; font: 12px sans-serif;");

        // Per-type markers, as they don't inherit styles.
        svg.append("defs").selectAll("marker")
            .data(labels)
            .join("marker")
            .attr("id", d => `arrow-${d.id}`)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -0.5)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("fill", d => color(d.id))
            .attr("d", "M0,-5L10,0L0,5");

        const link = svg.append("g")
            .attr("fill", "none")
            .attr("stroke-width", 1.5)
            .selectAll("path")
            .data(edges)
            .join("path")
            .attr("stroke", d => color(d.label))
            .attr("marker-end", d => `url(${new URL(`#arrow-${d.label}`, location)})`)
            .attr("id", (d, i) => `edgepath${i}`)

        const linkText = svg.append("g")
            .selectAll()
            .data(edges)
            .join("text")
            .attr("dy", -3)
            .attr("text-anchor", "middle")
            .append("textPath") // append a textPath to the text element
            .attr("startOffset", "50%") // place the text in the middle of the path
            .attr("xlink:href", (d, i) => `#edgepath${i}`) // reference the id of the path
            .text(d => labels[d.label - 1].name)
            .attr("fill", d => color(d.label))
            .attr("font-size", "10px")

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
            link.attr("d", linkArc)

            // linkText
            //     .attr("x", d => (d.source.x + d.target.x) / 2)
            //     .attr("y", d => (d.source.y + d.target.y) / 2)

            node.attr("transform", d => `translate(${d.x},${d.y})`);
        })

    }, [KGData])

    return (
        <svg ref={svgRef} />
    )
}

export default Graph