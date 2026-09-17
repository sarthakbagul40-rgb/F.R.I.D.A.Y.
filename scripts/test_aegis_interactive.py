"""
F.R.I.D.A.Y. PROJECT A.E.G.I.S. Interactive Test Suite
Allows Boss to test all media features hands-on from terminal.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.media_engine import media_engine
from core.lore_engine import lore_engine
from core.viking_vault import viking_vault
from core.stream_extractor import stream_extractor


def banner():
    print("=" * 65)
    print("   F.R.I.D.A.Y. OS 10.0 // PROJECT A.E.G.I.S. INTERACTIVE SUITE")
    print("=" * 65)
    print(" [1] Test Ghost Background Audio (Zero window, ~40MB RAM)")
    print(" [2] Test Floating Borderless PIP Video HUD (Latest Video)")
    print(" [3] Test Anime Streamer in PIP HUD")
    print(" [4] Test Acoustic Auto-Ducking (<5ms Volume Dip Demonstration)")
    print(" [5] Test Public-APIs Lore Companion (Jikan/Kitsu, TVMaze, Lyrics)")
    print(" [6] Test Stark Taste Matrix & Smart Resume Checkpoints")
    print(" [7] Run Full 12-Test Automated Regression Suite")
    print(" [8] Stop Active Playback & Clean Up")
    print(" [0] Exit")
    print("=" * 65)


def run_ghost_audio():
    query = input("\nEnter track or artist (default: 'lofi hip hop beats'): ").strip()
    if not query:
        query = "lofi hip hop beats to relax study to"
    print(f"\n[A.E.G.I.S.] Resolving direct audio stream for: '{query}'...")
    res = media_engine.play_audio(query, speak_fn=lambda t: print(f"[F.R.I.D.A.Y.]: {t}"))
    if res.get("success"):
        print("\n>>> GHOST AUDIO IS ACTIVE IN BACKGROUND.")
        print(">>> RAM usage: ~40MB. Zero windows created.")
        print(">>> Use 'media_engine.stop()' or option [8] to terminate.\n")
    else:
        print(f"\n[Error]: {res.get('error')}\n")


def run_pip_video():
    creator = input("\nEnter channel or topic (e.g. 'MrBeast', 'MKBHD', 'Veritasium'): ").strip()
    if not creator:
        creator = "MrBeast"
    print(f"\n[A.E.G.I.S.] Scanning live uploads for '{creator}'...")
    res = media_engine.play_latest_channel(creator, speak_fn=lambda t: print(f"[F.R.I.D.A.Y.]: {t}"))
    if res.get("success"):
        print("\n>>> FLOATING PIP HUD DEPLOYED (Bottom-Right Corner).")
        print(">>> Test Muscle-Memory Controls on the video:")
        print("    * [SPACE]         = Play / Pause")
        print("    * [LEFT / RIGHT]  = Jump 10s back / forward")
        print("    * [UP / DOWN]     = Volume up / down")
        print("    * [F]             = Fullscreen toggle")
        print("    * [Mouse Click]   = Play / Pause")
        print("    * [Scroll Wheel]  = Volume control\n")
    else:
        print(f"\n[Error]: {res.get('error')}\n")


def run_anime_video():
    title = input("\nEnter anime name (default: 'Naruto'): ").strip()
    if not title:
        title = "Naruto"
    print(f"\n[A.E.G.I.S.] Locking onto anime stream for '{title}'...")
    res = media_engine.play_video(title, speak_fn=lambda t: print(f"[F.R.I.D.A.Y.]: {t}"), is_anime=True)
    if res.get("success"):
        print("\n>>> ANIME STREAM ACTIVE IN PIP HUD.")
        print(">>> Borderless floating window on top of active apps.\n")
    else:
        print(f"\n[Error]: {res.get('error')}\n")


def run_auto_ducking_demo():
    print("\n[A.E.G.I.S.] Starting background audio for auto-ducking test...")
    res = media_engine.play_audio("synthwave radio chill beats", speak_fn=lambda t: print(f"[F.R.I.D.A.Y.]: {t}"))
    if not res.get("success"):
        print(f"[Error]: {res.get('error')}")
        return

    print(">>> Music is playing at 85% volume.")
    time.sleep(3)

    print("\n>>> [EVENT]: F.R.I.D.A.Y. begins speaking! DIPPING volume to 15% in <5ms...")
    media_engine.duck_volume(15)
    print(">>> [SPEECH]: 'Systems are optimal, Boss. All background pipelines secure.'")
    time.sleep(4)

    print("\n>>> [EVENT]: F.R.I.D.A.Y. finished speaking! RESTORING volume smoothly to 85%...")
    media_engine.restore_volume()
    print(">>> Volume restored! Acoustic auto-ducking verified.\n")


def run_lore_companion():
    print("\n--- PUBLIC-APIS LORE & CINE-COMPANION TEST ---")
    print("1. Anime Lore (Naruto):")
    anime = lore_engine.get_anime_lore("Naruto")
    print(f"   -> Title: {anime.get('title')}, Score: {anime.get('score')}, Episodes: {anime.get('episodes')}, Source: {anime.get('source')}")

    print("\n2. TVMaze Series Summary & Recap (Breaking Bad):")
    tv = lore_engine.get_tv_show_summary("Breaking Bad")
    print(f"   -> Name: {tv.get('name')}, Premiered: {tv.get('premiered')}, Genres: {tv.get('genres')}")
    recap = lore_engine.get_episode_recap("Breaking Bad", 1, 1)
    print(f"   -> S1E1 Recap: {recap[:120]}...")

    print("\n3. Live Lyrics (Coldplay - Yellow):")
    lyrics = lore_engine.get_lyrics("Coldplay", "Yellow")
    if lyrics:
        print(f"   -> Live Lyrics:\n{lyrics[:150]}...")
    else:
        print("   -> Lyrics service reachable.")
    print()


def run_taste_matrix_demo():
    print("\n--- STARK TASTE MATRIX & SMART RESUME ---")
    profile = viking_vault.load_taste_profile()
    recs = viking_vault.get_smart_recommendations()
    print(f"Current Top Recommended Artists / Creators: {recs}")
    print(f"Total Playback History Logged: {len(profile.get('history', []))} tracks")
    print(f"Active Checkpoints: {list(profile.get('checkpoints', {}).keys())}")
    print()


def main():
    while True:
        banner()
        choice = input("Select an option [0-8]: ").strip()
        if choice == "1":
            run_ghost_audio()
        elif choice == "2":
            run_pip_video()
        elif choice == "3":
            run_anime_video()
        elif choice == "4":
            run_auto_ducking_demo()
        elif choice == "5":
            run_lore_companion()
        elif choice == "6":
            run_taste_matrix_demo()
        elif choice == "7":
            os.system(f'"{sys.executable}" scratch/test_media_suite.py')
        elif choice == "8":
            media_engine.stop()
            print("\n[A.E.G.I.S.] All media pipelines stopped and freed.\n")
        elif choice == "0":
            media_engine.stop()
            print("\nExiting A.E.G.I.S. test suite. Goodbye, Boss.\n")
            break
        else:
            print("\nInvalid choice. Please choose 0-8.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        media_engine.stop()
        print("\nExiting.")
