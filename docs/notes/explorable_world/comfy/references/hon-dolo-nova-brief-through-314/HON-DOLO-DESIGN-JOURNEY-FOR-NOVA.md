# HON DOLO — DESIGN JOURNEY BRIEF FOR NOVA

- **Character:** CAST-001 Hon Dolo, a Han-inspired scoundrel for a trap-rap video
- **Status as of:** 2026-10-06 (covers through HD-EXP-314 walk pack)
- **Audience:** Repo Nova, for tracking what is locked and what is cut when reproducing in ComfyUI
- **Scope:** wardrobe, jewelry, tattoos, silhouette, finish, pose/walk scaffolds. **Likeness is out of scope.** Ziggy maps the likeness himself in ComfyUI. Never generate a celebrity or real-actor face.

---

## 1. CURRENT GROUND TRUTH (supersedes older stills)

| Priority | File | Role |
|---|---|---|
| **#1 IDENTITY** | `/workspace/HD-EXP-LOCK-FACE.jpg` | Ziggy attachment. Face/design lock. Compare every new still to this before accepting. Closest prior still ≈ HD-EXP-277. |
| Soft polish | `/workspace/HD-EXP-289.jpg` | In-place polish of LOCK-FACE (same pixels, mild photo finish). Safe only when regen dumps the design. |
| Artwork map (older) | HD-EXP-277 | Still useful for "no dice + brow slit" map, but **LOCK-FACE wins** on conflict. |
| Finish direction | HD-EXP-184, 186, 188–190 | Photographic, not over-processed. |

**Critical rule Ziggy enforced after failed resets:** do **not** dump the locked design to chase photorealism. Photoreal attempts that change the face, piercings, grill, or tattoos are failures even if they look "more photo."

Status key: **LOCKED** = do not change without Ziggy. **SOFT** = current default. **OPEN** = direction set, result not there. **DROPPED** = do not reproduce. **SCAFFOLD** = wardrobe/pose only; not identity.

