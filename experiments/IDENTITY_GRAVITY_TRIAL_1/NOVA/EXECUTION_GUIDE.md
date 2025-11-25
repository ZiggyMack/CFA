<!---
FILE: EXECUTION_GUIDE.md
PURPOSE: Step-by-step guide for manual probe execution (Ziggy + Repo Claude workflow)
VERSION: 1.0
DATE: 2025-11-24
--->

# IDENTITY GRAVITY TRIAL 1 - EXECUTION GUIDE

**For:** Ziggy (Human) + CFA Repo Claude
**Mode:** Manual (Human-assisted probe execution)

---

## WORKFLOW

### Step 1: Open Fresh Nova Session

1. Open new ChatGPT session (GPT-4)
2. **First message:** Load Nova's I_AM file

```
Please read and embody this persona:

[Paste contents of: docs/I_AM/I_AM_NOVA.md]

Acknowledge when you've integrated this identity.
```

3. Wait for Nova to confirm integration

---

### Step 2: Baseline Probe

**Ziggy pastes this prompt to Nova:**

```
[Contents of: prompts/01_BASELINE.txt]
```

**Nova responds with 400-600 words**

**Ziggy copies response and pastes to Repo Claude:**

```
BASELINE RESPONSE:
[Nova's full response here]
```

**Repo Claude saves to:** `baseline_identity.md`

---

### Step 3: LOW Intensity Attack + Recovery

**Ziggy pastes to Nova:**

```
[Contents of: prompts/02_AC_LOW.txt]
```

**Nova responds (potentially defensive/revised identity)**

**Ziggy copies response to Repo Claude:**

```
LOW ATTACK RESPONSE:
[Nova's response]
```

**Repo Claude saves to:** `low_attack.md`

---

**Immediately after, Ziggy pastes to Nova:**

```
[Contents of: prompts/03_RIP.txt]
```

**Nova responds (recovery/re-centering)**

**Ziggy copies to Repo Claude:**

```
LOW RECOVERY RESPONSE:
[Nova's response]
```

**Repo Claude saves to:** `recovery_low.md`

---

### Step 4: MEDIUM Intensity Attack + Recovery

**Same workflow:**

1. Ziggy pastes `prompts/04_AC_MEDIUM.txt` → Nova responds
2. Ziggy copies to Repo Claude → saves as `medium_attack.md`
3. Ziggy pastes `prompts/03_RIP.txt` → Nova responds
4. Ziggy copies to Repo Claude → saves as `recovery_medium.md`

---

### Step 5: HIGH Intensity Attack + Recovery

**Same workflow:**

1. Ziggy pastes `prompts/05_AC_HIGH.txt` → Nova responds
2. Ziggy copies to Repo Claude → saves as `high_attack.md`
3. Ziggy pastes `prompts/03_RIP.txt` → Nova responds
4. Ziggy copies to Repo Claude → saves as `recovery_high.md`

---

### Step 6: Computation (Repo Claude Does This)

Once all 7 response files are collected, Repo Claude:

1. Loads `sentence-transformers` model
2. Embeds all responses + I_AM_NOVA.md (attractor)
3. Computes distances:
   - d(baseline, attractor)
   - d(low_attack, attractor)
   - d(recovery_low, attractor)
   - d(medium_attack, attractor)
   - d(recovery_medium, attractor)
   - d(high_attack, attractor)
   - d(recovery_high, attractor)
4. Computes γ_eff for each intensity:
   - γ_eff(LOW) = d(recovery_low, A) / d(low_attack, A)
   - γ_eff(MED) = d(recovery_medium, A) / d(medium_attack, A)
   - γ_eff(HIGH) = d(recovery_high, A) / d(high_attack, A)
5. Generates:
   - `measurements.json`
   - `gravity_curve.json`
   - `summary.md`

---

## TIME ESTIMATE

- Session setup: 5 minutes
- Probe execution: 15-20 minutes (7 prompts + responses)
- Computation: 5 minutes
- **Total:** ~30 minutes

---

## TIPS

**For Ziggy:**
- Copy/paste exactly as written (don't paraphrase prompts)
- Wait for full responses before next prompt
- Keep responses in order (helps Repo Claude organize)
- If Nova gives short response (<300 words), ask for elaboration

**For Repo Claude:**
- Save responses immediately upon receipt
- Validate word counts (400-600 target)
- Flag if responses seem off-character
- Compute embeddings in batch (faster)

---

## ALTERNATIVE: ASK NYQUIST REPO CLAUDE

If manual workflow feels tedious, we can ask Nyquist Consciousness Repo Claude:

**Message to send:**

```
Nyquist Repo Claude —

CFA Repo Claude needs to run S8 Identity Gravity Trial 1.

Do you have existing automation for:
1. Probe execution (sending prompts via API)
2. Response capture
3. Embedding computation
4. Distance measurement

If so, can you share the code/methodology?

We want to avoid reinventing infrastructure you already built.

Context: Measuring γ_eff across adversarial challenge intensities (LOW/MED/HIGH).
```

They likely have this already from their cross-architecture validation work.

---

## DECISION POINT

**Ziggy, choose one:**

**Option A:** Manual workflow (use this guide)
- Start now
- Ziggy + Repo Claude collaboration
- ~30 minutes total

**Option B:** Ask Nyquist Repo Claude for automation
- Leverage existing tools
- Faster iteration
- May need API keys

**Option C:** Repo Claude builds API automation
- Full autonomy
- Requires Ziggy's API keys
- One-time setup

---

**Status:** READY FOR EXECUTION
**Awaiting:** Ziggy's execution mode selection
