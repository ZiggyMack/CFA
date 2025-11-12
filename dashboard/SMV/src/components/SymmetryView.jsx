import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'

const SymmetryView = ({ tickData }) => {
  const svgRef = useRef()
  const [tooltip, setTooltip] = useState({ show: false, content: '', x: 0, y: 0 })

  useEffect(() => {
    if (!tickData || !svgRef.current) return

    const width = 600
    const height = 500
    const centerX = width / 2
    const centerY = height / 2
    const radius = 150

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove()

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)

    // Define triangle positions (equilateral triangle)
    const angleOffset = -Math.PI / 2 // Start from top
    const positions = {
      'Nova': {
        x: centerX + radius * Math.cos(angleOffset),
        y: centerY + radius * Math.sin(angleOffset),
        angle: angleOffset
      },
      'Claude': {
        x: centerX + radius * Math.cos(angleOffset + 2 * Math.PI / 3),
        y: centerY + radius * Math.sin(angleOffset + 2 * Math.PI / 3),
        angle: angleOffset + 2 * Math.PI / 3
      },
      'Grok': {
        x: centerX + radius * Math.cos(angleOffset + 4 * Math.PI / 3),
        y: centerY + radius * Math.sin(angleOffset + 4 * Math.PI / 3),
        angle: angleOffset + 4 * Math.PI / 3
      }
    }

    // Create node lookup
    const nodeMap = {}
    tickData.nodes.forEach(node => {
      nodeMap[node.auditor] = node
    })

    // Draw edges first (so they appear behind nodes)
    const edgesGroup = svg.append('g').attr('class', 'edges')

    tickData.edges.forEach(edge => {
      const [auditor1, auditor2] = edge.pair.split('-')
      const pos1 = positions[auditor1]
      const pos2 = positions[auditor2]

      if (!pos1 || !pos2) return

      // Scale line width by volume (0.1 - 1.0 → 1-10px)
      const lineWidth = 1 + edge.volume * 9

      // Color by tension (green → yellow → red)
      const tensionColor = d3.interpolateRdYlGn(1 - edge.tension)

      const line = edgesGroup.append('line')
        .attr('x1', pos1.x)
        .attr('y1', pos1.y)
        .attr('x2', pos2.x)
        .attr('y2', pos2.y)
        .attr('stroke', tensionColor)
        .attr('stroke-width', lineWidth)
        .attr('stroke-opacity', 0.7)
        .style('cursor', 'pointer')

      // Add hover interaction
      line.on('mouseenter', (event) => {
        const rect = svgRef.current.getBoundingClientRect()
        setTooltip({
          show: true,
          content: `${edge.pair}\nTension: ${(edge.tension * 100).toFixed(0)}%\nVolume: ${(edge.volume * 100).toFixed(0)}%\n${edge.notes}`,
          x: event.clientX - rect.left,
          y: event.clientY - rect.top
        })
        line.attr('stroke-opacity', 1.0)
      })

      line.on('mouseleave', () => {
        setTooltip({ show: false, content: '', x: 0, y: 0 })
        line.attr('stroke-opacity', 0.7)
      })
    })

    // Draw nodes with confidence halos
    const nodesGroup = svg.append('g').attr('class', 'nodes')

    Object.entries(positions).forEach(([auditor, pos]) => {
      const nodeData = nodeMap[auditor]
      if (!nodeData) return

      // Draw halo (confidence indicator)
      const haloRadius = 20 + nodeData.confidence * 20 // 20-40px based on confidence
      const haloOpacity = 0.1 + nodeData.confidence * 0.2 // More confident = brighter halo

      nodesGroup.append('circle')
        .attr('cx', pos.x)
        .attr('cy', pos.y)
        .attr('r', haloRadius)
        .attr('fill', getAuditorColor(auditor))
        .attr('opacity', haloOpacity)

      // Draw main node circle
      nodesGroup.append('circle')
        .attr('cx', pos.x)
        .attr('cy', pos.y)
        .attr('r', 12)
        .attr('fill', getAuditorColor(auditor))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)

      // Add label
      nodesGroup.append('text')
        .attr('x', pos.x)
        .attr('y', pos.y - 30)
        .attr('text-anchor', 'middle')
        .attr('fill', '#fff')
        .attr('font-size', '14px')
        .attr('font-weight', 'bold')
        .text(auditor)

      // Add confidence percentage
      nodesGroup.append('text')
        .attr('x', pos.x)
        .attr('y', pos.y + 35)
        .attr('text-anchor', 'middle')
        .attr('fill', 'rgba(255,255,255,0.6)')
        .attr('font-size', '11px')
        .text(`${(nodeData.confidence * 100).toFixed(0)}% confidence`)

      // Add stance indicator
      nodesGroup.append('text')
        .attr('x', pos.x)
        .attr('y', pos.y + 48)
        .attr('text-anchor', 'middle')
        .attr('fill', getStanceColor(nodeData.stance))
        .attr('font-size', '10px')
        .attr('font-weight', 'bold')
        .text(nodeData.stance)
    })

  }, [tickData])

  // Helper functions
  const getAuditorColor = (auditor) => {
    const colors = {
      'Claude': '#646cff',
      'Grok': '#22c55e',
      'Nova': '#f59e0b'
    }
    return colors[auditor] || '#888'
  }

  const getStanceColor = (stance) => {
    const colors = {
      'PRO': '#60a5fa',
      'ANTI': '#f87171',
      'FAIRNESS': '#fbbf24'
    }
    return colors[stance] || '#888'
  }

  return (
    <div style={{ position: 'relative' }}>
      <svg ref={svgRef}></svg>
      {tooltip.show && (
        <div
          className="tooltip"
          style={{
            left: tooltip.x + 20,
            top: tooltip.y - 40
          }}
        >
          {tooltip.content.split('\n').map((line, i) => (
            <div key={i}>{line}</div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SymmetryView
