const CLASSIFICATION_COLORS = {
  methodological: '#f59e0b',
  definitional:   '#646cff',
  evidential:     '#22c55e',
  modal:          '#e879f9',
  teleological:   '#fb923c',
}

// Extract the "Deadlock basis:" paragraph from claude_narrative markdown
function extractDeadlock(narrative) {
  if (!narrative) return null
  const m = narrative.match(/\*{0,2}Deadlock basis[:\s]*\*{0,2}\s*(.+?)(?:\n\n|\n(?=\*\*)|$)/is)
  if (m) return m[1].replace(/\n/g, ' ').trim().slice(0, 200)
  return null
}

const CruxSummary = ({ cruxTicks, currentIndex, onTickSelect }) => {
  if (!cruxTicks || cruxTicks.length === 0) return null

  const declared  = cruxTicks.filter(({ tick }) => tick.crux?.status === 'declared')
  const potential = cruxTicks.filter(({ tick }) => tick.crux?.status === 'potential')

  if (declared.length === 0 && potential.length === 0) return null

  return (
    <div style={{
      margin: '0.75rem 0',
      padding: '0.85rem 1rem',
      background: 'rgba(239,68,68,0.06)',
      border: '1px solid rgba(239,68,68,0.2)',
      borderRadius: '10px',
      fontSize: '0.82rem',
    }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.65rem' }}>
        <span style={{ fontWeight: 700, color: '#fca5a5', fontSize: '0.85rem' }}>
          ⚑ Crux Analysis
        </span>
        <span style={{ color: 'rgba(255,255,255,0.35)', fontSize: '0.75rem' }}>
          {declared.length} declared
          {potential.length > 0 && ` · ${potential.length} potential`}
        </span>
        <span style={{ marginLeft: 'auto', fontSize: '0.72rem', color: 'rgba(255,255,255,0.25)', fontStyle: 'italic' }}>
          click row to jump
        </span>
      </div>

      {/* Declared cruxes */}
      {declared.map(({ tick, index }) => {
        const deadlock  = extractDeadlock(tick.claude_narrative)
        const classKey  = tick.crux.classification?.toLowerCase() ?? ''
        const classClr  = CLASSIFICATION_COLORS[classKey] ?? 'rgba(255,255,255,0.4)'
        const isActive  = index === currentIndex

        return (
          <div
            key={index}
            onClick={() => onTickSelect(index)}
            style={{
              cursor: 'pointer',
              padding: '0.45rem 0.7rem',
              marginBottom: '0.3rem',
              background: isActive ? 'rgba(239,68,68,0.16)' : 'rgba(239,68,68,0.05)',
              border: `1px solid ${isActive ? 'rgba(239,68,68,0.45)' : 'rgba(239,68,68,0.15)'}`,
              borderRadius: '6px',
              display: 'flex',
              gap: '0.65rem',
              alignItems: 'flex-start',
              transition: 'background 0.15s',
            }}
          >
            {/* Metric badge */}
            <span style={{
              color: '#fca5a5',
              fontWeight: 700,
              minWidth: '2.4rem',
              fontSize: '0.78rem',
              paddingTop: '0.1rem',
            }}>
              {tick.metric}
            </span>

            {/* Round */}
            <span style={{
              fontSize: '0.68rem',
              color: 'rgba(255,255,255,0.3)',
              paddingTop: '0.15rem',
              whiteSpace: 'nowrap',
            }}>
              R{tick.round}
            </span>

            {/* Classification badge */}
            {classKey && (
              <span style={{
                fontSize: '0.65rem',
                fontWeight: 700,
                color: classClr,
                background: `${classClr}20`,
                border: `1px solid ${classClr}40`,
                padding: '0.08rem 0.45rem',
                borderRadius: '4px',
                whiteSpace: 'nowrap',
                alignSelf: 'center',
              }}>
                {classKey}
              </span>
            )}

            {/* Deadlock reason */}
            <span style={{
              flex: 1,
              fontSize: '0.77rem',
              color: 'rgba(255,255,255,0.52)',
              lineHeight: 1.45,
            }}>
              {deadlock ?? tick.crux.description ?? 'Irreconcilable disagreement — see deliberation.'}
            </span>
          </div>
        )
      })}

      {/* Potential cruxes (smaller, dimmer) */}
      {potential.length > 0 && (
        <div style={{ marginTop: '0.5rem', paddingTop: '0.5rem', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
          <div style={{ fontSize: '0.68rem', color: 'rgba(255,255,255,0.25)', marginBottom: '0.3rem', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            Near-crux (not declared)
          </div>
          {potential.map(({ tick, index }) => {
            const isActive = index === currentIndex
            return (
              <div
                key={index}
                onClick={() => onTickSelect(index)}
                style={{
                  cursor: 'pointer',
                  padding: '0.35rem 0.7rem',
                  marginBottom: '0.25rem',
                  background: isActive ? 'rgba(245,158,11,0.12)' : 'transparent',
                  border: `1px solid ${isActive ? 'rgba(245,158,11,0.3)' : 'rgba(245,158,11,0.12)'}`,
                  borderRadius: '6px',
                  display: 'flex',
                  gap: '0.65rem',
                  alignItems: 'center',
                }}
              >
                <span style={{ color: '#fcd34d', fontWeight: 700, minWidth: '2.4rem', fontSize: '0.76rem' }}>
                  {tick.metric}
                </span>
                <span style={{ fontSize: '0.68rem', color: 'rgba(255,255,255,0.28)' }}>R{tick.round}</span>
                <span style={{ fontSize: '0.74rem', color: 'rgba(255,255,255,0.35)' }}>
                  Below convergence threshold — deliberation ultimately resolved
                </span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default CruxSummary
