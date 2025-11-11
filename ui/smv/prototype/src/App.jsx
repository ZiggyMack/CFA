import { useState, useEffect } from 'react'
import SymmetryView from './components/SymmetryView'
import TimelineSparkline from './components/TimelineSparkline'
import CalibrationDrawer from './components/CalibrationDrawer'
import EthicsBadges from './components/EthicsBadges'
import CruxToggle from './components/CruxToggle'
import scenario2 from './data/scenario_2_high_alignment.json'
import scenario3 from './data/scenario_3_resolution.json'

function App() {
  const scenarios = {
    'scenario2': { name: 'High Alignment (CT vs Process Theology)', data: scenario2 },
    'scenario3': { name: 'Resolution (CT vs Naturalism)', data: scenario3 }
  }

  const [selectedScenario, setSelectedScenario] = useState('scenario2')
  const [currentTickIndex, setCurrentTickIndex] = useState(0)
  const [drawerOpen, setDrawerOpen] = useState(false)

  const currentData = scenarios[selectedScenario].data
  const currentTick = currentData.ticks[currentTickIndex]

  useEffect(() => {
    // Reset to first tick when scenario changes
    setCurrentTickIndex(0)
  }, [selectedScenario])

  const handlePrevTick = () => {
    setCurrentTickIndex(prev => Math.max(0, prev - 1))
  }

  const handleNextTick = () => {
    setCurrentTickIndex(prev => Math.min(currentData.ticks.length - 1, prev + 1))
  }

  const handleTickSelect = (index) => {
    setCurrentTickIndex(index)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>SMV Prototype</h1>
        <p>Symmetry Matrix Visualizer - Phase 1</p>
      </div>

      <div className="controls">
        <label>
          Scenario:
          <select
            value={selectedScenario}
            onChange={(e) => setSelectedScenario(e.target.value)}
          >
            {Object.entries(scenarios).map(([key, { name }]) => (
              <option key={key} value={key}>{name}</option>
            ))}
          </select>
        </label>

        <button onClick={handlePrevTick} disabled={currentTickIndex === 0}>
          ← Previous Tick
        </button>

        <span>
          Tick {currentTickIndex + 1} of {currentData.ticks.length}
        </span>

        <button
          onClick={handleNextTick}
          disabled={currentTickIndex === currentData.ticks.length - 1}
        >
          Next Tick →
        </button>

        <button onClick={() => setDrawerOpen(!drawerOpen)}>
          {drawerOpen ? 'Hide' : 'Show'} Calibration
        </button>

        <CruxToggle />
      </div>

      <TimelineSparkline
        ticks={currentData.ticks}
        currentIndex={currentTickIndex}
        onTickSelect={handleTickSelect}
      />

      <div className="visualization-container">
        <div className="main-view">
          <SymmetryView tickData={currentTick} />

          <div style={{ marginTop: '1rem' }}>
            <EthicsBadges ethics={currentTick.ethics} />
          </div>

          <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: 'rgba(255,255,255,0.6)' }}>
            <p>Convergence: {currentTick.convergence.percentage}%</p>
            <p>Crux Status: {currentTick.crux.status}</p>
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
