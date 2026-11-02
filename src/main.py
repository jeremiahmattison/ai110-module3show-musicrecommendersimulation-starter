"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

MAX_SCORE = 5.0


# Taste profiles: genre and mood are exact-match bonuses; energy is a
# 0.0-1.0 target the scoring rule measures closeness to.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print()
    print("=" * width)
    print(
        f"{name}: {user_prefs['genre']} / {user_prefs['mood']} / "
        f"energy {user_prefs['energy']:.2f}"
    )
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} - {song['artist']}")
        print(f"    Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("    Reasons:")
        for reason in explanation.split(", "):
            print(f"      - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
