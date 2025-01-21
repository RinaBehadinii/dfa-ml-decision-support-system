import os

import pandas as pd

from modules.constants import CSV_FILE, user_feedback

if os.path.exists(CSV_FILE):
    wardrobe_data = pd.read_csv(CSV_FILE)
else:
    raise FileNotFoundError(f"The file '{CSV_FILE}' was not found. Please ensure it exists.")


class DFA:
    def __init__(self, max_colors=3):
        self.states = ['q0', 'q1', 'q2', 'q3', 'q_reject']
        self.current_state = 'q0'
        self.used_colors = set()
        self.outfit = []
        self.max_colors = max_colors
        self.transitions = {
            'q0': {'Top': 'q1', 'Bottom': 'q_reject', 'Outerwear': 'q_reject'},
            'q1': {'Bottom': 'q2', 'Top': 'q_reject', 'Outerwear': 'q_reject'},
            'q2': {'Outerwear': 'q3', 'Top': 'q_reject', 'Bottom': 'q_reject'},
            'q3': {'Top': 'q_reject', 'Bottom': 'q_reject', 'Outerwear': 'q_reject'},
            'q_reject': {'Top': 'q_reject', 'Bottom': 'q_reject', 'Outerwear': 'q_reject'},
        }

    def reset(self):
        self.current_state = 'q0'
        self.used_colors.clear()
        self.outfit.clear()

    def transition(self, item):
        next_state = self.transitions.get(self.current_state, {}).get(item['category'])
        if next_state and next_state != 'q_reject':
            self.current_state = next_state
            self.outfit.append(item['item'])
            self.used_colors.add(item['color'])
            return True
        else:
            self.current_state = 'q_reject'
            return False

    def validate_colors(self):
        return len(self.used_colors) <= self.max_colors

    def select_outfit(self, weather):
        self.reset()
        filtered_items = wardrobe_data[(wardrobe_data['weather'] == weather) | (wardrobe_data['weather'] == 'All')]

        if filtered_items.empty:
            return "Error: No items available for the selected weather."

        filtered_items = filtered_items.sample(frac=1).reset_index(drop=True)
        attempts = 0

        while attempts < 10:
            self.reset()
            selected_categories = set()

            for category in ['Top', 'Bottom', 'Outerwear']:
                category_items = filtered_items[filtered_items['category'] == category]

                if category_items.empty:
                    continue

                weights = [user_feedback.get(item['item'], 1) for _, item in category_items.iterrows()]
                category_items = category_items.sample(n=len(category_items), weights=weights, random_state=1)

                for _, item in category_items.iterrows():
                    if len(self.used_colors) < self.max_colors or item['color'] in self.used_colors:
                        if self.transition(item):
                            selected_categories.add(category)
                            break

            if len(self.outfit) >= 2 and len(selected_categories) >= 2 and self.validate_colors():
                if self.current_state == 'q3':
                    return self.outfit

            attempts += 1

        return "Error: Unable to create a valid outfit with the given constraints."
