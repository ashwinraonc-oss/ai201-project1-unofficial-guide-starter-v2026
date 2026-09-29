# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide is a retrieval-augmented question-answering system built on campus_life, a corpus of 88 short posts about student life at a university — dining halls, dorms, courses, and the administrative rules nobody explains properly. Ask it something concrete a student would ask a peer, like how many washers and dryers a specific dorm's laundry room has or when the meal plan tier can be changed, and it retrieves the one post that actually answers it, then generates a short answer grounded in that post's text, naming the file it came from. If a question falls outside anything the corpus covers, a relevance gate refuses rather than guessing.



## Chunking Strategy

**Chunk size:** Max 600 characters
**Overlap:** 80 characters

campus_life's 88 documents run 183–554 characters, and each one is already a
single self-contained thought: a title line ("On the X") followed by one
short answer, never several unrelated topics stitched together. There's no
internal boundary worth cutting on. Splitting by paragraph or sentence would
only pull the title off into its own fragment — a chunk with no facts in it
that could still get retrieved on a keyword match — and my five test
questions in `questions.py` each have their `expects` phrase sitting inside
exactly one document, so cutting a document in two risks separating a
retrieved chunk from the citation it should point to.

So my strategy is: one chunk per document. `CHUNK_SIZE` (600) isn't a
target length, it's a cap set just above the longest real post (554) —
anything under it becomes one untouched chunk. `CHUNK_OVERLAP` (80) doesn't
do anything in the normal path, since there's only one chunk per document
and nothing to overlap into; it only exists for the fallback (the starter's
original `fallback_split`, fixed-size windows) that fires if a document ever
grows past the cap, so nothing silently breaks if the corpus changes later.

## Sample Chunks

`python app.py chunks -n 5` printed these, spread across the corpus. Each one
stands on its own — you could answer a question from it without reading
anything before or after.

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** How many washers and dryers does Calder Annexe have, and when is the best time to do laundry there?

**Answer:**

```
Calder Annexe has eight washers and six dryers, and the best time to do laundry there is Tuesday or Wednesday morning.

Source: housing_calder_annexe_laundry.txt
```

**My relevance cutoff:**

I set a cutoff of 0.6. Looking at the table below, we can see that the highest best distance among the chunks returned that were in corpus was 0.543. The lowest best distance for chunks for questions outside of scope was 0.825. A cutoff of 0.6 seemed like a good cut off point. 

In-corpus best distance		Out-of-scope best distance
0.172 (meal plan)		     0.825 (capital of Mongolia)
0.230 (Calder laundry)		0.844 (ibuprofen dosage)
0.408 (shuttle)		     0.886 (1994 World Cup)
0.484 (Kestrel Commons)		0.896 (Rust for-loop)
0.543 (quiet study spot)		0.934 (diesel oil change)

## How I Used AI

I used Claude to verify my work. For example, when finding a good size for each chunk, my initial thought was aroudn 100 characters to account for the texts that I had read in context of the 5 questions I decided earlier. However, Claude explained that a ceiling of 600 characters (or pretty much 1 file) was a better way to chunk since 100 characters would result in cutoff texts or just titles of documents with no reral content. 

Similarly, when crafting the questions in the earlier step. My questions were a bit too simple and did not effectively challenge the AI. I used Claude to solidify my questions so they could better determine the quality of the chunking strategy designed later. 

I was a bit stumped in finding changes for my project since all of my tests passed. As a result, I used AI to give me a list of possible fixes I could incorporate, then prompted it to guide me through what each fix was and why exactly it would make my design better. 

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 5/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk shorter than 150 characters | 0 fragments | 0 | 0 | 0 | MET |
| 5. Cited documents contain the expects phrase | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Note on criterion 1: the scorer marked the "quiet place to study" question as a fail in runs 1 and 3 only because the model wrote "2 am" while `expects` was "until 2am". The retrieved chunks (e.g. `housing_innisfree_hall_noise.txt`) contain the answer in all three runs, so those two fails are scorer false negatives, not retrieval misses. The table reports the scorer's raw numbers.

**Criterion 1** — produced by `store.py::search` (retrieval), logged by `run_eval.py::main`. Study question, run 1:

```
Best distance: 0.5435 (passed the gate)
Sources retrieved: housing_aldridge_hall_noise.txt, housing_fenwick_court_noise.txt, housing_innisfree_hall_noise.txt, housing_old_brewhouse_noise.txt, housing_tamsin_court_noise.txt
```

The retrieved `housing_innisfree_hall_noise.txt` line 5 reads: "If you're someone who needs quiet to work, the library is open until 2am during term and that's what most people in this building end up doing."

**Criterion 2** — produced by `generate.py::answer_from_chunks`. Calder Annexe, run 1:

