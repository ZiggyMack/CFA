import { useState } from 'react'

const CruxToggle = () => {
  const [showTooltip, setShowTooltip] = useState(false)

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <button
        disabled
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        style={{
          opacity: 0.5,
          cursor: 'not-allowed',
          position: 'relative'
        }}
      >
        🎯 Crux Impact View
      </button>

      {showTooltip && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            marginTop: '0.5rem',
            padding: '0.75rem 1rem',
            backgroundColor: 'rgba(0, 0, 0, 0.95)',
            borderRadius: '8px',
            fontSize: '0.85rem',
            whiteSpace: 'nowrap',
            zIndex: 1000,
            border: '1px solid rgba(255,255,255,0.2)',
            pointerEvents: 'none'
          }}
        >
          <div style={{ fontWeight: 'bold', color: '#f59e0b', marginBottom: '0.3rem' }}>
            Phase 2 Feature
          </div>
          <div style={{ color: 'rgba(255,255,255,0.7)' }}>
            Available once pilot data arrives
          </div>
          <div style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.5)', marginTop: '0.3rem' }}>
            Will show convergence with/without Crux toggle
          </div>
        </div>
      )}
    </div>
  )
}

export default CruxToggle
