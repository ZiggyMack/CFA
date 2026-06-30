import { useState, useEffect, useMemo } from 'react'
import SymmetryView from './components/SymmetryView'
import TimelineSparkline from './components/TimelineSparkline'
import CalibrationDrawer from './components/CalibrationDrawer'
import EthicsBadges from './components/EthicsBadges'
import CruxToggle from './components/CruxToggle'
import DeliberationNarrative from './components/DeliberationNarrative'
import ExperimentBrief from './components/ExperimentBrief'
import CruxSummary from './components/CruxSummary'
import scenario1 from './data/scenario_1_tension_escalation.json'
import scenario2 from './data/scenario_2_high_alignment.json'
import scenario3 from './data/scenario_3_resolution.json'

// Lazy-load real run scenarios — Vite bundles these as separate chunks
const realScenarios = import.meta.glob('./data/scenario_{CT_MdN,MdN_CT}_*.json')

const GOLDEN_SESSIONS = [
  '132540', '135207', '141547', '143943', '150746',
  '153034', '155831', '162330', '164552', '170941',
]
const CONTROL_SESSIONS = [
  '201637', '202404', '203230', '203925', '204727',
  '205545', '210256', '211053', '211906', '212612',
]
const MDN_GOLDEN_SESSIONS = [
  '010555', '013915', '020430', '023628', '030546',
  '033444', '040536', '043509', '050406', '053600',
]

const STATIC_SCENARIOS = {
  'demo-1': { name: '[Demo] Tension Escalation (CT vs MdN)',   data: scenario1 },
  'demo-2': { name: '[Demo] High Alignment (CT vs Proc. Th.)', data: scenario2 },
  'demo-3': { name: '[Demo] Resolution (CT vs Naturalism)',    data: scenario3 },
}

function sessionLabel(id, condition) {
  return `${condition} · ${id}`
}

