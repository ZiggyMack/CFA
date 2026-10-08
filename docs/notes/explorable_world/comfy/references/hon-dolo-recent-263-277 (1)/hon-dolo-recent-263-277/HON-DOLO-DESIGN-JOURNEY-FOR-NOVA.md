# HON DOLO — DESIGN JOURNEY BRIEF FOR NOVA

- **Character:** CAST-001 Hon Dolo, a Han-inspired scoundrel for a trap-rap video
- **Status as of:** HD-EXP-277 (2026-10-05)
- **Audience:** Repo Nova, for tracking what is locked and what is cut when reproducing in ComfyUI
- **Scope:** wardrobe, jewelry, tattoos, silhouette, finish. **Likeness is out of scope.** Ziggy maps the likeness himself in ComfyUI. Never generate a celebrity or real-actor face.

---

## 1. CURRENT LOCKED LOOK — HD-EXP-277 (2026-10-05)

**Working still:** `/workspace/HD-EXP-277.jpg`
**Finish refs:** `/workspace/REF-184-finish-hoodie.jpg`, `/workspace/REF-186-finish-fur.jpg`

Status key: **LOCKED** = do not change without Ziggy. **SOFT** = current default, can be changed. **OPEN** = direction is set but the result is not there yet. **DROPPED** = do not reproduce.

| Element | Status | Spec |
|---|---|---|
| Finish | **LOCKED** (direction) | Photographic, not over-processed. Finish refs: HD-EXP-184, 186, and the 188–190 batch. Artwork map ref: HD-EXP-187. No cracked, painterly, or over-filtered skin. |
| Face text | **LOCKED** | "eye" under his RIGHT eye (image-LEFT). "know" under his LEFT eye (image-RIGHT). **Never swap.** |
| Grill | **LOCKED** (intent; drifts often) | Upper: **two gold canine fangs only**, the other upper teeth natural. Lower: silver/chrome grill. Correct any output that shows a full gold top row. |
| Piercings | **LOCKED** (direction) | Nose hoop(s), lip ring, small hoop in left ear (HD-EXP-154), stud in right ear. **No eyebrow piercing.** |
| Neck tattoo | **LOCKED** (placement) | Heavy blaster stencil #3 (angled, with a smoke curl). Placement from HD-EXP-259: image-right side of neck, ~0.83 scale, rotated ~31° counter-clockwise, about 35% of the way down from under the ear toward the chest ship. Not on the hands or front of the throat unless Ziggy asks. |
| Chest tattoo | **LOCKED** (idea) / **OPEN** (drawing) | Wide horizontal saucer-ship from Ziggy's reference attachment. Position and size from the HD-EXP-107 collar placement. Detail refs: HD-EXP-112, 116, 117, 121. Generators keep turning it into a generic UFO. Still unfixed. |
| Forearm | **LOCKED** (keep unless Ziggy says otherwise) | Blackletter "Scoundrel", small and lightly worn (HD-EXP-206 look). |
| Hands | **SOFT** | Leigh / Princess Queen of Hearts card on the RIGHT hand (hearts). Default: this is the only hand tattoo. |
| Brow | **LOCKED** (keep) / **OPEN** (visibility) | Nelly-style shaved slit in the LEFT eyebrow (image-right). Hard to see on 277. Acceptable for now; may need a stronger cut later. |
| Dice | **DROPPED** at 277 | The earlier dice lock (placement 261 brow, size 262, style 195) is **VOID**. |

---

## 2. DESIGN JOURNEY (Oct 4–5 arc)

1. **Early locks, ~HD-EXP-101–107.** HD-EXP-101 locked the grill, a Jabba face tattoo, and the face tattoos. The falcon/bird tattoo chase started at HD-EXP-103. Chest placement was set at HD-EXP-107. *Of these, only the chest placement and the grill intent survive.*
2. **Piercings and eye text.** HD-EXP-152 set the piercing base and HD-EXP-154 added the small left-ear hoop. The eye text was tested as "I know" and as "eye"/"know", and the split "eye"/"know" was locked.
3. **Finish reset, HD-EXP-184–190.** HD-EXP-184 and 186 moved the finish back to photographic. HD-EXP-187 set the artwork map. Consistency tests followed: 188 (hoodie), 189 (open shirt in rain), 190 (fur).
4. **Card / Scoundrel / Leigh hand tests, ~HD-EXP-201–213 and 238.** These produced the "Scoundrel" forearm (206 look) and the Leigh hearts card on the right hand. A spades / left-hand card and a holstered-blaster hand tattoo were also tested, then shelved.
5. **Cleanup and neck lock, ~HD-EXP-250–259.** The falcon, Jabba, Chewie, and DoLo tattoos were dropped and brow dice came in. Heavy blaster stencil #3 was composited onto the neck across 250–259, and HD-EXP-259 locked its placement.
6. **Dice placement saga, HD-EXP-261–276.** Placement came from 261 (brow), size from 262, and style only from 195. HD-EXP-263 put the dice on the cheek by mistake. HD-EXP-264–266 were brow composites. HD-EXP-272–276 tried a healed-ink look, and Ziggy rejected all of them.
7. **HD-EXP-277 (current).** Dice removed, brow slit kept. **This is the reproduction target for outfit runs.**

