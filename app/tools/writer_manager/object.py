import json
import threading


class WriterManager:
    def __init__(self, states_path):
        self.states_path = states_path
        self.lock = threading.Lock()
        self.states = self._load_states()

    def _load_states(self):
        try:
            with open(self.states_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def update_state(self, topic, state):
        with self.lock:
            self.states[topic] = state

    def save_states(self):
        with self.lock:
            with open(self.states_path, 'w') as file:
                json.dump(self.states, file, indent=4)

    def write_state(self, topic, state):
        with self.lock:
            self.states[topic] = state
            with open(self.states_path, 'w') as file:
                json.dump(self.states, file, indent=4)
