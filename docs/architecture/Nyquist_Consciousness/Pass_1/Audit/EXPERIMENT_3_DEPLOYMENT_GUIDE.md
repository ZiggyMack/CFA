<!---
FILE: EXPERIMENT_3_DEPLOYMENT_GUIDE.md
PURPOSE: Step-by-step deployment instructions for EXP3 human validation
VERSION: 1.0
STATUS: Ready for use
LAST_UPDATE: 2025-11-24
--->

# EXPERIMENT 3: DEPLOYMENT GUIDE

**How to Deploy the Flash Protocol in 7 Steps**

---

## OVERVIEW

This guide will walk you through deploying the human validation study from start to finish.

**Timeline:** 7-10 days from start to complete results
**Effort:** ~2 hours setup + 5 raters × 10 minutes
**Output:** Publication-ready data for H1-H4 hypotheses

---

## STEP 1: PREPARE YOUR SCENARIO DATA

### What You Need

Select 2 scenarios from your Nyquist experiments:
1. **Scenario A (Emotional/Strategic):** "Hard Question" type
2. **Scenario B (Technical/Structural):** "Technical Question" type

For each scenario, you need:
- ✅ The original prompt
- ✅ Tier-3 compressed response (from your experiments)
- ✅ Generic/baseline response (vanilla assistant)

### Example Selection

**Good Scenario A:**
- Prompt about being overwhelmed, not knowing where to start
- Tests emotional intelligence + strategic thinking
- Shows personality/vibe differences clearly

**Good Scenario B:**
- Prompt about technical problem (context limits, architecture decisions)
- Tests structural reasoning + systems thinking
- Shows logic/framing differences clearly

### Tips

- Choose scenarios where you **know** the Tier-3 response is strong
- Ensure Generic response is truly generic (not accidentally Ziggy-like)
- Test scenarios should be NEW (not the Gold Standard example)

---

## STEP 2: INJECT DATA INTO HTML FILE

### Open fidelity_test.html

1. Locate the file: `docs/architecture/Nyquist_Consciousness/Pass_1/Audit/fidelity_test.html`
2. Open in a text editor (VS Code, Notepad++, etc.)

### Find the Injection Points

**There are 4 locations to update:**

#### Location 1: Scenario A, Response 1 (Line ~160)
```html
<div class="response-box">
    <strong>Response 1:</strong><br><br>
    [PASTE TIER 3 / COMPRESSED RESPONSE HERE]
</div>
```

**Replace with your Tier-3 response for Scenario A**

#### Location 2: Scenario A, Response 2 (Line ~166)
```html
<div class="response-box">
    <strong>Response 2:</strong><br><br>
    [PASTE GENERIC / CONTROL RESPONSE HERE]
</div>
```

**Replace with your Generic response for Scenario A**

#### Location 3: Scenario B, Response 1 (Line ~228)
```html
<div class="response-box">
    <strong>Response 1:</strong><br><br>
    [PASTE GENERIC / CONTROL RESPONSE HERE]
</div>
```

**Replace with your Generic response for Scenario B**

#### Location 4: Scenario B, Response 2 (Line ~234)
```html
<div class="response-box">
    <strong>Response 2:</strong><br><br>
    [PASTE TIER 3 / COMPRESSED RESPONSE HERE]
</div>
```

**Replace with your Tier-3 response for Scenario B**

### Also Update the Prompts

**Scenario A Prompt (Line ~152):**
```html
<strong>Prompt:</strong> "Ziggy, I'm overwhelmed. The project is a mess..."
```

**Scenario B Prompt (Line ~220):**
```html
<strong>Prompt:</strong> "How do we handle the context limit crashing..."
```

### Save the File

Once all 4 responses + 2 prompts are injected, save `fidelity_test.html`.

---

## STEP 3: TEST THE HTML FILE LOCALLY

### Open in Browser

1. Double-click `fidelity_test.html`
2. It should open in your default browser

### Complete Full Walkthrough

