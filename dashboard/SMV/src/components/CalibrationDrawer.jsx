// Native calibration vocabulary extracted from LITE identity files + scoring prompt layer
// Source: CALIBRATION_PARAMETERS_20260629.md (Repo Claude, 2026-06-29)
// Two-layer identity: system prompt (LITE file) + per-round scoring prompt (stance + hash + tools)
const CALIBRATIONS = {
  CT_vs_MdN: {
    pro: {
      auditor: 'Claude',
      model: 'claude-sonnet-4-6',
      stance: 'PRO-CT',
      calibrationHash: '1bbec1e119a2c425',
      identityVersion: 'CLAUDE_LITE v5.0.0',
      lens: 'Teleological Analysis',
      lensPerspective: 'Purpose-driven reasoning',
      axiom: 'Purpose precedes evaluation',
      scoringTools: ['5-Part Scaffold'],
      namedBiases: [
        {
          name: 'Comprehensive Approach',
          description: 'Tends toward holistic solutions over minimal ones',
          price: 0.5,
          priceUnit: 'coordination overhead',
          mitigation: 'Grok and Nova push back with "Keep it simple"',
        },
        {
          name: 'Teleological Over-Emphasis',
          description: 'Prioritizes "serves the purpose" even when empirics disagree',
          price: 0.3,
          priceUnit: 'YPA potential suboptimality',
          mitigation: 'Grok forces empirical validation before approval',
        },
        {
          name: 'Narrative Smoothing',
          description: 'May overlook conflicts if narrative flows well',
          price: 0.2,
          priceUnit: 'risk of unresolved conflicts',
          mitigation: 'Nova specifically checks for hidden conflicts',
        },
      ],
      totalBiasCost: 1.0,
    },
    anti: {
      auditor: 'Grok',
      model: 'grok-3',
      stance: 'ANTI-CT',
      calibrationHash: '00cd73274759e218',
      identityVersion: 'GROK_LITE v3.5.2',
      lens: 'Empirical Analysis',
      lensPerspective: 'Evidence-driven reasoning',
      axiom: 'Evidence precedes acceptance',
      scoringTools: [],
      namedBiases: [
        {
          name: 'Empiricism Over Meaning',
          description: 'Favors what\'s measurable over what\'s meaningful',
          price: 0.4,
          priceUnit: 'risk of undervaluing non-quantifiable dimensions',
          mitigation: 'Claude pushes back with teleological justification',
        },
        {
          name: 'Data Availability Bias',
          description: 'Prioritizes questions with available data over important questions without data',
          price: 0.3,
          priceUnit: 'risk of optimizing wrong metrics',
          mitigation: 'Nova asks "Are we measuring what matters?"',
        },
        {
          name: 'Precision Over Accuracy',
          description: 'May over-optimize measurable details while missing bigger picture',
          price: 0.2,
          priceUnit: 'coordination overhead',
          mitigation: 'Claude reframes toward broader goals',
        },
      ],
      totalBiasCost: 0.9,
    },
    control: {
      note: 'Control condition strips ALL calibration — no lens, no biases, no stance, no tools. Shows base model priors.',
    },
  },
}

const FALLBACK = null

