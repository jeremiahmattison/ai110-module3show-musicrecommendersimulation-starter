# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal / Task**

- It suggests 5 songs a user might like.
- It guesses from three things: favorite genre, favorite mood, and target energy.

**Intended use**

- This is a class project.
- It helps me learn how recommenders work.

**Not intended for**

- Real music apps or real users.
- Judging anyone's taste.
- Anything that needs fair results for everyone. The catalog is too small and too narrow.

---

## 3. How the Model Works  

Every song gets a score out of 5. The top 5 scores win.

- **Genre:** +2 points if it matches. Otherwise 0.
- **Mood:** +1 point if it matches. Otherwise 0.
- **Energy:** up to +2 points. The closer the song's energy is to what you want, the more points.

It also prints the reasons for each score. It ignores tempo, valence, danceability and acousticness.

---

## 4. Data  

- 18 songs in `data/songs.csv`.
- 15 genres and 14 moods.
- Each song has genre, mood, energy, tempo, valence, danceability and acousticness. I only use genre, mood and energy.
- It is tiny. Most genres have only 1 song. Lofi has 3 and pop has 2.
- Some genres are missing, like k-pop and Latin.

---

## 5. Strengths  

- Works well for clear tastes like pop, lofi and rock. The #1 song matches all three things.
- Opposite profiles (pop vs. lofi) get totally different lists. That makes sense.
- The reasons make it easy to see why a song was picked.

---

## 6. Limitations and Bias 

- The catalog is tiny, so a genre with 1 song gives you 1 good pick and 4 fillers.
- Genre and mood have to match exactly. "pop" and "indie pop" count as totally different. So do typos and capital letters.
- If your genre isn't in the catalog, you still get a normal-looking list. Nothing says it found no match.
- It ignores acousticness and valence.

**Weakness found: exact-match labels outweigh the energy the user asked for.** Genre and mood together are worth up to 3.0 points, while the energy gap can cost a song at most 2.0, so a song with the right labels but the wrong energy beats a song that fits the energy. In my tests, a lofi/chill user who wanted energy 0.95 was shown Midnight Coding (energy 0.42) first at 3.94, ahead of Pulse Garden (energy 0.96) at 1.98. A metal/aggressive user who wanted energy 0.05 got Iron Tide (energy 0.97) at #1 with 3.16, well above the next song at 1.74. This hurts anyone whose mood or energy doesn't match the stereotype of their favorite genre. Shifting the weights (genre 1.0, energy 4.0) fixed these cases, but it made genre loyalty weaker for everyone else.

---

---

## 7. Evaluation  

**Quick summary**

- I tested 13 profiles. 3 normal ones and 10 tricky ones.
- I compared their top 5 lists and checked if the #1 song made sense.
- I tried one experiment: genre worth 1 point and energy worth 4. That fixed the conflicting-taste profiles.
- Biggest surprise: "Gym Hero" keeps showing up for happy pop fans. Details below.

### Which profiles I tested

I tested 13 profiles in total, all against the same 18-song catalog:

- **3 standard profiles:** High-Energy Pop (pop / happy / energy 0.85), Chill Lofi (lofi / chill / 0.40) and Deep Intense Rock (rock / intense / 0.92). These are "normal" listeners whose tastes agree with themselves.
- **10 adversarial profiles**, built to try to trick the scoring: people with conflicting tastes (wants sad but high energy, wants lofi but at energy 0.95, wants metal but at energy 0.05), people the catalog doesn't know about (genre "k-pop", mood "serene", empty answers), sloppy input (`"Pop "` with a capital letter and a trailing space, energy of 1.5, energy of -2), and a near-miss ("pop" vs. "indie pop", and an "ambient" fan who wants intense, loud music).

For each one I looked at three things: does the #1 song make sense for a real person with those tastes, does the rest of the list stay in the right "vibe", and does the score ever look wrong or misleading.

### What surprised me

