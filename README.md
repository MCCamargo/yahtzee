# Yahtzee

A web-based implementation (try it [here](https://mccamargo.github.io/yahtzee/?api=https://yahtzee-api-mauroccamargo.fly.dev)) of a variant of the classic dice game **Yahtzee**. Python backend written by me, html frontend almost entirely written by LLMs.

Players roll six dice, hold the ones they want, and select scoring categories — aiming for the highest total score possible. The variation from the classic rules comes from the possibility of saving "extra rolls" for later turns.

---

## How to play:

1. Start a new game by clicking on "New Game" button.
2. Roll dice using the "Roll" button. Click on a die to hold it (i.e. it won't be rolled, so you "keep" the number it is showing).  
3. Click on an unscored category in the scorecard to score it. The best score possible for the category (with the dice you have) will be computed automatically.
4. The game ends when all categories have been filled.  

---

## Scoring rules

| Category | Description |
|-----------|-------------|
| **Ones – Sixes** | Score the sum of dice showing that number. |
| **Pair** | Score the sum of the values of a pair of matching dice. |
| **Two Pair** | Sum of two different pairs. |
| **Three of a Kind** | Sum of three matching dice. |
| **Four of a Kind** |Sum of four matching dice. |
| **Full House** | 3 of one number + 2 of another. |
| **Small Straight** | Sequence 1–2–3–4–5 (15 points). |
| **Large Straight** | Sequence 2–3–4–5–6 (20 points). |
| **Yahtzee** | All six dice are the same (scores 100 points, regardless of the specific value all dice show). |
| **Chance** | Sum of all dice values. |
| **Upper Section Bonus** | +50 points for scoring ≥73 points in Ones–Sixes section. |

---
