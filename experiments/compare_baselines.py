
import csv
import random
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from quality_env import QualityControlEnv, ACCEPT, REJECT, INSPECT
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent


EPISODES = 1000
SEED = 2026
RESULTS_DIR = ROOT / "results"


def run_episode(agent_name, seed):
    env = QualityControlEnv(
        batch_size=10,
        inspection_budget=4,
        seed=seed
    )

    if agent_name == "Random":
        agent = RandomAgent(seed=seed + 1)
    elif agent_name == "Heuristic":
        agent = HeuristicAgent()
    else:
        raise ValueError("Nieznany agent.")

    state = env.reset()

    total_reward = 0
    correct_decisions = 0
    missed_defects = 0
    false_rejections = 0
    inspections = 0
    decisions = 0

    while not env.done:
        action = agent.choose_action(
            state,
            env.valid_actions()
        )

        state, reward, done, info = env.step(action)
        total_reward += reward

        if action == INSPECT:
            inspections += 1
            continue

        decisions += 1

        if info["correct"]:
            correct_decisions += 1
        elif action == ACCEPT:
            missed_defects += 1
        elif action == REJECT:
            false_rejections += 1

    defective_count = sum(
        plate.is_defective()
        for plate in env.plates
    )

    good_count = len(env.plates) - defective_count

    assert decisions == env.batch_size
    assert inspections <= env.inspection_budget

    return {
        "agent": agent_name,
        "seed": seed,
        "reward": total_reward,
        "decisions": decisions,
        "correct": correct_decisions,
        "defective": defective_count,
        "good": good_count,
        "missed_defects": missed_defects,
        "false_rejections": false_rejections,
        "inspections": inspections,
    }


def summarize(records, name):
    rows = [
        row for row in records
        if row["agent"] == name
    ]

    total_decisions = sum(row["decisions"] for row in rows)
    total_correct = sum(row["correct"] for row in rows)

    total_defective = sum(row["defective"] for row in rows)
    total_good = sum(row["good"] for row in rows)

    total_missed = sum(row["missed_defects"] for row in rows)
    total_false = sum(row["false_rejections"] for row in rows)

    return {
        "agent": name,
        "episodes": len(rows),
        "mean_reward": round(mean(row["reward"] for row in rows), 3),
        "accuracy_pct": round(
            100 * total_correct / total_decisions, 2
        ),
        "missed_defect_rate_pct": round(
            100 * total_missed / total_defective, 2
        ) if total_defective else 0.0,
        "false_rejection_rate_pct": round(
            100 * total_false / total_good, 2
        ) if total_good else 0.0,
        "mean_inspections": round(
            mean(row["inspections"] for row in rows), 3
        ),
    }


def save_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0].keys())
        )

        writer.writeheader()
        writer.writerows(rows)


def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    rng = random.Random(SEED)

    seeds = [
        rng.randrange(2**32)
        for _ in range(EPISODES)
    ]

    records = []

    print("EKSPERYMENT POROWNAWCZY E2")
    print("=" * 60)
    print(f"Liczba epizodow na agenta: {EPISODES}")
    print(f"Liczba plytek na epizod: 10")
    print(f"Ziarno eksperymentu: {SEED}")

    for episode, seed in enumerate(seeds, start=1):
        for name in ("Random", "Heuristic"):
            result = run_episode(name, seed)
            result["episode"] = episode
            records.append(result)

    summaries = [
        summarize(records, "Random"),
        summarize(records, "Heuristic"),
    ]

    save_csv(
        RESULTS_DIR / "baseline_episodes.csv",
        records
    )

    save_csv(
        RESULTS_DIR / "baseline_summary.csv",
        summaries
    )

    for result in summaries:
        print("\n" + "-" * 60)
        print(f"AGENT: {result['agent']}")
        print(f"Srednia nagroda: {result['mean_reward']}")
        print(f"Skutecznosc decyzji: {result['accuracy_pct']}%")
        print(
            "Odsetek przeoczonych wad: "
            f"{result['missed_defect_rate_pct']}%"
        )
        print(
            "Odsetek blednych odrzucen: "
            f"{result['false_rejection_rate_pct']}%"
        )
        print(
            "Srednia liczba dodatkowych kontroli: "
            f"{result['mean_inspections']}"
        )

    print("\n" + "=" * 60)
    print("Zapisano wyniki w folderze results:")
    print("baseline_episodes.csv")
    print("baseline_summary.csv")


if __name__ == "__main__":
    main()