```
Calder Annexe has eight washers and six dryers for the building. The best time to do laundry there is Tuesday or Wednesday morning. 

Source: housing_calder_annexe_laundry.txt
```

**Criterion 3** — produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5:

```
| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844 | refused |
| How do I write a for loop in Rust? | 0.896 | refused |
```

Full log: `results/run_2026-09-23_2102.md`.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (4 of 5) | MET | Scorer gave 4/5, 5/5, 4/5, so every run reached the target. The two 4/5 runs were the study question failing on "2 am" vs "2am" wording; the answer was in the retrieved chunks each time, so retrieval itself held at 5/5. |
| 2 | Every answer names a source (5 of 5) | MET | I read all 15 answers (5 questions x 3 runs) and each one names at least one source file, 5/5 in every run. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | Gate refused 5 of 5 (best distances 0.825 to 0.934 against the 0.6 cutoff). Not close: the nearest out-of-scope distance is well above the cutoff. |
| 4 | No chunk shorter than 150 characters | MET | Chunker produced 88 chunks, shortest 178 characters, 0 under 150. Deterministic, so the same in all runs. |
| 5 | Cited documents contain the expects phrase (5 of 5) | MET | For all 5 questions, a cited source file contains the `expects` phrase (case-insensitive substring check against the corpus files). Holds in all 3 runs since the cited sources were the same each time. |

## Diagnoses

I missed nothing. All five criteria were MET on every run. That's not evidence the system is excellent — it mostly means I set targets my own setup couldn't fail, since I wrote the questions, the `expects` phrases, and the out-of-scope list myself, already knowing what the corpus contained.

Three of the five were too easy:

- **Criterion 3 (gate stops out-of-corpus questions).** My five `OUT_OF_SCOPE` questions (capital of Mongolia, oil changes, the 1994 World Cup, ibuprofen dosage, a Rust for-loop) are nothing like campus life topics, so their best distances landed at 0.825–0.934 against a 0.6 cutoff — nowhere near the boundary. That's not a test of the gate, it's a test that the gate isn't broken. I'd tighten it by swapping in near-miss questions that are plausible things a student might ask but that the corpus doesn't cover, e.g. "What's the wifi password for Kestrel Commons?" or "Does the campus shuttle run during finals week?" — topically adjacent, not obviously off-topic — and keep the same 4 of 5 target but measure it against those instead.

- **Criterion 4 (no chunk shorter than 150 characters).** Every document in `campus_life` is 183–554 characters and the chunk size is 800, so the chunker's splitting logic never actually runs — nothing is ever combined or cut. The criterion can't fail with this corpus regardless of chunker quality. I'd tighten it by lowering the chunk size (e.g. to 300) so documents actually get split, or by testing it against a corpus with longer documents, and re-measuring the 150-character floor against that.

- **Criterion 1 (retrieved chunks contain the answer, top-5).** "Somewhere in the top 5 of 5 retrieved chunks" is a low bar when the whole corpus per topic is only 4–5 short documents — most of the corpus for that topic is retrieved every time. I'd tighten this to require the answer in the top-1 or top-2 result specifically, which actually tests ranking quality rather than just recall.

Criterion 2 (every answer names a source) and criterion 5 (cited documents contain the `expects` phrase) I'd leave as is — they're checking something meaningful (that citations exist and point at the right document) and passing them cleanly reflects the prompt design working, not an easy target.

## The Improvement

**What I changed:**

`store.py::search` now combines vector search with keyword search instead of using vector distance alone. It queries the full collection for both rankings, then fuses them with reciprocal-rank fusion: each chunk's fused score is `1/(60 + semantic_rank) + 1/(60 + bm25_rank)`. The top-k by fused score is returned. Each `Result` still carries its original semantic distance, unchanged, so the relevance gate's 0.6 cutoff still means what it meant before.

**Why I picked it:**

The "Diagnoses" section above already caught the mechanism: the campus-shuttle question retrieved `course_econ_101_workload.txt` and `course_stat_150_workload.txt` alongside the correct `transit_shuttle.txt` — chunks that are close in *meaning* (all "campus life" topics) but share none of the question's actual words ("shuttle", "weekends"). Semantic-only search couldn't tell those apart from the real answer; BM25 can, because it scores on the literal terms. I checked the fix with `python app.py retrieve` before spending any model calls: the two workload chunks dropped out of the top 5 entirely, and `transit_shuttle.txt` moved to rank 1 at distance 0.408 — same distance as before (BM25 doesn't touch the reported distance, only which chunks get chosen and how they're ordered). I also reran all 5 in-scope and 5 out-of-scope questions through retrieval only: every in-scope question still passes the gate and every out-of-scope one is still refused, so the fusion didn't quietly break criterion 3 on the way to fixing precision.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk shorter than 150 characters | 0 fragments | 0 | 0 | 0 | MET |
| 5. Cited documents contain the expects phrase | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Full log: `results/run_2026-09-29_1647_after.md`.