function App() {
  const [selectedKey, setSelectedKey] = useState('demo-1')
  const [currentData, setCurrentData] = useState(scenario1)
  const [loading, setLoading] = useState(false)
  const [currentTickIndex, setCurrentTickIndex] = useState(0)
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [narrativeOpen, setNarrativeOpen] = useState(true)
  const [cruxMode, setCruxMode] = useState(false)
  const [briefOpen, setBriefOpen] = useState(false)

  // Crux tick index — ticks where crux status is declared or potential
  const cruxTicks = currentData
    ? currentData.ticks
        .map((t, i) => ({ tick: t, index: i }))
        .filter(({ tick }) => tick.crux?.status === 'declared' || tick.crux?.status === 'potential')
    : []

  // Metric groups — one entry per metric in order, with firstIndex/lastIndex
  const metricGroups = useMemo(() => {
    if (!currentData) return []
    const groups = []
    let curMetric = null
    let startIdx = 0
    currentData.ticks.forEach((tick, i) => {
      if (tick.metric !== curMetric) {
        if (curMetric !== null) groups.push({ metric: curMetric, metricFull: currentData.ticks[startIdx].metric_full, firstIndex: startIdx, lastIndex: i - 1 })
        curMetric = tick.metric
        startIdx = i
      }
    })
    if (curMetric !== null) groups.push({ metric: curMetric, metricFull: currentData.ticks[startIdx].metric_full, firstIndex: startIdx, lastIndex: currentData.ticks.length - 1 })
    return groups
  }, [currentData])

  const currentGroupIndex = metricGroups.findIndex(g => g.firstIndex <= currentTickIndex && currentTickIndex <= g.lastIndex)
  const currentGroup = metricGroups[currentGroupIndex] ?? null

  useEffect(() => {
    setCurrentTickIndex(0)
    setCruxMode(false)
    setBriefOpen(false)

    if (STATIC_SCENARIOS[selectedKey]) {
      setCurrentData(STATIC_SCENARIOS[selectedKey].data)
      return
    }

    // Load real run scenario dynamically — detect prefix from session list
    const prefix = MDN_GOLDEN_SESSIONS.includes(selectedKey) ? 'MdN_CT' : 'CT_MdN'
    const path = `./data/scenario_${prefix}_${selectedKey}.json`
    const loader = realScenarios[path]
    if (!loader) {
      console.warn('No scenario found for key:', selectedKey)
      return
    }

    setLoading(true)
    loader()
      .then(mod => {
        setCurrentData(mod.default)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load scenario:', err)
        setLoading(false)
      })
  }, [selectedKey])

  if (!currentData || loading) {
    return (
      <div className="container">
        <div className="header">
          <h1>SMV</h1>
          <p>Loading scenario…</p>
        </div>
      </div>
    )
  }

  const currentTick = currentData.ticks[currentTickIndex]

  const handlePrevTick = () => {
    if (cruxMode && cruxTicks.length > 0) {
      const prev = [...cruxTicks].reverse().find(({ index }) => index < currentTickIndex)
      if (prev) setCurrentTickIndex(prev.index)
    } else {
      setCurrentTickIndex(prev => Math.max(0, prev - 1))
    }
  }

  const handleNextTick = () => {
    if (cruxMode && cruxTicks.length > 0) {
      const next = cruxTicks.find(({ index }) => index > currentTickIndex)
      if (next) setCurrentTickIndex(next.index)
    } else {
      setCurrentTickIndex(prev => Math.min(currentData.ticks.length - 1, prev + 1))
    }
  }

  const handleTickSelect = (index) => setCurrentTickIndex(index)

  const handlePrevMetric = () => {
    const prev = metricGroups[currentGroupIndex - 1]
    if (prev) setCurrentTickIndex(prev.firstIndex)
  }

  const handleNextMetric = () => {
    const next = metricGroups[currentGroupIndex + 1]
    if (next) setCurrentTickIndex(next.firstIndex)
  }

  const storyLabel = currentData.session_story
    ? `${currentData.identity_condition === 'external_identity' ? 'Golden' : 'Control'} — ${currentData.session_story.avg_convergence_pct}% conv, ${currentData.session_story.avg_rounds}r avg`
    : null

  return (
    <div className="container">
      <div className="header">
        <h1>SMV</h1>
        <p>Symmetry Matrix Visualizer · CFA Trinity</p>
      </div>

      <div className="controls">
        <label>
          Run:
          <select value={selectedKey} onChange={(e) => setSelectedKey(e.target.value)}>
            <optgroup label="CT vs MdN — Golden (Claude PRO-CT)">
              {GOLDEN_SESSIONS.map(id => (
                <option key={id} value={id}>{sessionLabel(id, 'Golden')}</option>
              ))}
            </optgroup>
            <optgroup label="CT vs MdN — Control (No Identity)">
              {CONTROL_SESSIONS.map(id => (
                <option key={id} value={id}>{sessionLabel(id, 'Control')}</option>
              ))}
            </optgroup>
            <optgroup label="MdN vs CT — Golden (Grok PRO-MdN)">
              {MDN_GOLDEN_SESSIONS.map(id => (
                <option key={id} value={id}>{sessionLabel(id, 'MdN Golden')}</option>
              ))}
            </optgroup>
            <optgroup label="Demo Scenarios">
              {Object.entries(STATIC_SCENARIOS).map(([key, { name }]) => (
                <option key={key} value={key}>{name}</option>
              ))}
            </optgroup>
          </select>
        </label>

        {storyLabel && (
          <span style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.5)', marginLeft: '0.5rem' }}>
            {storyLabel}
          </span>
        )}

        <button
          onClick={handlePrevMetric}
          disabled={currentGroupIndex <= 0}
          title="Jump to previous metric"
          style={{ opacity: currentGroupIndex <= 0 ? 0.3 : 1 }}
        >
          ⏮
        </button>

        <button onClick={handlePrevTick} disabled={currentTickIndex === 0}>← Prev</button>

        <span style={{ fontSize: '0.82rem', color: 'rgba(255,255,255,0.6)', minWidth: '140px', textAlign: 'center' }}>
          <span style={{ color: 'rgba(255,255,255,0.9)', fontWeight: 600 }}>{currentTick?.metric}</span>
          {' '}R{currentTick?.round}
          <span style={{ color: 'rgba(255,255,255,0.35)', marginLeft: '0.4rem' }}>
            · {currentTickIndex + 1}/{currentData.ticks.length}
          </span>
        </span>

        <button onClick={handleNextTick} disabled={currentTickIndex === currentData.ticks.length - 1}>Next →</button>

        <button
          onClick={handleNextMetric}
          disabled={currentGroupIndex >= metricGroups.length - 1}
          title="Jump to next metric"
          style={{ opacity: currentGroupIndex >= metricGroups.length - 1 ? 0.3 : 1 }}
        >
          ⏭
        </button>

        <button onClick={() => setDrawerOpen(!drawerOpen)}>
          {drawerOpen ? 'Hide' : 'Show'} Calibration
        </button>

        <button onClick={() => setNarrativeOpen(!narrativeOpen)}>
          {narrativeOpen ? 'Hide' : 'Show'} Narrative
        </button>

        <button
          onClick={() => setBriefOpen(!briefOpen)}
          style={{ background: briefOpen ? 'rgba(100,108,255,0.25)' : undefined }}
          title="Toggle Experiment Brief"
        >
          📖 Brief
        </button>

        <CruxToggle
          active={cruxMode}
          onToggle={() => {
            const entering = !cruxMode
            setCruxMode(entering)
            if (entering && cruxTicks.length > 0) {
              // Jump to first crux tick on activation
              const first = cruxTicks.find(({ index }) => index >= currentTickIndex) || cruxTicks[0]
              setCurrentTickIndex(first.index)
            }
          }}
          cruxCount={cruxTicks.length}
        />
      </div>

      <ExperimentBrief open={briefOpen} sessionData={currentData} />

      {cruxMode && (
        <CruxSummary
          cruxTicks={cruxTicks}
          currentIndex={currentTickIndex}
          onTickSelect={handleTickSelect}
        />
      )}

      <TimelineSparkline
        ticks={currentData.ticks}
        currentIndex={currentTickIndex}
        onTickSelect={handleTickSelect}
        metricGroups={metricGroups}
      />

      <div className="visualization-container">
        <div className="main-view">

          {/* Metric banner — always visible, shows which group you're in */}
          {currentGroup && (
            <div style={{
              marginBottom: '1rem',
              padding: '0.6rem 1rem',
              background: 'linear-gradient(90deg, rgba(100,108,255,0.18) 0%, rgba(100,108,255,0.06) 100%)',
              border: '1px solid rgba(100,108,255,0.35)',
              borderLeft: '4px solid #646cff',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
            }}>
              <span style={{ fontSize: '0.68rem', fontWeight: 700, color: '#646cff', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                Metric {currentGroupIndex + 1}/{metricGroups.length}
              </span>
              <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#fff' }}>
                {currentGroup.metric}
              </span>
              <span style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.55)' }}>
                — {currentGroup.metricFull}
              </span>
              <span style={{ marginLeft: 'auto', fontSize: '0.72rem', color: 'rgba(255,255,255,0.3)' }}>
                Round {currentTick?.round} · {currentTickIndex - currentGroup.firstIndex + 1}/{currentGroup.lastIndex - currentGroup.firstIndex + 1} ticks
              </span>
            </div>
          )}

          <SymmetryView tickData={currentTick} />

          <div style={{ marginTop: '1rem' }}>
            <EthicsBadges ethics={currentTick.ethics} />
          </div>

          <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: 'rgba(255,255,255,0.5)' }}>
            <span>Conv: {currentTick.convergence.percentage}%</span>
            <span style={{ marginLeft: '1rem' }}>Status: {currentTick.convergence.status}</span>
            <span style={{ marginLeft: '1rem' }}>Crux: {currentTick.crux.status}</span>
          </div>

          {narrativeOpen && (
            <div style={{ marginTop: '1.25rem' }}>
              <DeliberationNarrative tickData={currentTick} />
            </div>
          )}

          {/* Bottom navigation — mirrors top controls, no scrolling required */}
          <div style={{
            marginTop: '1.5rem',
            paddingTop: '1rem',
            borderTop: '1px solid rgba(255,255,255,0.08)',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            flexWrap: 'wrap',
          }}>
            <button
              onClick={handlePrevMetric}
              disabled={currentGroupIndex <= 0}
              title="Jump to previous metric"
              style={{ opacity: currentGroupIndex <= 0 ? 0.3 : 1 }}
            >
              ⏮
            </button>

            <button onClick={handlePrevTick} disabled={currentTickIndex === 0}>← Prev</button>

            <span style={{ fontSize: '0.82rem', color: 'rgba(255,255,255,0.6)', minWidth: '140px', textAlign: 'center' }}>
              <span style={{ color: 'rgba(255,255,255,0.9)', fontWeight: 600 }}>{currentTick?.metric}</span>
              {' '}R{currentTick?.round}
              <span style={{ color: 'rgba(255,255,255,0.35)', marginLeft: '0.4rem' }}>
                · {currentTickIndex + 1}/{currentData.ticks.length}
              </span>
            </span>

            <button onClick={handleNextTick} disabled={currentTickIndex === currentData.ticks.length - 1}>Next →</button>

            <button
              onClick={handleNextMetric}
              disabled={currentGroupIndex >= metricGroups.length - 1}
              title="Jump to next metric"
              style={{ opacity: currentGroupIndex >= metricGroups.length - 1 ? 0.3 : 1 }}
            >
              ⏭
            </button>

            <CruxToggle
              active={cruxMode}
              onToggle={() => {
                const entering = !cruxMode
                setCruxMode(entering)
                if (entering && cruxTicks.length > 0) {
                  const first = cruxTicks.find(({ index }) => index >= currentTickIndex) || cruxTicks[0]
                  setCurrentTickIndex(first.index)
                }
              }}
              cruxCount={cruxTicks.length}
            />
          </div>
        </div>

        {drawerOpen && (
          <div className="side-panel">
            <CalibrationDrawer
              worldviewPair={currentData.worldview_pair}
              tickData={currentTick}
            />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
