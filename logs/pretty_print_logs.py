
import json
from collections import defaultdict
from datetime import datetime

def pretty_print_game_log(filepath):
    with open(filepath, "r") as f:
        events = [json.loads(line) for line in f if line.strip()]

    game_events = defaultdict(list)
    for event in events:
        game_events[event["game_id"]].append(event)

    for game_id in sorted(game_events.keys()):
        turns = []
        current_turn = []

        for event in game_events[game_id]:
            if event["event_type"] == "roll":
                current_turn.append({"type": "roll", "dice": [d["value"] for d in event["data"]["dice"]]})
            elif event["event_type"] == "score":
                current_turn.append({
                    "type": "score",
                    "category": event["data"]["category"],
                    "scorecard": event["data"]["game_state"]["scorecard"]
                })
                turns.append(current_turn)
                current_turn = []

        start_event = next((e for e in game_events[game_id] if e["event_type"] == "new_game"), None)
        end_event = next((e for e in game_events[game_id] if e["event_type"] == "game_over"), None)

        start_time = start_event["timestamp"] if start_event else "unknown"
        end_time = end_event["timestamp"] if end_event else "unknown"
        final_score = end_event["data"]["final_score"] if end_event else "?"

        print(f"\n🎲 Game ID: {game_id}")
        print(f"🕒 Started at: {start_time}\n")

        for i, turn in enumerate(turns, 1):
            print(f"Turn {i}")
            for action in turn:
                if action["type"] == "roll":
                    print(f"  - Rolled: {action['dice']}")
                elif action["type"] == "score":
                    cat = action["category"]
                    score = action["scorecard"]["scores"][cat]
                    print(f"  - Scored: {cat} → {score} pts")
            print()

        print(f"🏁 Game Over at {end_time}")
        print(f"🔢 Final Score: {final_score}")
        print("="*40)

# Example usage:
pretty_print_game_log("game_logs.jsonl")
