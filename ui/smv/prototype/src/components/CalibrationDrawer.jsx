const CalibrationDrawer = ({ worldviewPair, tickData }) => {
  // Mock calibration data (in Phase 2, this will come from profile YAML)
  // For now, showing representative values based on worldview pair

  const getMockCalibration = () => {
    if (worldviewPair === 'CT_vs_ProcessTheology') {
      return {
        pro: {
          worldview: 'Classical Theism',
          stance: 'PRO',
          axiom_confidence: 0.85,
          burden_of_proof: 0.60,
          charity_interpretation: 0.75,
          edge_case_weight: 0.50,
          explanatory_credit: 0.70,
          historical_weight: 0.80,
          lived_experience: 0.65
        },
        anti: {
          worldview: 'Classical Theism',
          stance: 'ANTI (Process Theology)',
          axiom_confidence: 0.70,
          burden_of_proof: 0.50,
          charity_interpretation: 0.75,
          edge_case_weight: 0.60,
          explanatory_credit: 0.65,
          historical_weight: 0.60,
          lived_experience: 0.70
        }
      }
    } else if (worldviewPair === 'CT_vs_Naturalism') {
      return {
        pro: {
          worldview: 'Classical Theism',
          stance: 'PRO',
          axiom_confidence: 0.85,
          burden_of_proof: 0.60,
          charity_interpretation: 0.75,
          edge_case_weight: 0.50,
          explanatory_credit: 0.70,
          historical_weight: 0.80,
          lived_experience: 0.65
        },
        anti: {
          worldview: 'Classical Theism',
          stance: 'ANTI (Naturalism)',
          axiom_confidence: 0.40,
          burden_of_proof: 0.75,
          charity_interpretation: 0.70,
          edge_case_weight: 0.60,
          explanatory_credit: 0.45,
          historical_weight: 0.30,
          lived_experience: 0.50
        }
      }
    }

    // Default fallback
    return {
      pro: {
        worldview: 'Unknown',
        stance: 'PRO',
        axiom_confidence: 0.70,
        burden_of_proof: 0.50,
        charity_interpretation: 0.70,
        edge_case_weight: 0.50,
        explanatory_credit: 0.60,
        historical_weight: 0.60,
        lived_experience: 0.60
      },
      anti: {
        worldview: 'Unknown',
        stance: 'ANTI',
        axiom_confidence: 0.50,
        burden_of_proof: 0.50,
        charity_interpretation: 0.70,
        edge_case_weight: 0.50,
        explanatory_credit: 0.50,
        historical_weight: 0.50,
        lived_experience: 0.60
      }
    }
  }

  const calibration = getMockCalibration()
  const parameters = [
    { key: 'axiom_confidence', label: 'Axiom Confidence' },
    { key: 'burden_of_proof', label: 'Burden of Proof' },
    { key: 'charity_interpretation', label: 'Charity Interpretation' },
    { key: 'edge_case_weight', label: 'Edge Case Weight' },
    { key: 'explanatory_credit', label: 'Explanatory Credit' },
    { key: 'historical_weight', label: 'Historical Weight' },
    { key: 'lived_experience', label: 'Lived Experience' }
  ]

  const getDifference = (key) => {
    const diff = Math.abs(calibration.pro[key] - calibration.anti[key])
    if (diff > 0.20) return 'high'
    if (diff > 0.10) return 'medium'
    return 'low'
  }

  const getDifferenceColor = (level) => {
    const colors = {
      high: '#ef4444',
      medium: '#fbbf24',
      low: '#22c55e'
    }
    return colors[level] || '#888'
  }

  return (
    <div>
      <h3 style={{ marginBottom: '1rem', fontSize: '1.1rem' }}>
        Calibration Transparency
      </h3>

      <div style={{ marginBottom: '1.5rem', fontSize: '0.85rem', color: 'rgba(255,255,255,0.6)' }}>
        Comparing bias adjustments for {worldviewPair.replace('_', ' ')}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {parameters.map(({ key, label }) => {
          const proValue = calibration.pro[key]
          const antiValue = calibration.anti[key]
          const diffLevel = getDifference(key)

          return (
            <div key={key} style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.75rem' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: '500', marginBottom: '0.5rem', color: 'rgba(255,255,255,0.8)' }}>
                {label}
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '1rem' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.75rem', color: '#60a5fa', marginBottom: '0.2rem' }}>
                    PRO
                  </div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>
                    {(proValue * 100).toFixed(0)}%
                  </div>
                </div>

                <div style={{
                  width: '6px',
                  height: '6px',
                  borderRadius: '50%',
                  backgroundColor: getDifferenceColor(diffLevel)
                }} title={`Difference: ${diffLevel}`} />

                <div style={{ flex: 1, textAlign: 'right' }}>
                  <div style={{ fontSize: '0.75rem', color: '#f87171', marginBottom: '0.2rem' }}>
                    ANTI
                  </div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 'bold' }}>
                    {(antiValue * 100).toFixed(0)}%
                  </div>
                </div>
              </div>

              {/* Visual bar comparison */}
              <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.25rem', height: '4px' }}>
                <div
                  style={{
                    flex: proValue,
                    backgroundColor: '#60a5fa',
                    borderRadius: '2px'
                  }}
                />
                <div
                  style={{
                    flex: antiValue,
                    backgroundColor: '#f87171',
                    borderRadius: '2px'
                  }}
                />
              </div>
            </div>
          )
        })}
      </div>

      <div style={{ marginTop: '1.5rem', padding: '0.75rem', backgroundColor: 'rgba(100, 108, 255, 0.1)', borderRadius: '8px', fontSize: '0.8rem' }}>
        <div style={{ fontWeight: 'bold', marginBottom: '0.3rem' }}>Note:</div>
        <div style={{ color: 'rgba(255,255,255,0.6)' }}>
          Calibration values shown are mock data for Phase 1. In Phase 2, these will be extracted from worldview profile YAML blocks (lines 277-287 for PRO, 317+ for ANTI).
        </div>
      </div>
    </div>
  )
}

export default CalibrationDrawer