| Element | Status | Spec |
|---|---|---|
| Finish | **LOCKED** (direction) | Photographic, less-processed. Refs 184/186/188–190. No cracked, painterly, or over-filtered skin. |
| Face text | **LOCKED** | "eye" under his RIGHT eye (image-LEFT). "know" under his LEFT eye (image-RIGHT). **Never swap.** |
| Grill | **LOCKED** | Upper: **two gold canine caps only**, other uppers natural. Length: **slightly longer than normal human K9s** (subtle street-grill). **Not** vampire/saber fangs past the lip. Lower: silver/chrome grill. Reject full gold top row and vampire fangs. |
| Piercings | **LOCKED** | Nose hoop(s), two lip rings, ear hoop/studs. **No eyebrow piercings.** Do not drop any of these. |
| Brow | **LOCKED** / **OPEN** (visibility) | Nelly-style shaved slit in LEFT eyebrow (image-right). Keep even if subtle. No dice. |
| Neck tattoo | **LOCKED** (placement) | Heavy blaster (stencil #3 direction, smoke curl). Image-RIGHT neck only. Placement heritage HD-EXP-259. **Not** a ship on the neck. |
| Chest tattoo | **LOCKED** (idea) / **OPEN** (drawing) | Saucer/ship at open collar (107 position/scale). Detail refs 112/116/117/121. Generators still simplify to UFO. |
| Forearm | **LOCKED** (keep unless told) | Blackletter "Scoundrel", small, lightly worn (206 look). |
| Hands | **SOFT** | Leigh / Princess Queen of Hearts on RIGHT hand only (default). |
| Dice | **DROPPED** | Fully void as of 277 / LOCK-FACE. |
| Motion | **SCAFFOLD** | Walk stills 306–311 usable-ish; clips are keyframe/morph only (see §8). |

---

## 2. DESIGN JOURNEY (Oct 4–5 arc) — condensed

1. **Early locks ~101–107.** Grill + Jabba + falcon chase; chest placement 107. Only chest placement + grill intent survive.
2. **Piercings + eye text.** 152/154 piercings; "eye"/"know" locked (never swap).
3. **Finish reset 184–190.** Photographic finish; 187 artwork map; hoodie/fur/rain tests.
4. **Card / Scoundrel ~201–213, 238.** Forearm Scoundrel (206); Leigh hearts right hand. Spades left / holster hand blaster shelved.
5. **Cleanup + neck ~250–259.** Falcon, Jabba, Chewie, DoLo dropped; brow dice in then later out. Neck blaster placement locked at 259.
6. **Dice saga 261–276.** Placement 261, size 262, style 195. Ziggy rejected healed-ink attempts; **dice dropped at 277**.
7. **277.** No dice, brow slit kept. Was interim reproduction target until LOCK-FACE.

---

## 3. GAP UPDATE — what happened after the previous Nova brief (through walk pack)

### 3a. Photoreal dump failure (do not use as identity)

After 277, free-regen "photographic resets" **HD-EXP-278–287** and remasters **288/290** often **dumped** the locked dude: wrong face, vampire or full-gold grill, lost piercings, ship on neck, wrong tattoos. Ziggy: do not trade the locked look for photoreal.

- **289** = honest path when regen fails: polish LOCK-FACE in place.
- Treat **278–282 outfit zip** as wardrobe experiments with known drift, not face lock.
- Pack (historical): `/workspace/hon-dolo-outfit-run-278-282.zip`

### 3b. LOCK-FACE + turnaround outfits (291–305)

Ziggy locked **HD-EXP-LOCK-FACE.jpg** as face/design ground truth (also agent attachment `ef5d59a6…`).

Outfit × front/side/back cycle (cantina leather → hoodie → white fur → denim shearling → rain open shirt):

| Range | Look |
|---|---|
| 291–293 | Cantina leather |
| 294–296 | Cockpit hoodie |
| 297–299 | Club white fur |
| 300–302 | Denim shearling |
| 303–305 | Rain open shirt |

Pack: `/workspace/hon-dolo-lock-turnaround-outfits.zip`

**QA:** Fronts roughly usable (291, 294, 297, 300, 303). Sides/backs often drift (grill, piercings, mashed eye/know, fake backs, invented props). **Scaffolding only — never replace LOCK-FACE for identity.**

### 3c. Walk templates (306–314) + motion honesty

Ziggy asked for walking templates + multiple perspectives.

| # | Angle | Phase | QA |
|---|---|---|---|
| 306 | front | contact | usable-ish |
| 307 | front | mid | usable-ish |
| 308 | front | push-off | usable-ish |
| 309 | side | contact | usable-ish |
| 310 | side | mid | usable-ish |
| 311 | side | push-off | usable-ish |
| 312 | 3/4 | contact | **drifted** (wrong body scale) |
| 313 | 3/4 | mid | **drifted** (prop blaster in hand) |
| 314 | 3/4 | push-off | **drifted** (look-back / extras) |

Pack: `/workspace/hon-dolo-walk-pack.zip`  
Also: `/workspace/hon-dolo-walk-pack/` (stills, contact sheet, clips, README)

**Clips (honest):** Grok Bot has no true AI video generator here. Delivered:
- `HD-EXP-WALK-CLIP-keyframe-loop.mp4` — stepped still loop (front then side)
- `HD-EXP-WALK-CLIP-morph.mp4` — motion-interpolated morph between those stills

**Comfy path for real walk:** IP-Adapter (or equivalent) on **LOCK-FACE** + pose refs from **306–311** into AnimateDiff / SVD (or Nova's preferred motion stack). Do not treat the mp4s as locked character motion.

Outfit on walk sheet: cantina black leather + open white shirt (291 direction).

### 3d. Pending from Ziggy (as of last ask)

Offer on table: remaster **only 306–311** tighter to LOCK-FACE before cycling walks through other outfits. Not confirmed yet.

---

## 4. CUT LIST — DO NOT REPRODUCE

- Dice tattoos (cheek/brow); 261/262/195 dice lock **VOID**
- Falcon / bird face→neck tattoo
- Jabba face tattoo
- "Chewie" text
- Captain Falcon wording / racer IP
- "DoLo" neck lettering
- Third-eye tattoo
- Holstered blaster as hand tattoo
- Spades / left-hand card (shelved)
- Eyebrow piercings
- Full gold upper grill row
- Vampire / saber fangs past the lip
- Ship tattoo on the **neck** (blaster only there; ship is **chest**)
- Over-processed / cartoon / cracked-paint finishes
- Treating 278–290 dumped photoreal resets or 291–305 / 312–314 scaffolds as identity lock

---

## 5. OPEN ISSUES

1. **Chest saucer detail** vs Ziggy's photo; generators → UFO. Prefer composite.
2. **Grill length** — street-subtle K9s; still drifts to vampire or full gold.
3. **Brow slit visibility** — keep; may need stronger cut later.
4. **Hand card** — SOFT (Leigh hearts right hand).
5. **360° consistency** — turnaround pack exists but sides/backs drift; true multi-angle lock needs Comfy IP-Adapter on LOCK-FACE, not free regen.
6. **Walk consistency** — 306–311 scaffolds only; remaster + Comfy motion still open.
7. **Outfit walk sheets** — not done yet for hoodie / fur / denim / rain.

---

## 6. REPRODUCTION NOTES FOR NOVA (ComfyUI)

**Hard rules**
- Never generate Harrison Ford or any real actor/celebrity. Likeness = Ziggy.
- Keep trademarked IP names out of prompts where possible. Prefer "wide horizontal saucer-ship", "heavy blaster pistol with smoke curl", "scoundrel smuggler".
- **Identity ref = LOCK-FACE.** Change wardrobe/setting/pose only.
- Apply face text, neck blaster, chest saucer by composite when placement must be exact. Don't stack AI edits.
- Reject any "more photoreal" pass that changes the locked design.

**Per-output checklist**
- [ ] Matches LOCK-FACE face geometry / piercings / tattoos intent
- [ ] "eye" image-LEFT, "know" image-RIGHT
- [ ] Two gold upper K9s only, **slightly** longer than normal (not vampire); silver lower; other uppers natural
- [ ] Nose hoop(s), lip rings, ear jewelry; **no** brow piercing
- [ ] Blaster on image-right neck only (not ship on neck)
- [ ] Chest saucer at collar (107), wide/horizontal (not round UFO)
- [ ] Scoundrel forearm (soft-keep); Leigh hearts right hand (soft)
- [ ] Left brow Nelly slit; **no dice**
- [ ] Photographic skin, not over-processed

**Outfit cycle (wardrobe only)**
1. Cantina leather + open white shirt
2. Cockpit hoodie (184 / 188)
3. Club white fur (186 / 190)
4. Denim shearling (95 look)
5. Rain open shirt (189 direction)

**Reference packs**
- Lock face: `/workspace/HD-EXP-LOCK-FACE.jpg`
- Recent stills zip (263–277 era): `/workspace/hon-dolo-recent-263-277.zip`
- Outfit run 278–282 (drifted): `/workspace/hon-dolo-outfit-run-278-282.zip`
- Turnaround 291–305: `/workspace/hon-dolo-lock-turnaround-outfits.zip`
- Walk 306–314 + clips: `/workspace/hon-dolo-walk-pack.zip`

---

## 7. ONE-LINE FOR NOVA

**Identity = LOCK-FACE. 291–305 = outfit/angle scaffolds. 306–311 = walk pose scaffolds. Clips = still morphs, not locked AI video. Reproduce in Comfy with IP-Adapter on LOCK-FACE; never dump the design for photoreal.**
