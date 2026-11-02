# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube mostly combine two ideas: collaborative filtering, which looks at what lots of other users listen to, skip, and save, and content-based filtering, which looks at the attributes of the songs themselves. They also use a ton of data I don't have, like listening history, time of day, and device, and they test everything on millions of people. My version is a lot smaller. It only uses content-based filtering, since I have no data about other users, just 10 songs with attributes like energy, valence, and acousticness. Instead of saying "higher is better," it scores each song by how *close* it is to what the user wants, so someone who wants chill music doesn't get a super intense workout song. I treat genre as the strongest signal, since a genre match is the best sign a song is in the listener's comfort zone, with mood as a smaller refinement and energy closeness to keep the vibe right. Then it ranks all the songs by their score and returns the top few.

**What features does each `Song` use?**
Each song has genre, mood, energy, tempo, valence, danceability, and acousticness (plus id, title, and artist for display). For scoring I only use genre, mood, and energy. The other numeric features are left out to keep the first version simple and easy to explain.

**What does the `UserProfile` store?**
A favorite genre, a favorite mood, and a target energy value between 0 and 1.

**Algorithm Recipe**
Every song gets a score out of 5.0 from three parts:

| Component | Rule | Points |
|---|---|---|
| Genre | song genre equals the user's favorite genre | +2.0 or 0 |
| Mood | song mood equals the user's favorite mood | +1.0 or 0 |
| Energy | `2.0 * (1 - abs(song energy - target energy))` | 0.0 to 2.0 |

```python
def score_song(user, song):
    score = 0.0
    if song["genre"] == user["genre"]:
        score += 2.0
    if song["mood"] == user["mood"]:
        score += 1.0
    score += 2.0 * (1 - abs(song["energy"] - user["target_energy"]))
    return score
```

Energy is already between 0 and 1, so no normalization is needed. Closeness means a song with energy near the target scores close to 2.0, and one far from it scores close to 0.

**How do you choose which songs to recommend?**
I score every song in the CSV, sort from highest to lowest, and return the top `k` (default 5) with a short explanation of why each one was picked (for example, "genre match +2.0, energy close +1.8").

**Expected biases**
- **Genre over-prioritization:** A genre match is worth 2.0 and a mood match only 1.0, so a song in the right genre but the wrong mood can outrank a song that matches the user's mood perfectly in another genre. Great cross-genre songs will be buried.
- **Filter bubble:** Because genre dominates, users mostly get more of what they already listen to, with little discovery.
- **All-or-nothing labels:** Genre and mood are exact string matches, so "chill" vs. "relaxed" or "indie pop" vs. "pop" count as a full miss even though they are close.
- **Energy as a stand-in for vibe:** Valence, acousticness, danceability, and tempo are ignored, so two songs with the same energy but very different feels (a happy dance track vs. a tense one) can score the same.
- **Tiny catalog:** With only 10 songs, genres with few or no entries will give some users weak or arbitrary results, and tied scores are possible.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default profile (genre = pop, mood = happy, target energy = 0.80):

```
Loaded songs: 18

============================================================
Top 5 for: pop / happy / energy 0.80
============================================================

#1  Sunrise City - Neon Echo
    Score: 4.96 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+1.96)

#2  Gym Hero - Max Pulse
    Score: 3.74 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+1.74)

#3  Rooftop Lights - Indigo Parade
    Score: 2.92 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+1.92)

#4  Night Drive Loop - Neon Echo
    Score: 1.90 / 5.00
    Reasons:
      - energy closeness (+1.90)

#5  Concrete Dreams - Kid Meridian
    Score: 1.82 / 5.00
    Reasons:
      - energy closeness (+1.82)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Experiment: Weight Shift (genre 2.0 → 1.0, energy 2.0 → 4.0)

**Change** (in `score_song`): genre bonus `2.0 → 1.0`, energy term `2.0 * (1 - |diff|) → 4.0 * (1 - |diff|)`, mood unchanged at `1.0`.

**Math check:** the maximum score becomes 1.0 + 1.0 + 4.0 = **6.0** (was 5.0), so `MAX_SCORE` in `main.py` had to become 6.0 or the "/ 5.00" display would be wrong. For valid energy values (0–1) the minimum is still 0.0. Confirmed by calling `score_song` on a perfect match (6.0) and a worst-case mismatch (0.0).

**Ran all 13 profiles (3 standard + 10 adversarial), before vs. after, top 5:**

| Profile | Top 1 before | Top 1 after | Verdict |
|---|---|---|---|
| High-Energy Pop / Chill Lofi / Deep Intense Rock | unchanged | unchanged | Identical top 5, identical order |
| Conflict: lofi/chill + energy 0.95 | Midnight Coding (energy 0.42) | Pulse Garden (energy 0.96) | **More accurate**: the song that fits the requested energy now wins; lofi tracks drop to #4 or lower |
| Conflict: metal/aggressive + energy 0.05 | Iron Tide (energy 0.97) | Moonlit Sonata (energy 0.18) | **More accurate**: Iron Tide no longer wins on labels alone |
| Conflict: classical/sad + energy 0.9 | Moonlit Sonata (energy 0.18) | Storm Runner (energy 0.91) | **More accurate**: no more quiet song for a high-energy user |
| pop/happy/0.76 (near-miss genre) | Sunrise > Gym Hero > Rooftop Lights | Sunrise > Rooftop Lights > Gym Hero | Better: exact-energy indie pop happy now outranks pop/intense |
| Ambient/intense/0.93 | Spacewalk Thoughts at #3 | Spacewalk Thoughts dropped out of top 5 | Arguably better (wrong energy), but the user's genre disappears entirely |
| Energy -2 (invalid input) | Sunrise City | Moonlit Sonata | Just different: invalid input still produces garbage, now with scores down to about -6 |
| Unknown genre, case/whitespace, energy 1.5, empty labels | unchanged | unchanged | No effect: these failures come from label handling and validation, not weights |

**Takeaways**
- For normal profiles the change was invisible, because the best song already matched on all three features.
- For conflicting profiles it made the system **more accurate, not just different**: the top result now respects the user's energy instead of being decided by labels.
- It trades one bias for another. Genre loyalty is weaker, so a user who really wants "pop" is more likely to be shown non-pop songs with closer energy. Energy now acts almost like the whole recommender (4.0 of 6.0 points).
- It does not fix the label problems (unknown genre/mood, case sensitivity, missing validation). Those need code changes, not reweighting.
- The experiment was reverted afterwards so the code matches the documented 2.0 / 1.0 / 2.0 recipe and the model card output.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



