import { useEffect, useRef } from 'react'
import * as d3 from 'd3'

const TimelineSparkline = ({ ticks, currentIndex, onTickSelect, metricGroups = [] }) => {
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

    // Enrich convergenceData with crux status
    convergenceData.forEach((d, i) => {
      d.cruxStatus = ticks[i]?.crux?.status || 'none'
    })

    // Draw points
    const points = g.selectAll('.point')
      .data(convergenceData)
      .enter()
      .append('g')
      .attr('class', 'point')
      .attr('transform', d => `translate(${xScale(d.index)},${yScale(d.convergence)})`)
      .style('cursor', 'pointer')
      .on('click', (event, d) => onTickSelect(d.index))

    // Base dot
    points.append('circle')
      .attr('r', d => d.index === currentIndex ? 6 : 4)
      .attr('fill', d => {
        if (d.index === currentIndex) return '#f59e0b'
        if (d.cruxStatus === 'declared') return '#ef4444'
        if (d.cruxStatus === 'potential') return '#f59e0b'
        return '#646cff'
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 1)

    // Crux flag above declared ticks
    points.filter(d => d.cruxStatus === 'declared')
      .append('text')
      .attr('y', -7)
      .attr('text-anchor', 'middle')
      .attr('font-size', '9px')
      .attr('fill', '#ef4444')
      .text('⚑')

    // Potential indicator above potential ticks
    points.filter(d => d.cruxStatus === 'potential')
      .append('text')
      .attr('y', -7)
      .attr('text-anchor', 'middle')
      .attr('font-size', '8px')
      .attr('fill', '#f59e0b')
      .text('◈')

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

    // Draw metric boundary separators
    if (metricGroups.length > 1) {
      const separatorsGroup = svg.append('g').attr('class', 'metric-separators')
      metricGroups.forEach((group, i) => {
        if (i === 0) return // no line before first metric
        const x = xScale(group.firstIndex - 0.5)

        // Vertical separator line
        separatorsGroup.append('line')
          .attr('x1', x).attr('y1', 0)
          .attr('x2', x).attr('y2', chartHeight)
          .attr('stroke', 'rgba(255,255,255,0.2)')
          .attr('stroke-width', 1)
          .attr('stroke-dasharray', '3,3')

        // Metric label at top
        separatorsGroup.append('text')
          .attr('x', xScale(group.firstIndex))
          .attr('y', -2)
          .attr('text-anchor', 'middle')
          .attr('fill', 'rgba(255,255,255,0.35)')
          .attr('font-size', '9px')
          .attr('font-weight', '600')
          .text(group.metric)
      })

      // Label the first metric too
      separatorsGroup.append('text')
        .attr('x', xScale(metricGroups[0].firstIndex))
        .attr('y', -2)
        .attr('text-anchor', 'middle')
        .attr('fill', 'rgba(255,255,255,0.35)')
        .attr('font-size', '9px')
        .attr('font-weight', '600')
        .text(metricGroups[0].metric)
    }

  }, [ticks, currentIndex, onTickSelect, metricGroups])

  return (
    <div style={{ marginBottom: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.3rem' }}>
      <svg ref={svgRef}></svg>
      <div style={{ display: 'flex', gap: '1.2rem', fontSize: '0.7rem', color: 'rgba(255,255,255,0.4)' }}>
        <span><span style={{ color: '#646cff' }}>●</span> tick</span>
        <span><span style={{ color: '#f59e0b' }}>●</span> current</span>
        <span><span style={{ color: '#f59e0b' }}>◈</span> approaching crux</span>
        <span><span style={{ color: '#ef4444' }}>⚑</span> crux declared</span>
      </div>
    </div>
  )
}

export default TimelineSparkline
