const BATCH_CONTEXT = {
  CT_vs_MdN: {
    label: 'CT vs MdN — Forward Stance',
    badge: '📕 Claude PRO-CT · Grok ANTI-CT',
    date: '2026-06-29',
    runs: '10 golden + 10 control',
    convergence: '85.8% avg (golden)',
    instrument: 'CFA-EXP1-BATCH-20260629',
    headline: 'Claude advocates for Classical Theism; Grok applies empirical scrutiny as adversary.',
    keyFindings: [
      'CT scores highest on MS (Moral Substance) and AR (Aesthetic Resonance) across all metrics.',
      'Largest divergence on BFI — teleological vs empirical grounding creates definitional impasse.',
      'Golden vs control delta confirms identity-loaded priming lifts PRO scores ~0.5–1.2 pts.',
      'Crux declarations concentrated in BFI and ES — deepest philosophical fault lines.',
    ],
    stance: { claude: 'PRO-CT', grok: 'ANTI-CT' },
  },
  MdN_vs_CT: {
    label: 'MdN vs CT — Reverse Stance',
    badge: '📘 Grok PRO-MdN · Claude ANTI-MdN',
    date: '2026-06-30',
    runs: '10 golden',
    convergence: '86.2% avg (golden)',
    instrument: 'CFA-EXP1-BATCH-20260630',
    headline: 'Grok advocates for Methodological Naturalism; Claude applies teleological scrutiny as adversary.',
    keyFindings: [
      'MS (Moral Substance) is the weakest metric for BOTH auditors — not a role artifact, a genuine gap.',
      'Grok role-swap gain strongest on CA (+2.3) — empirical lens aligns naturally with MdN methodology.',
      'Claude drops 1.3–3.4 pts switching PRO-CT → ANTI-MdN, showing teleological lens creates asymmetric pressure.',
      'Instrument stability confirmed: 86.2% convergence matches CT batch (85.8%) — same deliberation depth regardless of subject.',
    ],
    stance: { claude: 'ANTI-MdN', grok: 'PRO-MdN' },
  },
}

const ExperimentBrief = ({ open, sessionData }) => {
  if (!open || !sessionData) return null

  const worldviewPair = sessionData.worldview_pair ?? 'CT_vs_MdN'
  const story = sessionData.session_story
  const batch = BATCH_CONTEXT[worldviewPair] ?? BATCH_CONTEXT.CT_vs_MdN
  const isGolden = sessionData.identity_condition === 'external_identity'

  return (
    <div style={{
      margin: '0.75rem 0',
      padding: '1rem 1.25rem',
      background: 'linear-gradient(135deg, rgba(100,108,255,0.08) 0%, rgba(34,197,94,0.05) 100%)',
      border: '1px solid rgba(100,108,255,0.25)',
      borderRadius: '10px',
      fontSize: '0.83rem',
    }}>
      {/* Header row */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', flexWrap: 'wrap', marginBottom: '0.75rem' }}>
        <div style={{ flex: 1, minWidth: '200px' }}>
          <div style={{ fontWeight: 700, color: '#fff', fontSize: '0.9rem', marginBottom: '0.15rem' }}>
            {batch.label}
          </div>
          <div style={{ color: 'rgba(255,255,255,0.45)', fontSize: '0.75rem' }}>
            {batch.badge} · {batch.date} · {batch.runs}
          </div>
        </div>

        {/* Session stats */}
        <div style={{ display: 'flex', gap: '1.25rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <Stat label="Session" value={sessionData.session_id} />
          <Stat label="Condition" value={isGolden ? '🟢 Golden' : '⚪ Control'} />
          {story && <>
            <Stat label="Convergence" value={`${story.avg_convergence_pct}%`} />
            <Stat label="Avg Rounds" value={story.avg_rounds} />
            {story.crux_metrics?.length > 0 && (
              <Stat label="Crux Metrics" value={story.crux_metrics.join(', ')} accent="#f59e0b" />
            )}
          </>}
        </div>
      </div>

      <div style={{ borderTop: '1px solid rgba(255,255,255,0.07)', paddingTop: '0.75rem', display: 'flex', gap: '1.25rem', flexWrap: 'wrap' }}>
        {/* Batch context */}
        <div style={{ flex: 2, minWidth: '240px' }}>
          <div style={{ color: 'rgba(255,255,255,0.7)', marginBottom: '0.4rem', lineHeight: 1.5 }}>
            {batch.headline}
          </div>
          <ul style={{ margin: 0, paddingLeft: '1.1rem', color: 'rgba(255,255,255,0.45)', lineHeight: 1.6 }}>
            {batch.keyFindings.map((f, i) => <li key={i}>{f}</li>)}
          </ul>
        </div>

        {/* Session summary */}
        {story?.summary && (
          <div style={{ flex: 1, minWidth: '180px', borderLeft: '1px solid rgba(255,255,255,0.08)', paddingLeft: '1rem' }}>
            <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'rgba(255,255,255,0.3)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '0.3rem' }}>
              Session Story
            </div>
            <div style={{ color: 'rgba(255,255,255,0.55)', lineHeight: 1.55 }}>
              {story.summary}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

const Stat = ({ label, value, accent }) => (
  <div style={{ textAlign: 'center' }}>
    <div style={{ fontSize: '0.68rem', color: 'rgba(255,255,255,0.3)', textTransform: 'uppercase', letterSpacing: '0.07em' }}>{label}</div>
    <div style={{ fontWeight: 700, color: accent ?? 'rgba(255,255,255,0.85)', fontSize: '0.82rem' }}>{value}</div>
  </div>
)

export default ExperimentBrief
