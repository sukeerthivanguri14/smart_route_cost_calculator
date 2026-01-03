
import tkinter as tk
from tkinter import messagebox
import webbrowser
import heapq

# Manhattan distance between two points
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Convert grid (x, y) to latitude and longitude
def grid_to_latlng(x, y, origin_lat=17.3850, origin_lng=78.4867, step=0.001):
    lat = origin_lat + y * step
    lng = origin_lng + x * step
    return f"{lat:.6f},{lng:.6f}"

# Dijkstra algorithm to compute minimum cost
def compute_min_cost(start, target, special_roads):
    points = {start, target}

    for a, b, _ in special_roads:
        points.add(a)
        points.add(b)

    min_cost = {p: float('inf') for p in points}
    min_cost[start] = 0

    heap = [(0, start)]

    while heap:
        cost, curr = heapq.heappop(heap)

        if curr == target:
            return cost

        if cost > min_cost[curr]:
            continue

        # Direct move to target
        direct_cost = cost + manhattan(curr, target)
        if direct_cost < min_cost[target]:
            min_cost[target] = direct_cost
            heapq.heappush(heap, (direct_cost, target))

        # Use special roads
        for a, b, special_cost in special_roads:
            move_cost = cost + manhattan(curr, a)
            total_cost = move_cost + special_cost

            if total_cost < min_cost[b]:
                min_cost[b] = total_cost
                heapq.heappush(heap, (total_cost, b))

    return -1

# Button action
def open_map():
    try:
        start = tuple(map(int, start_entry.get().strip().split(',')))
        target = tuple(map(int, target_entry.get().strip().split(',')))

        special_roads = []
        raw = special_entry.get().strip()

        if raw:
            for item in raw.split(';'):
                road = list(map(int, item.strip().split(',')))
                if len(road) != 5:
                    raise ValueError("Each special road must have 5 integers")
                special_roads.append(
                    ((road[0], road[1]), (road[2], road[3]), road[4])
                )

        cost = compute_min_cost(start, target, special_roads)

        if cost == -1:
            messagebox.showinfo("Result", "Target is not reachable")
            return

        rate_per_unit = 10
        price = cost * rate_per_unit

        messagebox.showinfo(
            "Travel Cost",
            f"Minimum cost: {cost} units\nEstimated price: ₹{price}"
        )

        origin = grid_to_latlng(*start)
        destination = grid_to_latlng(*target)

        url = (
            f"https://www.google.com/maps/dir/?api=1"
            f"&origin={origin}&destination={destination}"
        )

        if special_roads:
            waypoints = [
                grid_to_latlng(x2, y2) for _, (x2, y2), _ in special_roads
            ]
            url += "&waypoints=" + "|".join(waypoints)

        webbrowser.open(url)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# GUI setup
root = tk.Tk()
root.title("Grid Path Cost Calculator")

tk.Label(root, text="Start (x,y):").grid(row=0, column=0, padx=10, pady=5)
start_entry = tk.Entry(root, width=25)
start_entry.grid(row=0, column=1)
start_entry.insert(0, "0,0")

tk.Label(root, text="Target (x,y):").grid(row=1, column=0, padx=10, pady=5)
target_entry = tk.Entry(root, width=25)
target_entry.grid(row=1, column=1)
target_entry.insert(0, "6,6")

tk.Label(
    root,
    text="Special Roads (x1,y1,x2,y2,cost;...)"
).grid(row=2, column=0, padx=10, pady=5)

special_entry = tk.Entry(root, width=40)
special_entry.grid(row=2, column=1)
special_entry.insert(0, "0,0,2,2,1;2,2,5,5,2")

tk.Button(
    root,
    text="Compute Cost & Open Map",
    command=open_map
).grid(row=3, column=0, columnspan=2, pady=15)

root.mainloop()
