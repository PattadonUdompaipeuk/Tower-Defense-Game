import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class GameDataGraphs:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def average_time_per_wave(self, ax):
        avg = self.data.groupby("wave")["time_spent_per_wave(s)"].mean()
        avg.plot(kind="line", ax=ax, marker="o")
        ax.set_title("Average Time per Wave")
        ax.set_xlabel("Wave"); ax.set_ylabel("Time (s)")

    def missed_enemy_per_wave(self, ax):
        missed = self.data.groupby("wave")["missed_enemies"].sum()
        bars = missed.plot(kind="bar", ax=ax)

        ax.set_title("Missed Enemies per Wave")
        ax.set_xlabel("Wave")
        ax.set_ylabel("Missed Enemies")

        for bar in bars.patches:
            bar.set_color("red")

    def tower_usage_ratio(self, ax):
        counts = self.data[["archer", "magic", "slow"]].sum()

        ax.pie(
            counts,
            labels=["Archer", "Magic", "Slow"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Tower Usage Ratio")
        ax.axis("equal")

    def money_distribution(self, ax):
        ax.boxplot(self.data["money_spent"], vert=False)
        ax.set_title("Distribution of Money Spent per Wave")
        ax.set_xlabel("Money Spent")

    def time_vs_kills(self, ax):
        ax.scatter(self.data["time_spent_per_wave(s)"], self.data["killed_enemies"], c="green")
        ax.set_title("Time vs Kills")
        ax.set_xlabel("Time (s)"); ax.set_ylabel("Killed Enemies")

    def summary_table(self) -> pd.DataFrame:
        summary = (
            self.data
            .groupby("wave")
            .agg({
                "killed_enemies": "mean",
                "missed_enemies": "mean",
                "money_spent": "mean",
                "archer": "mean",
                "magic": "mean",
                "slow": "mean",
                "time_spent_per_wave(s)": "mean"
            })
            .round(2)
            .reset_index()
        )
        return summary

    def create_summary_view(self, container):
        df = self.summary_table()
        cols = list(df.columns)
        tree = ttk.Treeview(container, columns=cols, show="headings")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        tree.pack(fill="both", expand=True)

    def create_graph(self, kind: str, container):
        for child in container.winfo_children():
            child.destroy()

        if kind == "Summary Table":
            self.create_summary_view(container)
        else:
            fig = plt.Figure(figsize=(6,4))
            ax = fig.add_subplot(111)
            if kind == "Average Time per Wave":
                self.average_time_per_wave(ax)
            elif kind == "Missed enemy per wave":
                self.missed_enemy_per_wave(ax)
            elif kind == "Tower Usage Ratio":
                self.tower_usage_ratio(ax)
            elif kind == "Distribution of Money Spent per Wave":
                self.money_distribution(ax)
            elif kind == "Time vs Kills":
                self.time_vs_kills(ax)

            canvas = FigureCanvasTkAgg(fig, master=container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

class Application(tk.Tk):
    def __init__(self, csv_file):
        super().__init__()
        self.title("Game Data Viewer")
        self.geometry("800x600")

        self.data = pd.read_csv(csv_file)
        self.graphs = GameDataGraphs(self.data)

        frame = ttk.LabelFrame(self, text="Select Graph or Table")
        frame.pack(fill="x", padx=10, pady=10)

        self.combo = ttk.Combobox(frame, state="readonly",
                                  values=["Summary Table",
                                          "Average Time per Wave",
                                          "Missed enemy per wave",
                                          "Tower Usage Ratio",
                                          "Distribution of Money Spent per Wave",
                                          "Time vs Kills"])
        self.combo.current(0)
        self.combo.pack(padx=5, pady=5)
        self.combo.bind("<<ComboboxSelected>>", self.on_select)

        self.graph_frame = ttk.Frame(self)
        self.graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.graphs.create_graph(self.combo.get(), self.graph_frame)

        self.quit_button = ttk.Button(self, text="Quit", command=self.destroy)
        self.quit_button.pack(padx=5, pady=5)

    def on_select(self, event):
        kind = self.combo.get()
        self.graphs.create_graph(kind, self.graph_frame)

def run_frame():
    app = Application("game_data.csv")
    app.mainloop()
