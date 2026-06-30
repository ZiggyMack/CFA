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

    // Define triangle positions — Claude/Grok fixed, Nova drifts toward lower scorer
    const angleOffset = -Math.PI / 2 // Start from top

    // Claude is bottom-right (angle=30°), Grok is bottom-left (angle=150°)
    // Nova drifts toward the auditor with the LOWER score (needs fairness support)
    const claudeNode = tickData.nodes.find(n => n.auditor === 'Claude')
    const grokNode   = tickData.nodes.find(n => n.auditor === 'Grok')
    const claudeScore = claudeNode?.score ?? 5
    const grokScore   = grokNode?.score   ?? 5
    // scoreGap > 0 → Claude leading → Nova leans LEFT toward Grok; < 0 → lean RIGHT toward Claude
    const scoreGap = claudeScore - grokScore
    const leanNorm = Math.max(-1, Math.min(1, scoreGap / 8)) // cap at ±8pt gap
    const novaBaseX = centerX + radius * Math.cos(angleOffset)
    const novaBaseY = centerY + radius * Math.sin(angleOffset)
    const novaDriftX = -leanNorm * 90   // negative = left (toward Grok)
    const novaDriftY =  Math.abs(leanNorm) * 28  // drop as triangle skews

    const positions = {
      'Nova': {
        x: novaBaseX + novaDriftX,
        y: novaBaseY + novaDriftY,
        angle: angleOffset,
        lean: leanNorm,
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

      // Draw halo — use bias_overhead as proxy (0.3–0.5 range)
      const biasWeight = nodeData.bias_overhead ?? 0.3
      const haloRadius = 20 + biasWeight * 20
      const haloOpacity = 0.08 + biasWeight * 0.18

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

      // Score label (Claude/Grok show score; Nova shows lean direction)
      if (nodeData.score !== null && nodeData.score !== undefined) {
        nodesGroup.append('text')
          .attr('x', pos.x)
          .attr('y', pos.y + 35)
          .attr('text-anchor', 'middle')
          .attr('fill', 'rgba(255,255,255,0.65)')
          .attr('font-size', '12px')
          .attr('font-weight', '600')
          .text(nodeData.score.toFixed(1))
      } else if (auditor === 'Nova' && Math.abs(pos.lean ?? 0) > 0.12) {
        // Nova lean direction label — only when meaningfully off-center
        const leanAmt = pos.lean ?? 0
        const leanTarget = leanAmt > 0 ? '→ Grok' : 'Claude ←'
        const leanPct = Math.round(Math.abs(leanAmt) * 100)
        nodesGroup.append('text')
          .attr('x', pos.x)
          .attr('y', pos.y + 35)
          .attr('text-anchor', 'middle')
          .attr('fill', '#f59e0b')
          .attr('font-size', '10px')
          .attr('font-weight', '600')
          .text(`⚖ ${leanTarget} ${leanPct}%`)
      }

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

      {/* Edge legend */}
      <div style={{
        display: 'flex',
        gap: '1.5rem',
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: '-0.5rem',
        marginBottom: '0.5rem',
        fontSize: '0.72rem',
        color: 'rgba(255,255,255,0.45)',
      }}>
        {/* Color legend */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span>Edge color — disagreement:</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
            <span style={{ display: 'inline-block', width: '28px', height: '3px', background: 'linear-gradient(to right, #1a9850, #ffffbf, #d73027)', borderRadius: '2px' }} />
          </span>
          <span style={{ color: '#1a9850' }}>converging</span>
          <span>→</span>
          <span style={{ color: '#d73027' }}>diverging</span>
        </div>

        <span style={{ color: 'rgba(255,255,255,0.15)' }}>|</span>

        {/* Thickness legend */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span>Thickness — deliberation intensity:</span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
            <span style={{ display: 'inline-block', width: '18px', height: '2px', backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: '1px' }} />
            <span style={{ display: 'inline-block', width: '18px', height: '5px', backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: '1px' }} />
            <span style={{ display: 'inline-block', width: '18px', height: '9px', backgroundColor: 'rgba(255,255,255,0.5)', borderRadius: '1px' }} />
          </span>
          <span>thin = early · thick = active</span>
        </div>

        <span style={{ color: 'rgba(255,255,255,0.15)' }}>|</span>

        {/* Nova lean legend */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <span style={{ color: '#f59e0b' }}>⚖</span>
          <span>Nova vertex drifts toward lower scorer — fairness load</span>
        </div>
      </div>
    </div>
  )
}

export default SymmetryView
