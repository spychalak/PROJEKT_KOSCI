import json
import os
import pickle

MODEL_DIR = "models"
QTABLE_PATH = f"{MODEL_DIR}/rl_qtable.pkl"
META_PATH = f"{MODEL_DIR}/rl_meta.json"


def model_exists():
    return os.path.exists(QTABLE_PATH) and os.path.exists(META_PATH)


def save_model(Q, epsilon, episodes):
    os.makedirs(MODEL_DIR, exist_ok=True)

    with open(QTABLE_PATH, "wb") as f:
        pickle.dump(Q, f)

    with open(META_PATH, "w") as f:
        json.dump({
            "epsilon": epsilon,
            "episodes": episodes
        }, f)


def load_model():
    with open(QTABLE_PATH, "rb") as f:
        Q = pickle.load(f)

    with open(META_PATH, "r") as f:
        meta = json.load(f)

    return Q, meta["epsilon"], meta["episodes"]