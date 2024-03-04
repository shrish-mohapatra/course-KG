import React, { useEffect, useRef } from 'react'
import * as d3 from 'd3'

// import data from './data.json'

// const data = {
//     nodes: [
//         {
//             id: 1,
//             label: "intro to JS",
//             groups: ["COMP 2406"]
//         },
//         {
//             id: 2,
//             label: "DOM",
//             groups: ["COMP 2406", "frontend"]
//         },
//         {
//             id: 3,
//             label: "AJAX",
//             groups: ["COMP 2406", "frontend"]
//         },
//         {
//             id: 4,
//             label: "intro to Node.js",
//             groups: ["COMP 2406", "backend"]
//         },
//         {
//             id: 5,
//             label: "NPM",
//             groups: ["COMP 2406", "backend"]
//         },
//         {
//             id: 6,
//             label: "GraphQL",
//             groups: ["COMP 2406", "backend"]
//         },
//     ],
//     edges: [
//         { source: 1, target: 2 },
//         { source: 2, target: 3 },
//         { source: 1, target: 4 },
//         { source: 4, target: 5 },
//         { source: 4, target: 6 },
//     ]
// }

const data = {
    name: "comp 2406",
    children: [
        {
            id: 2,
            name: "intro to js",
            children: [],
            value: 10,
        },
        {
            id: 3,
            name: "frontend",
            children: [
                {
                    id: 5,
                    name: "DOM",
                    children: [],
                    value: 10,
                },
                {
                    id: 7,
                    name: "AJAX",
                    children: [],
                    value: 10,
                }
            ]
        },
        {
            id: 4,
            name: "backend",
            children: [
                {
                    id: 6,
                    name: "intro to node",
                    children: [],
                    value: 10,
                },
                {
                    id: 8,
                    name: "NPM",
                    children: [],
                    value: 10,
                }
            ]
        }
    ]
}

const PackCircles = () => {
    const svgRef = useRef()

    useEffect(() => {
        console.log(data)
        let svg = d3.select(svgRef.current)

        // Clear svg before rendering new graph
        svg.selectAll("*").remove()

        // Specify the dimensions of the chart
        const width = window.innerWidth;
        const height = window.innerHeight;

        // Create the color scale.
        const color = d3.scaleLinear()
            .domain([0, 5])
            .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
            .interpolate(d3.interpolateHcl);

        // Compute the layout.
        const pack = data => d3.pack()
            .size([width, height])
            .padding(3)
            (d3.hierarchy(data)
                .sum(d => d.value)
                .sort((a, b) => b.value - a.value)
            );
        const root = pack(data);

        // Create the SVG container.
        svg
            .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
            .attr("width", width)
            .attr("height", height)
            .attr("style", `max-width: 100%; height: auto; display: block; margin: 0 -14px; background: ${color(0)}; cursor: pointer;`);

        // Append the nodes.
        const node = svg.append("g")
            .selectAll("circle")
            .data(root.descendants().slice(1))
            .join("circle")
            .attr("fill", d => d.children ? color(d.depth) : "white")
            .attr("pointer-events", d => !d.children ? "none" : null)
            .on("mouseover", function () { d3.select(this).attr("stroke", "#000"); })
            .on("mouseout", function () { d3.select(this).attr("stroke", null); })
            .on("click", (event, d) => focus !== d && (zoom(event, d), event.stopPropagation()));

        // Append the text labels.
        const label = svg.append("g")
            .style("font", "10px sans-serif")
            .attr("pointer-events", "none")
            .attr("text-anchor", "middle")
            .selectAll("text")
            .data(root.descendants())
            .join("text")
            .style("fill-opacity", d => d.parent === root ? 1 : 0)
            .style("display", d => d.parent === root ? "inline" : "none")
            .text(d => d.data.name);

        // Create the zoom behavior and zoom immediately in to the initial focus node.
        svg.on("click", (event) => zoom(event, root));
        let focus = root;
        let view;
        zoomTo([focus.x, focus.y, focus.r * 2]);

        function zoomTo(v) {
            const k = width / v[2];

            view = v;

            label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
            node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
            node.attr("r", d => d.r * k);
        }

        function zoom(event, d) {
            const focus0 = focus;

            focus = d;

            const transition = svg.transition()
                .duration(event.altKey ? 7500 : 750)
                .tween("zoom", d => {
                    const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
                    return t => zoomTo(i(t));
                });

            label
                .filter(function (d) { return d.parent === focus || this.style.display === "inline"; })
                .transition(transition)
                .style("fill-opacity", d => d.parent === focus ? 1 : 0)
                .on("start", function (d) { if (d.parent === focus) this.style.display = "inline"; })
                .on("end", function (d) { if (d.parent !== focus) this.style.display = "none"; });
        }

    }, [])

    return (
        <svg ref={svgRef} />
    )
}

export default PackCircles