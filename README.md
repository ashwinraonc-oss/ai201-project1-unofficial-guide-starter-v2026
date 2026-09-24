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

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
