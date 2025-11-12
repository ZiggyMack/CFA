import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

const TimelineSparkline = ({ ticks, currentIndex, onTickSelect }) => {
  const svgRef = useRef()

  useEffect(() => {
    if (!ticks || ticks.length === 0 || !svgRef.current) return

    const width = 600
    const height = 80
    const margin = { top: 10, right: 20, bottom: 20, left: 20 }
    const chartWidth = width - margin.left - margin.right
    const chartHeight = height - margin.top - margin.bottom

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)

    const g = svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)

    // Extract convergence percentages
    const convergenceData = ticks.map((tick, i) => ({
      index: i,
      convergence: tick.convergence.percentage,
      timestamp: tick.timestamp
    }))

    // Scales
    const xScale = d3.scaleLinear()
      .domain([0, ticks.length - 1])
      .range([0, chartWidth])

    const yScale = d3.scaleLinear()
      .domain([0, 100])
      .range([chartHeight, 0])

    // Line generator
    const line = d3.line()
      .x(d => xScale(d.index))
      .y(d => yScale(d.convergence))
      .curve(d3.curveMonotoneX)

    // Draw area under line
    const area = d3.area()
      .x(d => xScale(d.index))
      .y0(chartHeight)
      .y1(d => yScale(d.convergence))
      .curve(d3.curveMonotoneX)

    g.append('path')
      .datum(convergenceData)
      .attr('fill', 'rgba(100, 108, 255, 0.2)')
      .attr('d', area)

    // Draw line
    g.append('path')
      .datum(convergenceData)
      .attr('fill', 'none')
      .attr('stroke', '#646cff')
      .attr('stroke-width', 2)
      .attr('d', line)

    // Draw points
    const points = g.selectAll('.point')
      .data(convergenceData)
      .enter()
      .append('g')
      .attr('class', 'point')
      .attr('transform', d => `translate(${xScale(d.index)},${yScale(d.convergence)})`)
      .style('cursor', 'pointer')
      .on('click', (event, d) => onTickSelect(d.index))

    points.append('circle')
      .attr('r', d => d.index === currentIndex ? 6 : 4)
      .attr('fill', d => d.index === currentIndex ? '#f59e0b' : '#646cff')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1)

    // Add labels for current tick
    if (currentIndex !== null && currentIndex >= 0 && currentIndex < convergenceData.length) {
      const currentData = convergenceData[currentIndex]

      g.append('text')
        .attr('x', xScale(currentData.index))
        .attr('y', yScale(currentData.convergence) - 12)
        .attr('text-anchor', 'middle')
        .attr('fill', '#f59e0b')
        .attr('font-size', '12px')
        .attr('font-weight', 'bold')
        .text(`${currentData.convergence}%`)
    }

    // Add x-axis
    const xAxis = d3.axisBottom(xScale)
      .ticks(ticks.length)
      .tickFormat(i => `T${i + 1}`)

    g.append('g')
      .attr('transform', `translate(0,${chartHeight})`)
      .call(xAxis)
      .selectAll('text')
      .attr('fill', 'rgba(255,255,255,0.6)')
      .attr('font-size', '10px')

    // Add axis line styling
    g.selectAll('.domain, .tick line')
      .attr('stroke', 'rgba(255,255,255,0.2)')

  }, [ticks, currentIndex, onTickSelect])

  return (
    <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'center' }}>
      <svg ref={svgRef}></svg>
    </div>
  )
}

export default TimelineSparkline
