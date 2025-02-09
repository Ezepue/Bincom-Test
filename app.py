import random
import psycopg2
from collections import Counter
import statistics

data = {
    "MONDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "TUESDAY": "ASH, BROWN, GREEN, BROWN, BLUE, BLUE, BLUE, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE",
    "WEDNESDAY": "GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE",
    "THURSDAY": "BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN",
    "FRIDAY": "GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE"
}

all_colors = []
for day, color_str in data.items():
   all_colors.extend(color_str.split(", "))

    
# Count Occurances
color_counts = Counter(all_colors)

# Mean Color Computation
mean_frequency = sum(color_counts.values()) / len(color_counts)
mean_color = min(color_counts.keys(), key=lambda x: abs(color_counts[x] - mean_frequency))

# Calculate Mode Colour
mode_color = color_counts.most_common(1)[0][0]

# Calculate Median
sorted_colors = sorted(all_colors)

def find_median_color(colors):
    n = len(colors)
    if n % 2 == 1:
        return colors[n // 2]
    else:
        return colors[n // 2 - 1]

median_color = find_median_color(sorted_colors)

# Variance of Color Occurrences
values = list(color_counts.values())
variance = statistics.variance(values)

# Calculate The Probability
total_colors = len(all_colors)
red_count = all_colors.count("RED")
probability_red = red_count / total_colors

# Save the colours and their frequencies in postgresql database
def save_to_db(color_counts):
    try:
        conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
        )
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS color_counts (color TEXT, frequency INTEGER)""")
        conn.commit()
        
        insert_query = "INSERT INTO colors (color, frequency) VALUES (%s, %s)"
        for color, frequency in color_counts.items():
            cursor.execute(insert_query, (color, frequency))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print("Database error:", e)
        
# Generate random 4-bit binary and convert to base 10
random_binary_number = "".join(str(random.randint(0, 1)) for _ in range(4))
base_10 = int(random_binary_number, 2)

# Sum of First 50 Fibonacci numbers
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

fibonacci_total = fibonacci_sum(50)

# Print results
print("Mean Color:", mean_color)
print("Mode Color:", mode_color)
print("Median Color:", median_color)
print("Variance of Colors:", variance)
print("Probability of picking RED:", probability_red)
print("Random Binary Number:", random_binary_number, "Base 10:", base_10)
print("Sum of first 50 Fibonacci numbers:", fibonacci_total)

# Save to database
save_to_db(color_counts)