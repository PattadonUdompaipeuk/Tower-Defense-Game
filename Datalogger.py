import csv
import os

class DataLogger:
    def __init__(self, filename="game_data.csv"):
        self.filename = filename
        self.data_rows = []
        self.round_number = 1

        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as f:
                has_header = csv.Sniffer().has_header(f.read(1024))
                f.seek(0)
                if has_header:
                    reader = csv.DictReader(f)
                    try:
                        rounds = [int(row["round_number"]) for row in reader if row.get("round_number")]
                        if rounds:
                            self.round_number = max(rounds) + 1
                    except KeyError:
                        self.round_number = 1

    def log_wave(self, map_obj, tower_count, money_spent=0, time_spent=0):
        self.data_rows.append({
            "round_number": self.round_number,
            "wave": map_obj.wave,
            "killed_enemies": map_obj.killed_enemies,
            "missed_enemies": map_obj.missed_enemies,
            "money_spent": money_spent,
            "archer": tower_count.get("Archer", 0),
            "magic": tower_count.get("Magic", 0),
            "slow": tower_count.get("Slow", 0),
            "time_spent_per_wave(s)": round(time_spent, 2)
        })

    def save_to_csv(self):
        file_exists = os.path.exists(self.filename)
        with open(self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "round_number", "wave", "killed_enemies", "missed_enemies",
                "money_spent", "archer", "magic", "slow", "time_spent_per_wave(s)"
            ])
            if not file_exists:
                writer.writeheader()
            writer.writerows(self.data_rows)
        self.data_rows = []