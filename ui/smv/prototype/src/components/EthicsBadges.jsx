import { useState } from 'react'

const EthicsBadges = ({ ethics }) => {
  const [hoveredBadge, setHoveredBadge] = useState(null)

  if (!ethics) return null

  const renderBadges = (items, type) => {
    if (!items || items.length === 0) return null

    const icon = {
      examined: '✓',
      deferred: '⏱',
      missing: '⚠'
    }[type]

    return items.map((item, index) => (
      <span
        key={`${type}-${index}`}
        className={`badge ${type}`}
        onMouseEnter={() => setHoveredBadge({ type, item })}
        onMouseLeave={() => setHoveredBadge(null)}
        style={{ cursor: 'help' }}
      >
        {icon} {formatInvariantName(item)}
      </span>
    ))
  }

  const formatInvariantName = (name) => {
    // Convert snake_case to Title Case
    return name
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  const getTooltipText = (type) => {
    const descriptions = {
      examined: 'This ethical invariant has been examined and verified for this tick.',
      deferred: 'This ethical invariant check has been deferred to a later tick.',
      missing: 'This ethical invariant has not been addressed yet.'
    }
    return descriptions[type] || ''
  }

  return (
    <div style={{ position: 'relative' }}>
      <div style={{ marginBottom: '0.5rem', fontSize: '0.9rem', color: 'rgba(255,255,255,0.6)' }}>
        Ethical Invariants:
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0.5rem' }}>
        {renderBadges(ethics.examined, 'examined')}
        {renderBadges(ethics.deferred, 'deferred')}
        {renderBadges(ethics.missing, 'missing')}
      </div>

      {hoveredBadge && (
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
            maxWidth: '300px',
            textAlign: 'center',
            zIndex: 1000,
            border: '1px solid rgba(255,255,255,0.2)'
          }}
        >
          <div style={{ fontWeight: 'bold', marginBottom: '0.3rem', color: '#fff' }}>
            {formatInvariantName(hoveredBadge.item)}
          </div>
          <div style={{ color: 'rgba(255,255,255,0.7)' }}>
            {getTooltipText(hoveredBadge.type)}
          </div>
        </div>
      )}
    </div>
  )
}

export default EthicsBadges