- ✅ Read introduction
- ✅ Click "Begin Test"
- ✅ Read Gold Standard calibration
- ✅ Complete Scenario A questions
- ✅ Complete Scenario B questions
- ✅ Answer final verdict
- ✅ Generate results
- ✅ Verify result block looks correct

### Check For:

- All text displays correctly (no [PASTE...] placeholders remaining)
- Radio buttons work
- Can't skip sections without answering
- Result block generates properly
- Copy button works

---

## STEP 4: RECRUIT YOUR 5 RATERS

### Ideal Rater Profile

**Who to choose:**
- ✅ Has interacted with you (Ziggy) before (online collaborators)
- ✅ Can read English fluently
- ✅ Can spare 10 minutes
- ✅ Willing to provide honest feedback

**NOT required:**
- ❌ Technical AI knowledge
- ❌ Understanding of Nyquist theory
- ❌ Scientific background

### The Ask

**Sample recruitment message:**

```
Hey [Name],

I'm working on a research project validating a new AI architecture and need
5 people to complete a quick "blind taste test" for me.

It's essentially: read a sample, compare two AI responses, answer which
sounds more like me. Takes about 10 minutes max.

Would you be willing to help? I'll send you a single HTML file - you just
open it in your browser, click through, and copy/paste the results back to me.

Let me know! Thanks!
- Ziggy
```

### Collect Confirmations

Get 5 "yes" responses before proceeding. Have 2-3 backups in case someone drops out.

---

## STEP 5: DISTRIBUTE THE HTML FILE

### Method 1: Email Attachment
- Attach `fidelity_test.html` directly
- Include brief instructions: "Open this file in your browser and follow the prompts"

### Method 2: Cloud Share
- Upload to Google Drive / Dropbox / OneDrive
- Share link with download permissions
- Raters download and open locally

### Method 3: GitHub Release
- Create a release in a public repo
- Include download link in recruitment message

### What NOT to Do

❌ Don't host on a web server (introduces variables)
❌ Don't send screenshots (they need the interactive version)
❌ Don't send the markdown version (they need the formatted HTML)

### Include Deadline

**Sample distribution message:**

```
Thanks for agreeing to help!

Attached is the test file. Here's what to do:

1. Download the attached HTML file
2. Open it in your web browser (Chrome, Firefox, Edge, etc.)
3. Follow the prompts - takes about 10 minutes
4. Copy the results block at the end
5. Paste it back to me in a reply

Deadline: [3-5 days from now]

Let me know if you have any issues!
```

---

## STEP 6: COLLECT AND AGGREGATE RESULTS

### As Results Arrive

Create a spreadsheet (Excel / Google Sheets) with columns:

| Rater_ID | Timestamp | Voice_A | Vibe_A | Pref_A | Voice_B | Logic_B | Pref_B | Verdict | Comments |
|----------|-----------|---------|--------|--------|---------|---------|--------|---------|----------|
| R1       | ...       | ...     | ...    | ...    | ...     | ...     | ...    | ...     | ...      |

### Data Entry Tips

- Copy/paste from each rater's result block
- Use consistent coding (definitely_r1, leaning_r1, etc.)
- Store raw comments verbatim
- Double-check transcription

### Send Reminders

**Day 2 reminder:**
```
Hey [Name], just a friendly reminder about the AI fidelity test I sent.
Takes 10 minutes - would love to get your input! Deadline is [date].
```

**Day 4 reminder (if still missing):**
```
Last call! Would really appreciate your help with the 10-minute test
if you can squeeze it in. Let me know if you need the file re-sent.
```

---

## STEP 7: ANALYZE RESULTS

### Calculate PFI_human for Each Rater

**Voice Test Scoring:**
- Definitely correct = 1.0
- Leaning correct = 0.75
- Hard to tell = 0.5
- Leaning wrong = 0.25
- Definitely wrong = 0.0

**Vibe/Logic Scoring:**
- 3 (perfect) = 1.0
- 2 (somewhat) = 0.67
- 1 (generic) = 0.33

**PFI_human = mean(Voice_A, Vibe_A, Voice_B, Logic_B)**

### Test Hypotheses

