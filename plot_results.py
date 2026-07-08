import matplotlib.pyplot as plt
import csv


def generate_graphs():
    try:
        # קריאת הנתונים מה-CSV שיצרנו
        data = []
        with open('experiment_results.csv', mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # דילוג על שורת הכותרות
            for row in reader:
                if not row or "Total Time" in row[0]:
                    break  # הגענו לשורת הסיכום הריקה
                data.append(row)

        if not data:
            print("No data found in CSV.")
            return

        # הכנת הנתונים לגרף
        labels = [f"{row[0]}\nvs\n{row[1]}" for row in data]
        p1_wins = [int(row[2]) for row in data]
        p2_wins = [int(row[3]) for row in data]
        draws = [int(row[4]) for row in data]

        x = range(len(labels))
        width = 0.25

        # יצירת הגרף
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.bar([i - width for i in x], p1_wins, width, label='Agent 1 Wins', color='#4CAF50')
        ax.bar(x, p2_wins, width, label='Agent 2 Wins', color='#F44336')
        ax.bar([i + width for i in x], draws, width, label='Draws', color='#9E9E9E')

        # עיצוב אקדמי ונקי
        ax.set_ylabel('Number of Wins / Games')
        ax.set_title('Tournament Results: Agent Performance Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()

        # שמירת הגרף כתמונה
        plt.savefig('tournament_chart.png', dpi=300)
        print("Chart saved successfully as 'tournament_chart.png'")
        plt.show()

    except FileNotFoundError:
        print("Error: 'experiment_results.csv' not found. Please run evaluate.py first.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    generate_graphs()