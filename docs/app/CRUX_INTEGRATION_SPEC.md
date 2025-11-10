<!---
FILE: CRUX_INTEGRATION_SPEC.md
PURPOSE: Complete specification for integrating Crux Points architecture into CFA application
VERSION: 1.0.0
STATUS: Implementation Specification
DEPENDS_ON: auditors/CRUX_TEMPLATE.md, auditors/VUDU_CFA.md, profiles/comparisons/*.yaml
NEEDED_BY: App development team, UI/UX implementation
MOVES_WITH: /docs/app/
LAST_UPDATE: 2025-11-10 [B-STORM_4 Entry 3: Crux architecture app requirements]
--->

# Crux Points - App Integration Specification

**Version:** 1.0.0
**Status:** Implementation Specification
**Target:** CFA Web Application
**Priority:** Required before CT vs MdN pilot scoring session

---

## Executive Summary

This specification defines how Crux Points (named impasses in worldview scoring) integrate into the CFA application. Key features:

1. **Crux Handling Lever** - User control over uncertainty penalty
2. **Three-View System** - Self-Reported, Peer-Reviewed, Delta tabs
3. **BFI Dropdown Integration** - Crux controls in existing info panel
4. **Preset Mode Auto-Configuration** - Skeptic/Zealot/Diplomat modes auto-set Crux
5. **Comparison File Loading** - Context-dependent scoring via /profiles/comparisons/*.yaml
6. **Session Metadata Logging** - YAML hash, Domain 7 diff, Crux count

---

## 1. Crux Handling Lever UI

### Location

**Primary:** Integrated into BFI Dropdown Info Panel (existing UI component)

**Rationale:**
- Users already go to BFI dropdown to access Mr. Brute's Ledger
- Crux context lives in Ledger (philosophical background)
- Harmonious with existing information flow
- Avoids cluttering main comparison view

### UI Components

**Component 1: Crux Mode Checkbox**

```tsx
<div className="crux-mode-control">
  <label>
    <input
      type="checkbox"
      checked={cruxMode === 'NORMALIZE_UNCERTAINTY'}
      onChange={handleCruxToggle}
      disabled={presetLocked}  // If user locked preset mode
    />
    <span className="crux-label">
      CRUX Mode
      <Tooltip content={CRUX_TOOLTIP_TEXT} />
    </span>
  </label>
  <span className="crux-status">
    {cruxMode === 'NORMALIZE_UNCERTAINTY' ?
      'Normalize Uncertainty (Skeptic)' :
      'Carry Forward (Zealot)'}
  </span>
</div>
```

**Tooltip Text:**
```
CRUX Mode: Apply uncertainty penalty for unresolved disagreements

When auditors can't reach 98% convergence after genuine deliberation,
a Crux Point is declared. This setting controls how Crux affects scores:

☑ NORMALIZE UNCERTAINTY (Skeptic Mode)
  Apply penalty based on disagreement width. Wider spread = larger penalty.
  Philosophy: "Unresolved disagreement signals measurement instability"

☐ CARRY FORWARD (Zealot Mode)
  Use team decision without penalty. Document Crux in story.
  Philosophy: "Honest disagreement doesn't invalidate the score"

Diplomat Mode: Context-dependent (varies by metric and story impact)

Learn more about Crux Points in Mr. Brute's Ledger.
```

---

**Component 2: Crux Summary Badge**

Shows Crux count for current comparison:

```tsx
<div className="crux-summary-badge">
  {cruxCount > 0 && (
    <span className="crux-indicator">
      🔺 {cruxCount} Crux Point{cruxCount > 1 ? 's' : ''} declared
      <Tooltip content={`Click View 3 (Delta) to see details`} />
    </span>
  )}
</div>
```

**Placement:** Below BFI dropdown, above Ledger link

---

### Preset Mode Integration

**Auto-Configuration Logic:**

```typescript
interface PresetModeConfig {
  skeptic: {
    cruxMode: 'NORMALIZE_UNCERTAINTY',
    userOverrideable: true,
    description: 'Applies uncertainty penalty to all Crux Points'
  },
  zealot: {
    cruxMode: 'CARRY_FORWARD',
    userOverrideable: true,
    description: 'Uses team decision, documents Crux in story'
  },
  diplomat: {
    cruxMode: 'HYBRID',
    userOverrideable: true,
    description: 'Context-dependent (foundational metrics → normalize, edge metrics → carry forward)',
    logic: (metric: string, storyImpact: string) => {
      const foundationalMetrics = ['BFI', 'CA', 'IP'];
      if (foundationalMetrics.includes(metric) || storyImpact === 'high') {
        return 'NORMALIZE_UNCERTAINTY';
      }
      return 'CARRY_FORWARD';
    }
  }
}
```

**User Experience:**

1. User selects preset mode (Skeptic/Zealot/Diplomat)
2. Crux checkbox auto-checks/unchecks based on mode
3. Status text updates: "(auto-set by [Mode] preset)"
4. User can click checkbox to override
5. Override shows warning: "⚠️ Overriding preset mode default"
6. Override persists only for current session (resets on worldview change)

---

## 2. Three-View System

### Tab Structure

**Primary Component:** Scoring Results Panel

**Tabs:**
1. **View 1: Self-Reported** (worldview's own scores, UNAUDITED)
2. **View 2: Peer-Reviewed** (after adversarial deliberation, AUDITED)
3. **View 3: Delta** (shows shift + Crux Points)

**Default View:** View 2 (Peer-Reviewed) if available, else View 1

---

### View 1: Self-Reported

**Data Source:** Worldview profile YAML (`profiles/worldviews/[WV].md`)

**Display:**

```tsx
<div className="view-self-reported">
  <h3>Self-Reported Scores</h3>
  <p className="view-description">
    Scores from the worldview's own profile (UNAUDITED)
  </p>

  <div className="metrics-table">
    {metrics.map(metric => (
      <div className="metric-row" key={metric.id}>
        <span className="metric-name">{metric.name}</span>
        <span className="metric-score">{metric.selfReportedScore}</span>
        <span className="metric-status badge-unaudited">Unaudited</span>
      </div>
    ))}
  </div>

  <div className="view-notice">
    ℹ️ These scores represent the worldview's self-understanding before
    adversarial peer review. See View 2 for audited scores.
  </div>
</div>
```

**Styling:**
- Muted colors (grays, light blues)
- "UNAUDITED" badge on each metric
- Notice box at bottom explaining what self-reported means

---

### View 2: Peer-Reviewed

**Data Source:** Comparison file (`/profiles/comparisons/[WV1]_vs_[WV2].yaml`)

**Display:**

```tsx
<div className="view-peer-reviewed">
  <h3>Peer-Reviewed Scores</h3>
  <p className="view-description">
    Scores after adversarial deliberation by Claude, Grok, and Nova (AUDITED)
  </p>

  <div className="metrics-table">
    {metrics.map(metric => (
      <div className="metric-row" key={metric.id}>
        <span className="metric-name">{metric.name}</span>
        <span className="metric-score">
          {metric.peerReviewedScore}
          {metric.hasCrux && <span className="crux-icon">🔺</span>}
        </span>
        <span className="metric-status badge-audited">Audited</span>
        {metric.hasCrux && (
          <Tooltip content={`Crux: ${metric.cruxQuestion}`}>
            <button onClick={() => openCruxDetails(metric.cruxId)}>
              Details
            </button>
          </Tooltip>
        )}
      </div>
    ))}
  </div>

  <div className="convergence-summary">
    ✓ Average convergence: {convergenceRate}%
    {cruxCount > 0 && (
      <span> | 🔺 {cruxCount} Crux Point{cruxCount > 1 ? 's' : ''}</span>
    )}
  </div>
</div>
```

**Crux Handling Integration:**

```typescript
function calculatePeerReviewedScore(
  metric: Metric,
  cruxMode: CruxMode
): number {
  if (!metric.hasCrux) {
    return metric.teamDecision;  // Full convergence, no Crux
  }

  if (cruxMode === 'CARRY_FORWARD') {
    return metric.teamDecision;  // Use decision, no penalty
  }

  if (cruxMode === 'NORMALIZE_UNCERTAINTY') {
    const { claudeScore, grokScore } = metric.auditorPositions;
    const midpoint = (claudeScore + grokScore) / 2;
    const spread = Math.abs(claudeScore - grokScore) / 2;
    const uncertaintyFactor = midpoint > 0 ? spread / midpoint : 1.0;
    return midpoint * (1 - uncertaintyFactor);
  }

  if (cruxMode === 'HYBRID') {
    return calculateHybridScore(metric);  // Uses diplomat logic
  }
}
```

**Styling:**
- Vibrant colors (greens for high scores, yellows for medium)
- "AUDITED" badge in green
- Crux icon (🔺) stands out in red/orange
- Hover effect on Crux metrics shows tooltip

---

### View 3: Delta

**Data Source:** Comparison between View 1 and View 2

**Display:**

```tsx
<div className="view-delta">
  <h3>Delta Analysis</h3>
  <p className="view-description">
    Shows how peer review changed self-reported scores + full Crux details
  </p>

  <div className="metrics-table">
    {metrics.map(metric => (
      <div className="metric-row expanded" key={metric.id}>
        <div className="metric-header">
          <span className="metric-name">{metric.name}</span>
          <span className="delta-value"
                className={metric.delta > 0 ? 'increase' : 'decrease'}>
            {metric.delta > 0 ? '↑' : '↓'} {Math.abs(metric.delta).toFixed(1)}
          </span>
        </div>

        <div className="score-comparison">
          <div className="score-before">
            <label>Self-Reported</label>
            <span>{metric.selfReportedScore}</span>
          </div>
          <div className="arrow">→</div>
          <div className="score-after">
            <label>Peer-Reviewed</label>
            <span>{metric.peerReviewedScore}</span>
          </div>
        </div>

        {metric.hasCrux && (
          <CruxDetailsPanel crux={metric.cruxData} />
        )}
      </div>
    ))}
  </div>
</div>
```

**Crux Details Panel (Expanded View):**

```tsx
<div className="crux-details-panel">
  <div className="crux-header">
    <h4>🔺 {crux.id}: {crux.question}</h4>
    <span className="crux-type badge">{crux.type}</span>
  </div>

  <div className="crux-positions">
    <div className="auditor-position claude">
      <h5>Claude (PRO-{worldview})</h5>
      <p className="position-text">{crux.positions.claude.position}</p>
      <div className="score-proposed">Score: {crux.positions.claude.score_proposed}</div>
      <details>
        <summary>Calibration Applied</summary>
        <ul>
          {crux.positions.claude.calibration_applied.map(param => (
            <li key={param}>{param}</li>
          ))}
        </ul>
      </details>
    </div>

    <div className="auditor-position grok">
      <h5>Grok (ANTI-{worldview})</h5>
      <p className="position-text">{crux.positions.grok.position}</p>
      <div className="score-proposed">Score: {crux.positions.grok.score_proposed}</div>
      <details>
        <summary>Calibration Applied</summary>
        <ul>
          {crux.positions.grok.calibration_applied.map(param => (
            <li key={param}>{param}</li>
          ))}
        </ul>
      </details>
    </div>

    <div className="auditor-position nova">
      <h5>Nova (FAIRNESS)</h5>
      <p className="assessment-text">{crux.positions.nova.assessment}</p>
      <div className="pattern-detected">
        <strong>Pattern:</strong> {crux.positions.nova.pattern_detected}
      </div>
      <div className="recommendation">
        <strong>Recommendation:</strong> {crux.positions.nova.recommendation}
      </div>
    </div>
  </div>

  <div className="crux-impact">
    <div className="why-matters">
      <strong>Why This Matters:</strong>
      <p>{crux.why_matters}</p>
    </div>
    <div className="impact-metrics">
      <span className="story-impact">Story Impact: {crux.story_impact}</span>
      <span className="ypa-sensitivity">YPA Sensitivity: ±{crux.ypa_sensitivity * 100}%</span>
    </div>
  </div>

  <div className="crux-resolution">
    <span className="status badge">{crux.resolution_status}</span>
    {crux.team_decision && (
      <div className="team-decision">
        <strong>Team Decision:</strong> {crux.team_decision}
      </div>
    )}
    {crux.uncertainty_penalty_applied && (
      <div className="penalty-applied">
        ⚠️ Uncertainty penalty applied (NORMALIZE mode)
      </div>
    )}
  </div>
</div>
```

**Styling:**
- Three columns for three auditor positions
- Color-coded (Claude blue, Grok orange, Nova purple)
- Collapsible calibration details (reduce visual clutter)
- Impact metrics highlighted in boxes
- Resolution status badge (color varies by status)

---

## 3. Comparison File Loading

### File Structure

**Directory:** `/profiles/comparisons/`

**Naming Convention:** `[WV1]_vs_[WV2].yaml`

**Example Files:**
- `CT_vs_MdN.yaml` (Classical Theism vs Methodological Naturalism)
- `CT_vs_Buddhism.yaml`
- `MdN_vs_ErrorTheory.yaml`

**Note:** Order matters for directionality (CT_vs_MdN is CT being reviewed by MdN advocates, not vice versa)

---

### File Schema

```yaml
# /profiles/comparisons/CT_vs_MdN.yaml

comparison_metadata:
  worldview_under_review: "Classical Theism"
  comparison_context: "Methodological Naturalism"
  session_id: "ct-mdn-pilot-2025-11-15"
  session_date: 2025-11-15

  calibration_version:
    yaml_hash: "a3f9c2b1e5d8..."
    domain_7_diff_summary: "No changes since v1.0.0"

  auditor_assignments:
    claude:
      stance: "PRO-CT"
      lens: "Teleological"
      profile_reference: "auditors/Bootstrap/Claude/Identity/SKELETON.md"
    grok:
      stance: "ANTI-CT"
      lens: "Empirical"
      profile_reference: "auditors/Bootstrap/BOOTSTRAP_GROK.md"
    nova:
      stance: "FAIRNESS"
      lens: "Symmetry"
      profile_reference: "auditors/Bootstrap/BOOTSTRAP_NOVA.md"

peer_reviewed_scores:
  BFI:
    self_reported: 8.5
    peer_reviewed: 6.9
    delta: -1.6
    convergence: 73%
    has_crux: true
    crux_id: "CRUX_BFI_001"

  CA:
    self_reported: 9.0
    peer_reviewed: 8.7
    delta: -0.3
    convergence: 98.5%
    has_crux: false

  # ... (other metrics)

crux_points:
  - id: CRUX_BFI_001
    # (Full Crux metadata from CRUX_TEMPLATE.md)

convergence_summary:
  metrics_scored: 7
  full_convergence: 6  # ≥98%
  crux_declared: 1     # <98%, confirmed Crux
  avg_convergence: 96.4%

process_claude_review:
  date: 2025-11-16
  gap_closure: false
  rotation_triggered: false
  notes: "CRUX_BFI_001 documented as framework limitation, not bias"
```

---

### Loading Logic

```typescript
async function loadComparisonScores(
  worldview1: string,
  worldview2: string
): Promise<ComparisonData | null> {
  const filename = `${worldview1}_vs_${worldview2}.yaml`;
  const filepath = `/profiles/comparisons/${filename}`;

  try {
    const data = await fetchYAML(filepath);
    return parseComparisonData(data);
  } catch (error) {
    if (error.status === 404) {
      // Comparison file doesn't exist yet
      return null;
    }
    throw error;
  }
}

function getScoresForComparison(
  worldview1: string,
  worldview2: string,
  cruxMode: CruxMode
): ScoringData {
  const comparisonData = await loadComparisonScores(worldview1, worldview2);

  if (!comparisonData) {
    // Fall back to self-reported
    return {
      view: 'SELF_REPORTED',
      scores: loadSelfReportedScores(worldview1),
      notice: `Peer review pending for ${worldview1} vs ${worldview2}`,
      availableViews: ['SELF_REPORTED']
    };
  }

  // Apply Crux handling to peer-reviewed scores
  const peerReviewedScores = comparisonData.peer_reviewed_scores.map(
    metric => ({
      ...metric,
      final_score: calculatePeerReviewedScore(metric, cruxMode)
    })
  );

  return {
    view: 'PEER_REVIEWED',
    scores: peerReviewedScores,
    cruxPoints: comparisonData.crux_points,
    metadata: comparisonData.comparison_metadata,
    availableViews: ['SELF_REPORTED', 'PEER_REVIEWED', 'DELTA']
  };
}
```

---

### Fallback Behavior

**Scenario 1: Comparison file doesn't exist**

```tsx
<div className="peer-review-pending">
  <h3>Peer Review Pending</h3>
  <p>
    This comparison ({worldview1} vs {worldview2}) has not yet been
    peer-reviewed by our auditor team.
  </p>
  <p>
    Currently showing <strong>Self-Reported</strong> scores from
    {worldview1}'s profile. These represent the worldview's own
    self-understanding and have not undergone adversarial checking.
  </p>
  <button onClick={requestPeerReview}>Request Peer Review</button>
</div>
```

**Scenario 2: Comparison exists but reverse direction needed**

If user selects `MdN vs CT` but only `CT_vs_MdN.yaml` exists:

```typescript
// Check both directions
const forward = await loadComparisonScores(worldview1, worldview2);
const reverse = await loadComparisonScores(worldview2, worldview1);

if (!forward && reverse) {
  // Show notice about directionality
  return {
    ...reverse,
    notice: `Showing ${worldview2} vs ${worldview1} comparison (reverse direction)`
  };
}
```

---

## 4. Session Metadata Logging

### What Gets Logged

Every scoring comparison captures:

```typescript
interface SessionMetadata {
  session_id: string;           // "ct-mdn-pilot-2025-11-15"
  timestamp: Date;

  worldviews: {
    under_review: string;       // "Classical Theism"
    comparison_context: string; // "Methodological Naturalism"
  };

  calibration_version: {
    yaml_hash: string;          // Git hash or content hash of YAML block
    domain_7_diff_summary: string; // "No changes" or "Updated axiom_confidence"
  };

  auditor_assignments: {
    claude: { stance: string; lens: string; };
    grok: { stance: string; lens: string; };
    nova: { stance: string; lens: string; };
  };

  crux_handling: {
    mode: CruxMode;             // CARRY_FORWARD | NORMALIZE_UNCERTAINTY | HYBRID
    preset_mode: string;        // "Skeptic" | "Zealot" | "Diplomat"
    user_override: boolean;
  };

  convergence_summary: {
    metrics_scored: number;
    full_convergence: number;   // Count of ≥98%
    crux_declared: number;      // Count of <98% confirmed Crux
    avg_convergence: number;    // Percentage
  };

  crux_points_declared: string[]; // Array of Crux IDs

  process_claude_review: {
    reviewed: boolean;
    review_date?: Date;
    gap_closure?: boolean;
    rotation_triggered?: boolean;
    notes?: string;
  };
}
```

### Where It's Stored

**Option 1: Embedded in Comparison File**

Store as `session_metadata` block in `/profiles/comparisons/*.yaml`

**Pros:**
- All data in one place
- Easy to access during comparison load
- Version controlled via Git

**Cons:**
- File grows with each session
- Need to manage history

**Option 2: Separate Session Log Directory**

Store in `/session_logs/[session_id].yaml`

**Pros:**
- Clean separation of concerns
- Easier to analyze sessions in aggregate
- Comparison files stay focused

**Cons:**
- Two files to load for full context
- Cross-referencing needed

**Recommendation:** Hybrid
- Current session metadata embedded in comparison file
- Historical sessions archived to `/session_logs/archive/`
- Process Claude maintains session index

---

### YAML Hash Calculation

```typescript
function calculateYAMLHash(worldviewProfile: string): string {
  // Extract YAML block from worldview profile
  const yamlMatch = worldviewProfile.match(/```yaml\n([\s\S]+?)\n```/);
  if (!yamlMatch) {
    throw new Error('No YAML block found in profile');
  }

  const yamlContent = yamlMatch[1];

  // Use SHA-256 hash (first 16 chars for brevity)
  const hash = crypto
    .createHash('sha256')
    .update(yamlContent)
    .digest('hex')
    .substring(0, 16);

  return hash;
}
```

**Usage:**
- Computed at session start
- Logged in session metadata
- Compared against previous sessions to detect calibration drift

---

### Domain 7 Diff Summary

```typescript
async function getDomain7DiffSummary(
  worldview: string,
  currentHash: string
): Promise<string> {
  // Check if Process Claude has logged changes
  const changeLog = await fetchDomain7ChangeLog(worldview);

  if (!changeLog || changeLog.latestHash === currentHash) {
    return "No changes since last review";
  }

  // Extract changes from most recent Domain 7 review
  const changes = changeLog.changes.map(c =>
    `${c.parameter}: ${c.oldValue} → ${c.newValue}`
  );

  return changes.join('; ');
}
```

**Example Output:**
```
"axiom_confidence: 0.85 → 0.80; edge_case_weight: 0.30 → 0.35"
```

---

## 5. UI/UX Flow Summary

### User Journey: Comparing Two Worldviews

**Step 1: User selects comparison**
- Choose Worldview A and Worldview B
- App attempts to load `/profiles/comparisons/A_vs_B.yaml`

**Step 2: Preset mode auto-configuration**
- User's preset mode (Skeptic/Zealot/Diplomat) auto-sets Crux checkbox
- Tooltip explains what Crux Mode does
- User can override if desired

**Step 3: Three-View tabs displayed**
- Default to View 2 (Peer-Reviewed) if available
- Tab badges show status:
  - View 1: "Unaudited" (gray)
  - View 2: "Audited" (green) + Crux count badge if >0
  - View 3: "Delta" (blue) + delta summary

**Step 4: Crux Points visible**
- View 2: Crux icon (🔺) next to metrics with Crux
- Hover tooltip shows Crux question
- Click for full details (opens View 3 or modal)

**Step 5: View 3 exploration**
- See before/after comparison
- Read auditor positions side-by-side
- Understand why disagreement happened
- Review calibration compliance

**Step 6: BFI Dropdown context**
- Click BFI dropdown to access Mr. Brute's Ledger
- See Crux Mode checkbox and status
- Crux Summary badge shows total Crux count
- Link to full Crux template documentation

---

## 6. Implementation Checklist

### Phase 1: Data Layer (Week 1)

- [ ] Create `/profiles/comparisons/` directory structure
- [ ] Define comparison file YAML schema
- [ ] Implement `loadComparisonScores()` function
- [ ] Build fallback logic for missing comparison files
- [ ] Add YAML hash calculation utility
- [ ] Set up session metadata logging

### Phase 2: UI Components (Week 2)

- [ ] Add Crux Mode checkbox to BFI dropdown
- [ ] Implement Crux Summary badge
- [ ] Create Three-View tab structure
- [ ] Build Crux icon + tooltip for View 2
- [ ] Design Crux Details Panel for View 3
- [ ] Add preset mode auto-configuration logic

### Phase 3: Scoring Logic (Week 3)

- [ ] Implement `calculatePeerReviewedScore()` with Crux handling
- [ ] Add NORMALIZE UNCERTAINTY formula
- [ ] Build CARRY FORWARD logic
- [ ] Create HYBRID (Diplomat) context-dependent logic
- [ ] Test YPA calculation with Crux adjustments

### Phase 4: Integration & Testing (Week 4)

- [ ] Connect Three-View System to comparison loader
- [ ] Test preset mode interactions (Skeptic/Zealot/Diplomat)
- [ ] Verify user override behavior
- [ ] Validate session metadata logging
- [ ] Test fallback for missing comparison files
- [ ] Cross-browser testing (Chrome, Firefox, Safari)

### Phase 5: Documentation (Ongoing)

- [ ] Update app README with Crux features
- [ ] Create user guide for Three-View System
- [ ] Document Crux Mode for end users (tooltip + help page)
- [ ] Add developer docs for comparison file schema
- [ ] Provide examples of Crux handling in different modes

---

## 7. Technical Dependencies

**Required:**
- YAML parser (js-yaml or similar)
- Cryptographic hash function (crypto.createHash for Node.js, or SubtleCrypto for browser)
- React 18+ (for component architecture)
- TypeScript (for type safety in scoring logic)

**Optional but Recommended:**
- React Query (for caching comparison file loads)
- Zustand or Redux (for global Crux Mode state management)
- Framer Motion (for smooth View tab transitions)

---

## 8. Performance Considerations

**Comparison File Caching:**
- Cache comparison files client-side after first load
- Invalidate cache on YAML hash mismatch
- Preload related comparisons (e.g., if viewing CT vs MdN, preload CT vs Buddhism)

**Lazy Loading:**
- Load View 1 (Self-Reported) immediately
- Lazy load View 2 (Peer-Reviewed) only when comparison file found
- Defer View 3 (Delta) calculation until tab clicked

**Crux Details Rendering:**
- Render Crux Details Panel only when expanded
- Virtualize if many Crux Points (unlikely for MVP, but future-proof)

---

## 9. Accessibility

**WCAG 2.1 AA Compliance:**

- [ ] Crux checkbox has `aria-label` and keyboard navigation
- [ ] Tooltip content readable by screen readers
- [ ] Crux icon (🔺) has text alternative "Crux Point declared"
- [ ] Color-coded auditor positions also use icons/patterns (not just color)
- [ ] View tabs have `role="tablist"` and proper ARIA attributes
- [ ] Crux Details Panel has collapsible sections with `aria-expanded`

---

## 10. Future Enhancements

**Phase 2 (Post-Pilot):**

1. **Crux Timeline View** - Show how Crux Points emerge/resolve over time
2. **Crux Heatmap** - Visualize which metrics produce most Crux across all worldviews
3. **Interactive Crux Resolution** - Allow users to propose resolutions, vote on positions
4. **Crux Export** - Download Crux data as JSON/CSV for external analysis
5. **Crux Notifications** - Alert users when new Crux declared for watched comparisons

**Phase 3 (Advanced):**

1. **Machine Learning Crux Prediction** - Predict likely Crux based on worldview features
2. **Automated Rotation Triggers** - When Crux density exceeds threshold, suggest assignment swap
3. **Third-Party Auditor Integration** - Allow external experts to weigh in on Crux
4. **Crux Visualization** - Network graph showing relationships between Crux across worldviews

---

## 11. Testing Strategy

### Unit Tests

```typescript
describe('Crux Handling', () => {
  test('CARRY FORWARD uses team decision without penalty', () => {
    const metric = { teamDecision: 7.0, hasCrux: true };
    const score = calculatePeerReviewedScore(metric, 'CARRY_FORWARD');
    expect(score).toBe(7.0);
  });

  test('NORMALIZE UNCERTAINTY applies penalty correctly', () => {
    const metric = {
      hasCrux: true,
      auditorPositions: { claudeScore: 8.0, grokScore: 6.0 }
    };
    const score = calculatePeerReviewedScore(metric, 'NORMALIZE_UNCERTAINTY');
    const midpoint = 7.0;
    const spread = 1.0;
    const uncertainty = spread / midpoint; // ~0.143
    const expected = midpoint * (1 - uncertainty); // ~6.0
    expect(score).toBeCloseTo(expected, 2);
  });

  test('HYBRID uses context-dependent logic', () => {
    const foundationalMetric = { metric: 'BFI', storyImpact: 'high' };
    const edgeMetric = { metric: 'LS', storyImpact: 'low' };

    expect(getDiplomatMode(foundationalMetric)).toBe('NORMALIZE_UNCERTAINTY');
    expect(getDiplomatMode(edgeMetric)).toBe('CARRY_FORWARD');
  });
});
```

### Integration Tests

```typescript
describe('Comparison File Loading', () => {
  test('Loads comparison file when available', async () => {
    const data = await loadComparisonScores('CT', 'MdN');
    expect(data).toBeDefined();
    expect(data.comparison_metadata.worldview_under_review).toBe('Classical Theism');
  });

  test('Falls back to self-reported when comparison missing', async () => {
    const data = await loadComparisonScores('CT', 'Hinduism');
    expect(data).toBeNull();

    const scores = getScoresForComparison('CT', 'Hinduism', 'CARRY_FORWARD');
    expect(scores.view).toBe('SELF_REPORTED');
    expect(scores.notice).toContain('Peer review pending');
  });
});
```

### E2E Tests (Playwright/Cypress)

```typescript
test('User can toggle Crux Mode and see score changes', async ({ page }) => {
  await page.goto('/compare?wv1=CT&wv2=MdN');

  // Default: Skeptic Mode (NORMALIZE UNCERTAINTY)
  await expect(page.locator('[data-crux-mode]')).toHaveText('Normalize Uncertainty');
  const scoreNormalized = await page.locator('[data-metric="BFI"] .score').textContent();

  // Toggle to CARRY FORWARD
  await page.click('[data-crux-checkbox]');
  await expect(page.locator('[data-crux-mode]')).toHaveText('Carry Forward');
  const scoreCarryForward = await page.locator('[data-metric="BFI"] .score').textContent();

  // Scores should differ for metrics with Crux
  expect(scoreNormalized).not.toBe(scoreCarryForward);
});
```

---

## 12. Success Metrics

**After implementation, we should see:**

1. **User Engagement:**
   - 70%+ of users explore View 3 (Delta) at least once
   - 40%+ of users override preset mode Crux setting
   - Average time on Crux Details Panel: >30 seconds

2. **Technical Performance:**
   - Comparison file load time: <500ms
   - View tab switch time: <200ms
   - No layout shift when Crux Details Panel expands

3. **Auditor Adoption:**
   - 100% of scoring sessions log session metadata
   - Crux Points declared in 10-20% of metrics (not too few, not too many)
   - Process Claude reviews 100% of Crux Points within 48 hours

---

## 13. Open Questions for Team

**Q1:** Should Crux Mode persist across sessions (localStorage) or reset each time?

**Q2:** How should we handle comparison files for 132 unique pairings? (66 combinations × 2 directions)
- Option A: Create all 132 files (even if empty)
- Option B: Create on-demand as scoring sessions complete
- Option C: Single master file with all comparisons (?)

**Q3:** Should we expose raw YAML hash in UI for advanced users, or hide it in metadata?

**Q4:** Do we need version control for comparison files (e.g., `CT_vs_MdN_v1.0.yaml`)?

**Q5:** How should we handle Crux resolution updates? (Edit existing file, append resolution block, new version?)

---

## 14. Alignment with Nova's Concerns

This implementation directly addresses Nova's Entry 2 findings:

| Nova Finding | Crux Feature | How It Helps |
|--------------|--------------|--------------|
| **#1: Rotation Triggers** | Crux declaration auto-triggers | >30pt spread or 2 failures → review assignments |
| **#2: Calibration Verification** | Crux Handling Lever | Proves YAML matters (affects YPA via penalty) |
| **#4: Compliance Checklist** | Crux positions field | Documents which parameters applied |
| **#5: Telemetry** | Session metadata logging | YAML hash + Domain 7 diff captured |
| **#5: Enforceable Monitoring** | Crux density tracking | Process Claude logs creation/resolution |

**All success criteria met:**
- ✅ Session log captures YAML hash + Domain 7 diff (Nova criterion #1)
- ✅ Calibration compliance in Crux positions (Nova criterion #2)
- ✅ Process Claude records gap closure + rotation actions (Nova criterion #3)

---

**Specification Version:** 1.0.0
**Status:** Ready for Implementation
**Maintained by:** DOC_CLAUDE + Dev Team
**Next Review:** After CT vs MdN pilot session

**"From transparency comes trust. From adversarial checking comes truth. From named impasses comes learning."** 🔺
