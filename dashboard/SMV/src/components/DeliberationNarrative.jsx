const AUDITOR_STYLES = {
  claude: { label: 'Claude — PRO-CT (Teleological)', color: '#646cff', borderColor: 'rgba(100,108,255,0.4)' },
  grok:   { label: 'Grok — ANTI-CT (Empirical)',    color: '#22c55e', borderColor: 'rgba(34,197,94,0.4)' },
  nova:   { label: 'Nova — Fairness Assessment',     color: '#f59e0b', borderColor: 'rgba(245,158,11,0.4)' },
}

const NarrativeBlock = ({ auditor, text }) => {
  const style = AUDITOR_STYLES[auditor]
  if (!text) return null
  return (
    <div style={{
      borderLeft: `3px solid ${style.borderColor}`,
      paddingLeft: '0.85rem',
      marginBottom: '1rem',
    }}>
      <div style={{ fontSize: '0.7rem', fontWeight: 'bold', color: style.color, marginBottom: '0.35rem', letterSpacing: '0.04em', textTransform: 'uppercase' }}>
        {style.label}
      </div>
      <div style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.75)', lineHeight: 1.55, whiteSpace: 'pre-wrap' }}>
        {text}
      </div>
    </div>
  )
}

const DeliberationNarrative = ({ tickData }) => {
  if (!tickData) return null

  const { metric_full, round, claude_narrative, grok_challenge, nova_assessment, crux, convergence } = tickData
  const hasCrux = crux?.status === 'declared'
  const isPotentialCrux = crux?.status === 'potential'
  const hasContent = claude_narrative || grok_challenge || nova_assessment || hasCrux || isPotentialCrux

  if (!hasContent) return null

  return (
    <div style={{
      padding: '1rem',
      backgroundColor: 'rgba(255,255,255,0.03)',
      borderRadius: '8px',
      border: '1px solid rgba(255,255,255,0.08)',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '0.85rem' }}>
        <div style={{ fontSize: '0.8rem', fontWeight: '600', color: 'rgba(255,255,255,0.5)', letterSpacing: '0.05em' }}>
          DELIBERATION · {metric_full} · Round {round}
        </div>
        <div style={{ fontSize: '0.75rem', color: convergence?.percentage >= 98 ? '#22c55e' : convergence?.percentage >= 85 ? '#f59e0b' : '#f87171' }}>
          {convergence?.percentage}% convergence
        </div>
      </div>

      {hasCrux && (
        <div style={{
          marginBottom: '1rem',
          padding: '0.5rem 0.75rem',
          backgroundColor: 'rgba(239,68,68,0.12)',
          border: '1px solid rgba(239,68,68,0.3)',
          borderRadius: '6px',
          fontSize: '0.78rem',
          color: '#fca5a5',
        }}>
          <span style={{ fontWeight: 'bold' }}>⚑ CRUX DECLARED</span>
          {crux.classification && <span style={{ marginLeft: '0.5rem', opacity: 0.8 }}>({crux.classification})</span>}
          {crux.description && <div style={{ marginTop: '0.3rem', opacity: 0.85 }}>{crux.description}</div>}
        </div>
      )}

      {isPotentialCrux && (
        <div style={{
          marginBottom: '1rem',
          padding: '0.5rem 0.75rem',
          backgroundColor: 'rgba(245,158,11,0.10)',
          border: '1px solid rgba(245,158,11,0.3)',
          borderRadius: '6px',
          fontSize: '0.78rem',
          color: '#fcd34d',
        }}>
          <span style={{ fontWeight: 'bold' }}>◈ APPROACHING CRUX</span>
          <span style={{ marginLeft: '0.5rem', opacity: 0.75 }}>
            Convergence below 90% in a late round — deliberation did reach a crux declaration this metric
          </span>
        </div>
      )}

      <NarrativeBlock auditor="claude" text={claude_narrative} />
      <NarrativeBlock auditor="grok"   text={grok_challenge} />
      <NarrativeBlock auditor="nova"   text={nova_assessment} />
    </div>
  )
}

export default DeliberationNarrative