- **"Gym Hero" keeps showing up for people who just want happy pop.** Here is why, in plain terms. The system gives every song points: 2 points if the genre is the same, 1 point if the mood is the same, and up to 2 points for how close the energy is. "Sunrise City" is pop, happy and high-energy, so it earns nearly all 5 points and wins. But the catalog only has two pop songs, and the other one is "Gym Hero". It is pop (+2), and its energy is almost the same as what the listener asked for (+1.84), so it scores 3.84 and takes second place. It only misses the 1 point for "happy", because its mood label is "intense". The computer doesn't understand that a workout anthem *feels* different from a feel-good song. It only checks whether the mood word is spelled the same, and the genre word is worth twice as much as the mood word. Any pop fan will therefore see "Gym Hero" near the top whether or not they want a workout song, and the Rock profile gets it at #2 too, for a different reason (its "intense" mood and loud energy).
- **Labels beat what the person actually asked for.** The lofi fan who wanted very high energy was still shown quiet lofi songs first, and the metal fan who wanted nearly silent music was shown the loudest metal song first. Matching words counted for more than matching the feel.
- **Bad or unusual input fails silently.** Energy of 1.5 and `"Pop "` were accepted with no warning, and energy of -2 produced negative scores on a "0 to 5" scale. An unknown genre or mood gave a normal-looking list with no hint that nothing matched.
- **An unknown taste and no taste at all give the same answer.** The "k-pop / serene" profile and the empty profile (both energy 0.50) returned identical top 5 lists, so the system can't tell "I don't know what you want" from "I couldn't find what you want".

### Comparing the profiles, pair by pair

**The three standard profiles**

- **High-Energy Pop vs. Chill Lofi: zero songs in common.** Pop wants energy 0.85 and gets Sunrise City, Gym Hero, Rooftop Lights, Storm Runner, Night Drive Loop. Lofi wants 0.40 and gets Midnight Coding, Library Rain, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories. That makes sense: one listener wants an upbeat drive, the other wants quiet background music, and the system pulled from opposite ends of the catalog. The lofi list has all three lofi songs on top because the catalog has exactly three; after that it fills the list with other slow, calm songs.
- **High-Energy Pop vs. Deep Intense Rock: three songs in common (Sunrise City, Gym Hero, Storm Runner).** Both listeners want loud, fast music (0.85 vs. 0.92), so the overlap is expected. The differences are at the top: Pop puts the happy pop song first, Rock puts the intense rock song first. Past those top picks both lists are just "the loudest songs in the catalog", because the genre and mood labels have run out of matches and only energy is left. Gym Hero is the bridge between the two profiles: it is a pop song (helps the pop fan) with an "intense" mood and huge energy (helps the rock fan).
- **Chill Lofi vs. Deep Intense Rock: zero songs in common.** This is the opposite-ends test. Lofi gets slow, acoustic songs; Rock gets loud, electric ones. The result is valid and about what any listener would expect.

**Each adversarial profile vs. the standard profile it is closest to**

- **Chill Lofi vs. lofi / chill / energy 0.95.** Same genre and mood, only the energy changed. The same three lofi songs stayed on top (their scores dropped from about 4.9 to 3.8-3.9), and the two loud songs that actually fit the energy (Pulse Garden, Gym Hero) only reached #4 and #5. Not valid: nobody asking for 0.95 energy wants Library Rain. This is the clearest sign that labels count for too much.
- **Deep Intense Rock vs. metal / aggressive / energy 0.05.** The metal fan wants nearly silent music but gets the loudest song in the catalog (Iron Tide, energy 0.97) at #1, followed by quiet songs (Moonlit Sonata, Spacewalk Thoughts). It looks like a list written for two different people. The only reason the loud song wins is that its genre and mood words match.
- **Deep Intense Rock vs. classical / sad / energy 0.9.** Rock gets a clean #1 (Storm Runner, a full match). The classical fan wants loud music, but the one classical song is very quiet (energy 0.18) and still wins on the genre bonus; "sad" matched nothing because the catalog says "melancholy". The rest of the list is the loud songs they asked for, so they get a list that splits down the middle.
- **Deep Intense Rock vs. ambient / intense / energy 0.93.** Rock has a song that matches on genre, mood and energy, so it's an easy win. The ambient fan has no song that matches on genre *and* mood: the two loud "intense" songs (Gym Hero, Storm Runner) win on mood plus energy, and the only ambient song (quiet Spacewalk Thoughts) takes #3. That makes sense for what the data holds, but it shows a person with a rare genre gets a worse list.
- **High-Energy Pop vs. pop / happy / energy 0.76 (near-miss).** Nearly the same listener, a little calmer. The same three songs lead, but the gap between Gym Hero and "Rooftop Lights" (an indie-pop, happy song with exactly the right energy) shrinks from about 1.0 point to 0.66, and Gym Hero still wins. A human would see Rooftop Lights as a better fit for "happy pop", but "indie pop" is not spelled the same as "pop", so it gets no genre credit.
- **High-Energy Pop vs. `"Pop "` / `"Happy"` / energy 0.80.** Almost the same person, only the typing differs (capital letters and a trailing space). Gym Hero disappears and the list becomes whatever is closest in energy, led by Sunrise City on energy alone (1.96 instead of about 4.9). This is a software problem, not a taste problem: the system can't tell that "Pop " and "pop" mean the same thing.
- **High-Energy Pop vs. pop / happy / energy 1.5.** The same top three songs appear (Sunrise City, Gym Hero, Rooftop Lights), now with lower scores, and #4 and #5 become the two loudest songs in the catalog (Iron Tide, Pulse Garden). That is sensible behavior for an impossible request ("louder than the loudest"), but the system should have complained instead of quietly accepting 1.5.
- **High-Energy Pop vs. pop / happy / energy -2.** The label matches still decide the top spots (Sunrise City, Gym Hero), but below them the *quietest* songs rank highest, and every score is negative. The ranking direction is consistent, but the numbers are meaningless, which is the kind of output that would mislead a user who trusted the "/ 5.00".