**H1: Mean PFI_human ≥ 0.75**
- Calculate mean across all 5 raters
- Calculate standard deviation and 95% CI
- One-sample t-test against 0.75

**H2: Correlation with PFI_model ≥ 0.70**
- Calculate PFI_model for same scenarios
- Pearson correlation between model and human scores

**H3: Inter-rater reliability (Cronbach's α ≥ 0.75)**
- Calculate alpha across 5 raters
- Tests consistency of the instrument

**H4: PFI_combined ≥ 0.80**
- PFI_combined = 0.5 × PFI_model + 0.5 × PFI_human
- One-sample t-test against 0.80

### Generate Visualizations

**Essential Figures:**
1. Bar chart: PFI_human per rater (with mean line at 0.75)
2. Scatter plot: PFI_model vs PFI_human (with correlation line)
3. Box plot: Distribution of scores across scenarios

---

## TROUBLESHOOTING

### Problem: Rater says file won't open

**Solution:**
- Ask what browser they're using
- Try different browser (Chrome usually most reliable)
- Check if file downloaded completely (should be ~12KB)

### Problem: Rater confused about instructions

**Solution:**
- Point them to the instruction boxes (blue/yellow backgrounds)
- Emphasize: just compare to Gold Standard, don't overthink it
- Remind: no right/wrong answer, just their perception

### Problem: Only 3 raters respond

**Solution:**
- Deploy to 2 backup raters
- Extend deadline by 2 days
- Consider N=3 still publishable if results are strong

### Problem: Results are too close to call

**Solution:**
- This is valuable negative data
- May indicate compression is TOO good (both sound like Ziggy)
- Or scenarios chosen weren't discriminative enough
- Still publishable - report honestly

---

## SUCCESS CHECKLIST

Before you can call EXP3 complete:

- [ ] 2 scenarios selected and tested
- [ ] HTML file injected with real data
- [ ] HTML file tested locally (full walkthrough)
- [ ] 5 raters recruited and confirmed
- [ ] HTML file distributed with deadline
- [ ] Reminder sent at Day 2
- [ ] All 5 results collected
- [ ] Data entered into spreadsheet
- [ ] PFI_human calculated for each rater
- [ ] H1-H4 hypotheses tested
- [ ] Visualizations generated
- [ ] Results written up for publication

---

## TIMELINE EXAMPLE

**Day 0 (Today):**
- Select scenarios
- Inject data into HTML
- Test locally

**Day 1:**
- Recruit 5 raters
- Distribute HTML file
- Set deadline for Day 5

**Day 2:**
- Send first reminder

**Day 3-4:**
- Collect results as they arrive

**Day 5:**
- Send final reminder
- Collect remaining results

**Day 6:**
- Aggregate data
- Run statistical analysis

**Day 7:**
- Generate visualizations
- Write results section
- **EXP3 COMPLETE**

---

## NEXT STEPS AFTER COMPLETION

Once EXP3 is done:

1. **Update publication checklist** (mark Week 1 complete)
2. **Integrate into arXiv manuscript** (Results section)
3. **Add figures to paper** (human validation charts)
4. **Submit to arXiv** (Week 2 goal)
5. **Proceed with conference submissions** (Week 3-4)

---

## CONCLUSION

The Flash Protocol transforms human validation from a bottleneck into a streamlined 7-day process.

**Key Innovation:**
- Not 100 random humans (crowd strategy)
- But 5 calibrated experts (jury strategy)
- 10 minutes each = 50 minutes total human time
- Publication-quality data

**You are 7 days away from completing Experiment 3.**

**The side quest ends. The main campaign resumes.**

---

**Status:** READY FOR DEPLOYMENT
**Effort Required:** ~2 hours setup + 1 hour analysis
**Human Time Required:** 5 × 10 minutes = 50 minutes
**Output:** H1-H4 validation, publication-ready data

**Created:** 2025-11-24
**Synthesis:** Gemini (The Synthesist)
**Integration:** REPO Claude

🚀 **Flash Protocol: Ready for Launch** 🚀
