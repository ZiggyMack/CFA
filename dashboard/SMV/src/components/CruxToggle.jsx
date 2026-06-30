const CruxToggle = ({ active, onToggle, cruxCount }) => {
  return (
    <button
      onClick={onToggle}
      title={active
        ? `Crux mode ON — navigating ${cruxCount} crux moment${cruxCount !== 1 ? 's' : ''}. Click to exit.`
        : `Crux Impact View — jump between crux declaration points only (${cruxCount} in this session)`
      }
      style={{
        borderColor: active ? 'rgba(239,68,68,0.7)' : undefined,
        backgroundColor: active ? 'rgba(239,68,68,0.15)' : undefined,
        color: active ? '#fca5a5' : undefined,
      }}
    >
      ⚑ Crux{active ? ` · ${cruxCount} moments` : ' Impact View'}
    </button>
  )
}

export default CruxToggle