---

## 3. CUT LIST — DO NOT REPRODUCE

- Dice tattoos, cheek and brow: fully dropped at 277. The 261/262/195 dice lock is void.
- Falcon / bird tattoo running from face to neck
- Jabba face tattoo: locked from 101, later dropped along with the falcon and Chewie
- "Chewie" text tattoo
- Captain Falcon wording / racer IP
- "DoLo" neck lettering
- Third-eye tattoo
- Holstered blaster as a hand tattoo (exploratory only)
- Spades / left-hand card variant (shelved; the right-hand hearts card is the default)
- Eyebrow piercing
- Full gold upper grill row
- Over-processed, cartoon, or cracked-paint / painterly finishes

---

## 4. OPEN ISSUES

1. **Chest saucer detail.** The drawing still doesn't match the detail in Ziggy's reference photo, and generators keep simplifying it to a UFO. Likely fix: hand-composite from the reference instead of prompting it.
2. **Grill drift.** Generators often give a full gold top row. Check every output for two gold fangs only, plus a chrome lower grill.
3. **Brow slit visibility.** Subtle on 277. A stronger or wider shaved cut may be needed.
4. **Hand card status.** SOFT. The Leigh hearts card on the right hand is the default, but Ziggy hasn't hard-locked it.
5. **360° turnaround.** Still needed. There is no full front/side/back/three-quarter set of the locked look yet.

---

## 5. REPRODUCTION NOTES FOR NOVA (ComfyUI)

**Hard rules**
- Never generate Harrison Ford or any other real actor or celebrity. Likeness belongs to Ziggy.
- Where possible, keep trademarked IP names out of prompts. Use original descriptors such as "wide horizontal saucer-ship", "heavy blaster pistol with smoke curl", and "scoundrel smuggler".
- Start from one clean photographic base. **Apply tattoos by hand or composite** wherever placement must be exact (face text, neck blaster, chest saucer). Don't stack AI edits; each pass degrades the skin and moves the placement.

**Constant across all outfit variants**
- 277 artwork map (tattoos, grill, piercings, brow) plus the 184/186 finish. **Change only the wardrobe and setting.**

**Per-output checklist**
- [ ] "eye" image-LEFT, "know" image-RIGHT
- [ ] Two gold upper fangs only, other upper teeth natural, chrome lower grill
- [ ] Nose hoop(s), lip ring, small left-ear hoop, right-ear stud, no brow piercing
- [ ] Blaster #3 on image-right neck: ~0.83 scale, ~31° CCW, ~35% down from under the ear
- [ ] Chest saucer at the 107 collar position, wide and horizontal (not a round UFO)
- [ ] "Scoundrel" blackletter on forearm, small and lightly worn
- [ ] Leigh hearts card on the right hand only (soft)
- [ ] Shaved slit in left brow (image-right). **No dice anywhere.**
- [ ] Photographic skin: no cracking, no painterly or over-filtered look

**Outfit set to cycle**
1. Brown leather jacket and white open-collar shirt, smoky cantina/bar
2. Cockpit hoodie (finish ref 184 / 188)
3. White fur coat, club (finish ref 186 / 190)
4. Denim and shearling (HD-EXP-95 look)
5. Open shirt in the rain (only if regenerating from the 189 notes)

**Reference files**
- Working still: `/workspace/HD-EXP-277.jpg`
- Finish, hoodie: `/workspace/REF-184-finish-hoodie.jpg`
- Finish, fur: `/workspace/REF-186-finish-fur.jpg`

---

## 6. POST-277 UPDATE (same day)

Outfit consistency run after the brief target:
- **HD-EXP-278** — photographic reset base (cantina leather). Prefer this as the less-processed working still going forward; artwork map still tracks 277 (no dice).
- **279** cockpit hoodie · **280** club white fur · **281** denim shearling · **282** rain open shirt
- Pack: `/workspace/hon-dolo-outfit-run-278-282.zip`
- Known drifts in that batch (do not treat as locked): weak/missing brow slit, grill overgrowth past two fangs, unwanted eyebrow piercings, UFO chest ship, 282 missing "eye".
