import os

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from modules.constants import FEEDBACK_FILE, user_feedback


def train_model():
    if os.path.exists(FEEDBACK_FILE):
        feedback_df = pd.read_csv(FEEDBACK_FILE)
        feedback_df['Feedback'] = feedback_df['Feedback'].map({'like': 1, 'dislike': 0})
        feedback_df['Top'] = feedback_df['Top'].astype('category').cat.codes
        feedback_df['Bottom'] = feedback_df['Bottom'].astype('category').cat.codes
        feedback_df['Outerwear'] = feedback_df['Outerwear'].astype('category').cat.codes

        X = feedback_df[['Top', 'Bottom', 'Outerwear']]
        y = feedback_df['Feedback']

        model = DecisionTreeClassifier()
        model.fit(X, y)
        return model
    return None


def update_feedback(top, bottom, outerwear, feedback):
    feedback_entry = {'Top': top, 'Bottom': bottom, 'Outerwear': outerwear, 'Feedback': feedback}

    if not os.path.exists(FEEDBACK_FILE):
        pd.DataFrame([feedback_entry]).to_csv(FEEDBACK_FILE, index=False)
    else:
        feedback_df = pd.read_csv(FEEDBACK_FILE)
        feedback_df = pd.concat([feedback_df, pd.DataFrame([feedback_entry])], ignore_index=True)
        feedback_df.to_csv(FEEDBACK_FILE, index=False)

    feedback_value = 1 if feedback == 'like' else -1
    user_feedback[top] = user_feedback.get(top, 1) + feedback_value
    user_feedback[bottom] = user_feedback.get(bottom, 1) + feedback_value
    user_feedback[outerwear] = user_feedback.get(outerwear, 1) + feedback_value