**Two adversarial profiles against each other**

- **k-pop / serene / 0.50 vs. empty genre and mood / 0.50.** Identical top 5 (Dusty Porch Light, Velvet Hours, Island Drift, Midnight Coding, Focus Flow). Both end up as "just find songs near energy 0.5". This shows the system treats "nothing matched" and "no preference" the same way, which is a design gap, not a bug in the math.

### Did the change in weights make anything better?

I also tried a version with genre worth 1.0 and energy worth 4.0 (see the README's experiments section). The three standard profiles didn't change at all, and the conflicting-taste profiles (lofi at 0.95, metal at 0.05, classical at 0.9) all picked songs that fit the requested energy. So the weights were the cause of those odd results, but the typing, unknown-genre and out-of-range problems need code changes, not different weights.

### Terminal output by profile

Captured by running `print_recommendations` from `src/main.py` for each profile (top 5, `k=5`). The three standard profiles come first, followed by adversarial / edge-case profiles. These runs were captured before the blank row at the end of `data/songs.csv` was removed (it made `load_songs` crash); the song data itself is the same as it is now.

#### High-Energy Pop

```
============================================================
High-Energy Pop: pop / happy / energy 0.85
============================================================

#1  Sunrise City - Neon Echo
    Score: 4.94 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+1.94)

#2  Gym Hero - Max Pulse
    Score: 3.84 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+1.84)

#3  Rooftop Lights - Indigo Parade
    Score: 2.82 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+1.82)

#4  Storm Runner - Voltline
    Score: 1.88 / 5.00
    Reasons:
      - energy closeness (+1.88)

#5  Night Drive Loop - Neon Echo
    Score: 1.80 / 5.00
    Reasons:
      - energy closeness (+1.80)
```

#### Chill Lofi

```
============================================================
Chill Lofi: lofi / chill / energy 0.40
============================================================

#1  Midnight Coding - LoRoom
    Score: 4.96 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+1.96)

#2  Library Rain - Paper Lanterns
    Score: 4.90 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+1.90)

#3  Focus Flow - LoRoom
    Score: 4.00 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+2.00)

#4  Spacewalk Thoughts - Orbit Bloom
    Score: 2.76 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+1.76)

#5  Coffee Shop Stories - Slow Stereo
    Score: 1.94 / 5.00
    Reasons:
      - energy closeness (+1.94)
```

#### Deep Intense Rock

```
============================================================
Deep Intense Rock: rock / intense / energy 0.92
============================================================

#1  Storm Runner - Voltline
    Score: 4.98 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+1.98)

#2  Gym Hero - Max Pulse
    Score: 2.98 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+1.98)

#3  Pulse Garden - Kairo Lux
    Score: 1.92 / 5.00
    Reasons:
      - energy closeness (+1.92)

#4  Iron Tide - Hollow Crown
    Score: 1.90 / 5.00
    Reasons:
      - energy closeness (+1.90)

#5  Sunrise City - Neon Echo
    Score: 1.80 / 5.00
    Reasons:
      - energy closeness (+1.80)
```

#### ADV Conflict: high energy + sad

```
============================================================
ADV Conflict: high energy + sad: classical / sad / energy 0.90
============================================================

#1  Moonlit Sonata - Elena Voss
    Score: 2.56 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+0.56)

#2  Storm Runner - Voltline
    Score: 1.98 / 5.00
    Reasons:
      - energy closeness (+1.98)

#3  Gym Hero - Max Pulse
    Score: 1.94 / 5.00
    Reasons:
      - energy closeness (+1.94)

#4  Pulse Garden - Kairo Lux
    Score: 1.88 / 5.00
    Reasons:
      - energy closeness (+1.88)

#5  Iron Tide - Hollow Crown
    Score: 1.86 / 5.00
    Reasons:
      - energy closeness (+1.86)
```

**Observation:** Genre bonus drags a quiet classical song to #1 for a high-energy user; "sad" matches no catalog mood (closest is "melancholy").

#### ADV Conflict: lofi/chill + high energy

```
============================================================
ADV Conflict: lofi/chill + high energy: lofi / chill / energy 0.95
============================================================

#1  Midnight Coding - LoRoom
    Score: 3.94 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+0.94)

#2  Library Rain - Paper Lanterns
    Score: 3.80 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+0.80)

#3  Focus Flow - LoRoom
    Score: 2.90 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+0.90)

#4  Pulse Garden - Kairo Lux
    Score: 1.98 / 5.00
    Reasons:
      - energy closeness (+1.98)

#5  Gym Hero - Max Pulse
    Score: 1.96 / 5.00
    Reasons:
      - energy closeness (+1.96)
```

**Observation:** Genre + mood (3.0 pts) beat a 0.5+ energy gap; the songs that actually fit the energy rank below the lofi tracks.

#### ADV Conflict: metal/aggressive + low energy

```
============================================================
ADV Conflict: metal/aggressive + low energy: metal / aggressive / energy 0.05
============================================================

#1  Iron Tide - Hollow Crown
    Score: 3.16 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+0.16)

#2  Moonlit Sonata - Elena Voss
    Score: 1.74 / 5.00
    Reasons:
      - energy closeness (+1.74)

#3  Spacewalk Thoughts - Orbit Bloom
    Score: 1.54 / 5.00
    Reasons:
      - energy closeness (+1.54)

#4  Autumn Letters - Juniper Hale
    Score: 1.44 / 5.00
    Reasons:
      - energy closeness (+1.44)

#5  Library Rain - Paper Lanterns
    Score: 1.40 / 5.00
    Reasons:
      - energy closeness (+1.40)
```

**Observation:** Iron Tide (energy 0.97) wins for a user who wants energy 0.05, on labels alone.

#### ADV Unknown genre+mood

```
============================================================
ADV Unknown genre+mood: k-pop / serene / energy 0.50
============================================================

#1  Dusty Porch Light - Willow Creek
    Score: 1.96 / 5.00
    Reasons:
      - energy closeness (+1.96)

#2  Velvet Hours - Amara Skye
    Score: 1.90 / 5.00
    Reasons:
      - energy closeness (+1.90)

#3  Island Drift - Sol Marley
    Score: 1.84 / 5.00
    Reasons:
      - energy closeness (+1.84)

#4  Midnight Coding - LoRoom
    Score: 1.84 / 5.00
    Reasons:
      - energy closeness (+1.84)

#5  Focus Flow - LoRoom
    Score: 1.80 / 5.00
    Reasons:
      - energy closeness (+1.80)
```

**Observation:** No genre or mood matches; ranking silently falls back to energy only.

#### ADV Case/whitespace

```
============================================================
ADV Case/whitespace: Pop  / Happy / energy 0.80
============================================================

#1  Sunrise City - Neon Echo
    Score: 1.96 / 5.00
    Reasons:
      - energy closeness (+1.96)

#2  Rooftop Lights - Indigo Parade
    Score: 1.92 / 5.00
    Reasons:
      - energy closeness (+1.92)

#3  Night Drive Loop - Neon Echo
    Score: 1.90 / 5.00
    Reasons:
      - energy closeness (+1.90)

#4  Concrete Dreams - Kid Meridian
    Score: 1.82 / 5.00
    Reasons:
      - energy closeness (+1.82)

#5  Storm Runner - Voltline
    Score: 1.78 / 5.00
    Reasons:
      - energy closeness (+1.78)
```

**Observation:** "Pop " and "Happy" never match "pop"/"happy", so all label points are lost.

#### ADV Energy 1.5

```
============================================================
ADV Energy 1.5: pop / happy / energy 1.50
============================================================

#1  Sunrise City - Neon Echo
    Score: 3.64 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+0.64)

#2  Gym Hero - Max Pulse
    Score: 2.86 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+0.86)

#3  Rooftop Lights - Indigo Parade
    Score: 1.52 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+0.52)

#4  Iron Tide - Hollow Crown
    Score: 0.94 / 5.00
    Reasons:
      - energy closeness (+0.94)

#5  Pulse Garden - Kairo Lux
    Score: 0.92 / 5.00
    Reasons:
      - energy closeness (+0.92)
```

**Observation:** Out-of-range energy is accepted with no validation.

#### ADV Energy -2

```
============================================================
ADV Energy -2: pop / happy / energy -2.00
============================================================

#1  Sunrise City - Neon Echo
    Score: -0.64 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+-3.64)

#2  Gym Hero - Max Pulse
    Score: -1.86 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+-3.86)

#3  Moonlit Sonata - Elena Voss
    Score: -2.36 / 5.00
    Reasons:
      - energy closeness (+-2.36)

#4  Rooftop Lights - Indigo Parade
    Score: -2.52 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+-3.52)

#5  Spacewalk Thoughts - Orbit Bloom
    Score: -2.56 / 5.00
    Reasons:
      - energy closeness (+-2.56)
```

**Observation:** Scores go negative (and print as "+-3.64"), breaking the documented 0-5 range.

#### ADV Empty genre/mood

```
============================================================
ADV Empty genre/mood:  /  / energy 0.50
============================================================

#1  Dusty Porch Light - Willow Creek
    Score: 1.96 / 5.00
    Reasons:
      - energy closeness (+1.96)

#2  Velvet Hours - Amara Skye
    Score: 1.90 / 5.00
    Reasons:
      - energy closeness (+1.90)

#3  Island Drift - Sol Marley
    Score: 1.84 / 5.00
    Reasons:
      - energy closeness (+1.84)

#4  Midnight Coding - LoRoom
    Score: 1.84 / 5.00
    Reasons:
      - energy closeness (+1.84)

#5  Focus Flow - LoRoom
    Score: 1.80 / 5.00
    Reasons:
      - energy closeness (+1.80)
```

**Observation:** Empty strings are accepted; identical result to the unknown-label case.

#### ADV Near-miss pop vs indie pop

```
============================================================
ADV Near-miss pop vs indie pop: pop / happy / energy 0.76
============================================================

#1  Sunrise City - Neon Echo
    Score: 4.88 / 5.00
    Reasons:
      - genre match (+2.0)
      - mood match (+1.0)
      - energy closeness (+1.88)

#2  Gym Hero - Max Pulse
    Score: 3.66 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+1.66)

#3  Rooftop Lights - Indigo Parade
    Score: 3.00 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+2.00)

#4  Night Drive Loop - Neon Echo
    Score: 1.98 / 5.00
    Reasons:
      - energy closeness (+1.98)

#5  Concrete Dreams - Kid Meridian
    Score: 1.90 / 5.00
    Reasons:
      - energy closeness (+1.90)
```

**Observation:** "indie pop" gets no genre credit for pop, so Gym Hero (pop, intense) outranks Rooftop Lights (indie pop, happy, exact energy).

#### ADV Ambient/intense/high energy

```
============================================================
ADV Ambient/intense/high energy: ambient / intense / energy 0.93
============================================================

#1  Gym Hero - Max Pulse
    Score: 3.00 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+2.00)

#2  Storm Runner - Voltline
    Score: 2.96 / 5.00
    Reasons:
      - mood match (+1.0)
      - energy closeness (+1.96)

#3  Spacewalk Thoughts - Orbit Bloom
    Score: 2.70 / 5.00
    Reasons:
      - genre match (+2.0)
      - energy closeness (+0.70)

#4  Pulse Garden - Kairo Lux
    Score: 1.94 / 5.00
    Reasons:
      - energy closeness (+1.94)

#5  Iron Tide - Hollow Crown
    Score: 1.92 / 5.00
    Reasons:
      - energy closeness (+1.92)
```

**Observation:** Two mood matches outrank the only ambient song, which has the wrong energy.

---

## 8. Future Work  

1. Give partial credit for close genres and moods, like "sad" and "melancholy", or "pop" and "indie pop".
2. Use more song features, like acousticness and valence. Add a check for bad input and warn when nothing matches.
3. Add more songs and stop one artist or genre from filling the whole top 5.

---

## 9. Personal Reflection  

**Biggest learning moment.** I learned that a recommender is just a scoring rule, and the weights are my choices. When I tried tricky profiles, a lofi fan who wanted high energy still got quiet songs. The labels counted for more than the vibe. I didn't see that until I tried to break my own system.

**How AI helped, and when I double-checked.** The AI helped me find edge cases fast. It also found a blank row in my CSV that crashed the whole app. But I had to check its work. It first said there were 15 moods when there are 14, and my README still said 10 songs when there are 18. When we changed the weights, the max score became 6, not 5, so the "/ 5.00" would have been wrong. I learned to run the code and check the numbers myself.

**What surprised me.** A really simple rule can still feel like a real recommendation. Sunrise City came up first for the pop fan and I thought, "yeah, that makes sense." It's only three points added together. The "reasons" lines make it feel smart too. Then Gym Hero showed up and it felt dumb, because the computer only checks if words match.

**What I'd try next.** I'd give partial credit for close genres and moods, like pop and indie pop. I'd add acousticness and valence, and I'd add checks so bad input gets a warning. I'd also add more songs so each genre has more than one.