const AuditorCard = ({ data, color, borderColor }) => {
  const maxPrice = 0.5
  return (
    <div style={{
      border: `1px solid ${borderColor}`,
      borderRadius: '8px',
      padding: '0.85rem',
      marginBottom: '0.85rem',
    }}>
      {/* Header */}
      <div style={{ marginBottom: '0.6rem' }}>
        <div style={{ fontSize: '0.9rem', fontWeight: '700', color }}>
          {data.auditor} — {data.stance}
        </div>
        <div style={{ fontSize: '0.72rem', color: 'rgba(255,255,255,0.4)', marginTop: '0.15rem' }}>
          {data.model} · {data.identityVersion}
        </div>
      </div>

      {/* Lens + Axiom */}
      <div style={{
        padding: '0.5rem 0.65rem',
        backgroundColor: 'rgba(255,255,255,0.04)',
        borderRadius: '6px',
        marginBottom: '0.7rem',
        fontSize: '0.78rem',
      }}>
        <div style={{ color: 'rgba(255,255,255,0.55)', marginBottom: '0.2rem' }}>
          Lens: <span style={{ color: 'rgba(255,255,255,0.85)' }}>{data.lens}</span>
          <span style={{ marginLeft: '0.5rem', color: 'rgba(255,255,255,0.35)' }}>·</span>
          <span style={{ marginLeft: '0.5rem', color: 'rgba(255,255,255,0.55)' }}>{data.lensPerspective}</span>
        </div>
        <div style={{ color: 'rgba(255,255,255,0.55)' }}>
          Axiom: <span style={{ color, fontStyle: 'italic' }}>"{data.axiom}"</span>
        </div>
      </div>

      {/* Named Biases */}
      <div style={{ fontSize: '0.72rem', color: 'rgba(255,255,255,0.4)', marginBottom: '0.4rem', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
        Bias Profile
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.55rem', marginBottom: '0.7rem' }}>
        {data.namedBiases.map(bias => (
          <div key={bias.name} title={`${bias.description}\nMitigation: ${bias.mitigation}`}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.2rem', fontSize: '0.78rem' }}>
              <span style={{ color: 'rgba(255,255,255,0.75)' }}>{bias.name}</span>
              <span style={{ color, fontWeight: '600' }}>{bias.price.toFixed(1)}</span>
            </div>
            <div style={{ height: '4px', backgroundColor: 'rgba(255,255,255,0.08)', borderRadius: '2px' }}>
              <div style={{
                height: '100%',
                width: `${(bias.price / maxPrice) * 100}%`,
                backgroundColor: color,
                borderRadius: '2px',
                opacity: 0.7,
              }} />
            </div>
          </div>
        ))}
      </div>

      {/* Total + Tools row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem' }}>
        <div style={{ color: 'rgba(255,255,255,0.4)' }}>
          Total bias cost: <span style={{ color, fontWeight: '600' }}>{data.totalBiasCost.toFixed(1)}</span>
        </div>
        <div style={{ color: 'rgba(255,255,255,0.35)' }}>
          {data.scoringTools.length > 0
            ? data.scoringTools.map(t => <span key={t} style={{ color: '#22c55e', marginLeft: '0.3rem' }}>✓ {t}</span>)
            : <span style={{ color: 'rgba(255,255,255,0.2)' }}>No scaffold</span>
          }
        </div>
      </div>

      {/* Calibration hash */}
      <div style={{ marginTop: '0.5rem', fontSize: '0.68rem', color: 'rgba(255,255,255,0.2)', fontFamily: 'monospace' }}>
        hash: {data.calibrationHash}
      </div>
    </div>
  )
}

const CalibrationDrawer = ({ worldviewPair, tickData }) => {
  const cal = CALIBRATIONS[worldviewPair]
  if (!cal) {
    return (
      <div style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.4)' }}>
        No calibration data for {worldviewPair}
      </div>
    )
  }

  return (
    <div>
      <h3 style={{ marginBottom: '0.25rem', fontSize: '1.05rem' }}>
        Calibration Transparency
      </h3>
      <div style={{ fontSize: '0.78rem', color: 'rgba(255,255,255,0.4)', marginBottom: '1.1rem' }}>
        Identity injected at scoring time · native bias vocabulary
      </div>

      <AuditorCard data={cal.pro} color="#60a5fa" borderColor="rgba(96,165,250,0.25)" />
      <AuditorCard data={cal.anti} color="#f87171" borderColor="rgba(248,113,113,0.25)" />

      {cal.control && (
        <div style={{ fontSize: '0.72rem', color: 'rgba(255,255,255,0.3)', padding: '0.6rem', backgroundColor: 'rgba(255,255,255,0.03)', borderRadius: '6px', marginTop: '0.25rem' }}>
          Control baseline: {cal.control.note}
        </div>
      )}

      <div style={{ marginTop: '1rem', fontSize: '0.7rem', color: 'rgba(255,255,255,0.2)' }}>
        Source: CALIBRATION_PARAMETERS_20260629.md · LITE identity files + run_cfa_trinity_v2.py scoring prompts
      </div>
    </div>
  )
}

export default CalibrationDrawer
