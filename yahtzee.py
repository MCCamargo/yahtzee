from flask import Flask, jsonify
from flask_cors import CORS
import random
from typing import List, Dict

class Die:
    def __init__(self):
        self.value = 1
        self.held = False
    
    def roll(self):
        if not self.held:
            self.value = random.randint(1, 6)
    
    def toggle_hold(self):
        self.held = not self.held
    
    def to_dict(self):
        return {
            "value": self.value,
            "held": self.held
        }

class Scorecard:
    def __init__(self):
        self.scores = {
            "ones": None,
            "twos": None,
            "threes": None,
            "fours": None,
            "fives": None,
            "sixes": None,
            "pair":None,
            "two_pair": None,
            "three_of_a_kind": None,
            "four_of_a_kind": None,
            "full_house": None,
            "small_straight": None,
            "large_straight": None,
            "yahtzee": None,
            "chance": None
            }
        self.upper_bonus = False
        
    def is_game_over(self) -> bool:
        #app.logger.info(f"Checking game over. Scores: {self.scores}")  # Debug log
        is_over = all(score is not None for score in self.scores.values())
        #app.logger.info(f"Game over status: {is_over}")  # Debug log
        return is_over
        
    def get_upper_section_total(self) -> int:
        upper_categories = ["ones", "twos", "threes", "fours", "fives", "sixes"]
        return sum(self.scores[category] or 0 for category in upper_categories)
    
    def check_upper_bonus(self) -> bool:
        if not self.upper_bonus and self.get_upper_section_total() >= 73:
            self.upper_bonus = True
            return True
        return False
        
    def calculate_score(self, category: str, dice: List[Die]) -> int:
        values = [die.value for die in dice]
        value_counts = {i: values.count(i) for i in range(1, 7)}
        
        
        if category in ["ones", "twos", "threes", "fours", "fives", "sixes"]:
            number = {"ones": 1, "twos": 2, "threes": 3, "fours": 4, "fives": 5, "sixes": 6}[category]
            
            return sum(v for v in values if v == number)
        
        
        # problem in scoring full house
        
        elif category == "pair":
            if max(value_counts.values()) >= 2:
                for i in range(6,0, -1):
                    if value_counts[i] >= 2:
                        return 2*i
            return 0
        # treats four of a kind as 0
        elif category == "two_pair":
            
            pairs = [value for value, count in value_counts.items() if count >= 2]
            if len(pairs) >= 2:
                pairs.sort(reverse=True)
                score = (pairs[0] * 2) + (pairs[1] * 2)
                return score
            return 0
            
            
        elif category == "three_of_a_kind":
            if max(value_counts.values()) >= 3:
                for i in range(6,0,-1):
                    if value_counts[i] >= 3:
                        return 3*i                       
            return 0
            
        elif category == "four_of_a_kind":
            if max(value_counts.values()) >= 4:
                for i in range(6,0,-1):
                    if value_counts[i] >= 4:
                        return 4*i
            return 0
        
        # change to actual score?
        elif category == "full_house":
            if 2 in value_counts.values() and 3 in value_counts.values():
                
                candidates = [(value, count) for value, count in value_counts.items() if count >= 2]
                
                candidates.sort(reverse = True)
                
                if candidates[0][1] >= 3:
                    return 3*candidates[0][0] + 2*candidates[1][0]
                else:
                    return 2*candidates[0][0] + 3*candidates[1][0]
              
            elif 3 in value_counts.values():
                candidates = [(value, count) for value, count in value_counts.items() if count >= 3]
                
                if len(candidates) <= 1:
                    return 0
                
                candidates.sort(reverse = True)
                
                return 3*candidates[0][0] + 2*candidates[1][0]
                
            return 0
            
        
        elif category == "small_straight":
            sorted_values = sorted(list(set(values)))
            if len(sorted_values) >= 5 and sorted_values[0] == 1 and sorted_values[4] == 5:
                return 15
          
            return 0
        
        elif category == "large_straight":
            value_set = set(values)
            for i in range(2,7):
                if i not in value_set:
                    return 0
            return 20
            
        elif category == "yahtzee":
            if max(value_counts.values()) == 6:
                return 100
            return 0
            
        elif category == "chance":
            return sum(values)
            
        return 0

    def score_category(self, category: str, dice: List[Die]) -> bool:
        if self.scores[category] is not None:
            return False
        self.scores[category] = self.calculate_score(category, dice)
        
        return True
    
    def get_total(self) -> int:
        base_total = sum(score for score in self.scores.values() if score is not None)
        self.check_upper_bonus()
        bonus = 50 if self.upper_bonus else 0
        return base_total + bonus
        
    def to_dict(self):
        return {
            "scores": self.scores,
            "total": self.get_total(),
            "upper_section_total": self.get_upper_section_total(),
            "upper_bonus": self.upper_bonus,
            "upper_bonus_threshold": 73
        }