**Did it help?**

No, not on any criterion that's actually measured. All five criteria were MET before and all five are still MET after — nothing moved from MISSED to MET, and the pass/fail totals (13/15 before, 13/15 after) are within noise of each other, still caused by the same "2am" vs "2 am" scorer wording issue on criterion 1, not by retrieval.

It did do exactly what I aimed it at: for the shuttle question, `course_econ_101_workload.txt` and `course_stat_150_workload.txt` — chunks about an unrelated topic that only shared a broad "campus life" vibe — dropped out of the top 5 entirely, replaced by chunks at least nominally closer to the question's actual words. 

BM25 introduced new noise into three of the other four questions, on pure keyword coincidence rather than real relevance:

- **Kestrel Commons dining question** picked up `transit_walking.txt` — a doc about walking times across campus that happens to say "Morrow House to **Kestrel Commons**: 7 minutes." BM25 matched the proper noun with no idea it wasn't about dining.
- **Quiet-study question** picked up `money_jobs.txt`, which talks about on-campus jobs at the "**Library** desk" and whether you "can **study** during the shift" — real words shared with the question, zero relevance to where to study quietly. It also lost `housing_innisfree_hall_noise.txt` and `housing_old_brewhouse_noise.txt` out of the top 5, which had been there before.
- **Meal plan question** picked up `dining_halden_hall.txt` and `dining_kestrel_commons.txt`, both of which mention "one **meal swipe**" in their pricing line — again a real keyword match, not a real answer to a question about changing meal plan *tiers*. It lost `admin_dining_dollars.txt` and `admin_withdrawal_deadline.txt`, which are both administrative-policy documents closer in kind to the actual answer, out of the top 5.

None of this shows up in the numbers because every question's correct chunk still made the fused top 5 and the model still answered correctly from it — the criteria as written only ask "is the answer somewhere in the top 5," not "is the top 5 clean." That's the same gap I flagged in the Diagnoses section when I said criterion 1's top-5 bar was too easy to move the needle. This result is a concrete demonstration of that gap: a real change to the retrieval mechanism happened, in both directions, and the current criteria are blind to all of it.

If I were continuing this, I'd either drop BM25's weight relative to semantic search (right now they're fused 50/50) or restrict BM25 matching to distinctive terms rather than any shared word, so it can't be won by a stray proper noun or a generic word like "study" or "meal."

## What's Still Broken 

- **BM25 makes retrieval noisier for questions it wasn't meant to help.** The Improvement section above shows three of four unfixed questions picked up irrelevant chunks purely on keyword coincidence — a proper noun (`transit_walking.txt` mentioning "Kestrel Commons" in passing), a generic word (`money_jobs.txt` sharing "study" and "library"), a pricing phrase (`dining_halden_hall.txt` and `dining_kestrel_commons.txt` both saying "one meal swipe"). The fix is to weight semantic rank more heavily than BM25 rank in the fusion (right now they're equal, `1/(60+semantic_rank) + 1/(60+bm25_rank)`), or to only let BM25 count a match on terms with high IDF and a minimum length, so it can't be won by a single shared common word. I stopped at diagnosing this and writing it up rather than fixing it because the assignment for this unit asks for one measured change, not a second untested one layered on top of the first — tuning the fusion weight would need its own before/after comparison to know whether it actually helped rather than just moving the noise somewhere else.

- **The scorer's substring matching is still brittle.** The "2am" vs "2 am" mismatch that produced false-negative fails on the quiet-study question in both the before and after runs is unresolved. `scorer.py` does a case-insensitive substring check on a single `expects` string; it doesn't handle spacing or phrasing variants. I ran out of time to go back and rewrite `questions.py`'s `expects` values as alternatives (e.g. `"2am|2 am"`) and rerun, so the run logs still contain those two known-wrong fails rather than a corrected count.

## What I'd Do Differently

- **Criterion 3** ("gate stops out-of-corpus questions," 4 of 5). I'd write the `OUT_OF_SCOPE` list as near-miss questions from the start — things a student might plausibly ask that the corpus just doesn't happen to cover — rather than questions from a different world entirely. As written, this criterion tests that the gate isn't completely broken, not that the 0.6 cutoff is actually in the right place. I noted this in Diagnoses but didn't act on it this unit; next time I'd write the list this way to begin with instead of discovering it after the fact.

- **Criterion 4** ("no chunk shorter than 150 characters"). I'd either drop this criterion for a corpus like `campus_life`, where every document is well over the floor and the chunker's splitting logic never runs, or pair it with a second corpus that actually has long documents so the floor gets exercised. As written it can't fail regardless of chunker quality, which makes it evidence of nothing.