class Game:
    def __init__(self):
        self.dice = [Die() for _ in range(6)]
        self.rolls_left = 3
        self.saved_rolls = 0
        self.scorecard = Scorecard()
        self.current_turn_scored = False
        self.game_started = False
        
    
    def roll_dice(self) -> bool:
        self.game_started = True
        if self.current_turn_scored:  # reset everything on new roll after scoring
            self.rolls_left = 3
            self.current_turn_scored = False
            for die in self.dice:
                die.held = False
            
        if self.rolls_left > 0:
            for die in self.dice:
                die.roll()
            self.rolls_left -= 1
            return True
        elif self.saved_rolls > 0:
            for die in self.dice:
                die.roll()
            self.saved_rolls -= 1
            return True
        return False
    
    def toggle_hold(self, die_index: int) -> bool:
        if 0 <= die_index < 6 and self.rolls_left < 3:
            self.dice[die_index].toggle_hold()
            return True
        return False
    
    def score(self, category: str) -> str:  # Changed return type to str
        if not self.game_started:
            return "game_not_started"
            
        if self.current_turn_scored:
            return "turn_scored"
            
        if self.rolls_left > 0:
            self.saved_rolls += self.rolls_left
            
        success = self.scorecard.score_category(category, self.dice)
        if success:
            self.current_turn_scored = True
            self.rolls_left = 3
            for die in self.dice:
                die.held = False
            return "success"
        return "category_used"
    
    def to_dict(self):
        return {
            "dice": [die.to_dict() for die in self.dice],
            "rolls_left": self.rolls_left,
            "saved_rolls": self.saved_rolls,
            "scorecard": self.scorecard.to_dict()
        }

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["https://mccamargo.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Store active games (in a real app, this would be a database)
games = {}

@app.route('/game/new', methods=['POST'])
def new_game():
    game_id = len(games)
    games[game_id] = Game()
    return jsonify({"game_id": game_id})

@app.route('/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(games[game_id].to_dict())

@app.route('/game/<int:game_id>/roll', methods=['POST'])
def roll_dice(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    
    success = games[game_id].roll_dice()
    if not success:
        return jsonify({"error": "No rolls left"}), 400
    
    return jsonify(games[game_id].to_dict())

@app.route('/game/<int:game_id>/hold/<int:die_index>', methods=['POST'])
def toggle_hold(game_id, die_index):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    
    success = games[game_id].toggle_hold(die_index)
    if not success:
        return jsonify({"error": "Invalid die index or first roll"}), 400
    
    return jsonify(games[game_id].to_dict())

@app.route('/game/<int:game_id>/score/<category>', methods=['POST'])
def score_category(game_id, category):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404
    
    game = games[game_id]
    result = game.score(category)
    if result == "game_not_started":
        return jsonify({"error": "Roll the dice to start!"}), 400
    elif result == "turn_scored":
        return jsonify({"error": "You already scored this turn! Roll again for a new turn."}), 400
    elif result == "category_used":
        return jsonify({"error": "This category has already been scored"}), 400
    
    # Debug logs
    app.logger.info("Checking if game is over...")
    if game.scorecard.is_game_over():
        app.logger.info("Game is over! Sending final score")
        response_data = {
            "game_over": True,
            "final_score": game.scorecard.get_total(),
            "game_state": game.to_dict()
        }
        app.logger.info(f"Response data: {response_data}")
        return jsonify(response_data)
    
    return jsonify(game.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
