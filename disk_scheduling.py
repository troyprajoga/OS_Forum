import sys


def read_requests(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file.readlines()]


def calculate_head_movements(requests, initial_position, algorithm):
    movements = 0
    current_position = initial_position

    if algorithm == "FCFS":
        for request in requests:
            movements += abs(request - current_position)
            current_position = request
    elif algorithm == "SCAN":
        sorted_requests = sorted(requests)
        left = [r for r in sorted_requests if r <= initial_position]
        right = [r for r in sorted_requests if r > initial_position]

        movements += abs(initial_position - left[0]) if left else 0
        movements += abs(left[-1] - right[0]) + sum(abs(right[i] - right[i+1]) for i in range(len(right) - 1)) if right else 0
    elif algorithm == "C-SCAN":
        sorted_requests = sorted(requests)
        left = [r for r in sorted_requests if r <= initial_position]
        right = [r for r in sorted_requests if r > initial_position]

        movements += sum(abs(current_position - r) for r in left[::-1]) if left else 0
        movements += 4999 - left[-1] + 4999 + sum(abs(right[i] - right[i+1]) for i in range(len(right) - 1)) if right else 0

    return movements


def optimized_scan(requests, initial_position):
    sorted_requests = sorted(requests)
    left = [r for r in sorted_requests if r <= initial_position]
    right = [r for r in sorted_requests if r > initial_position]

    movements = abs(initial_position - left[0]) if left else 0
    movements += abs(left[-1] - right[0]) + sum(abs(right[i] - right[i+1]) for i in range(len(right) - 1)) if right else 0

    return movements


def optimized_cscan(requests, initial_position):
    sorted_requests = sorted(requests)
    left = [r for r in sorted_requests if r < initial_position]
    right = [r for r in sorted_requests if r >= initial_position]

    movements = 0
    current_position = initial_position

    if right:
        movements += sum(abs(current_position - r) for r in right)
        if left:
            optimal_jump = min(left, key=lambda x: abs(4999 - x))
            movements += abs(right[-1] - optimal_jump)
            movements += sum(abs(x - left[i-1]) for i, x in enumerate(left, start=1))
    else:
        optimal_jump = min(left, key=lambda x: abs(4999 - x))
        movements += abs(current_position - optimal_jump)
        movements += sum(abs(x - left[i-1]) for i, x in enumerate(left, start=1))

    return movements


def optimized_fcfs(requests, initial_position):
    requests.sort()
    return calculate_head_movements(requests, initial_position, "FCFS")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python DiskScheduling.py <initial_position> requests.txt")
        sys.exit(1)

    initial_position = int(sys.argv[1])
    filename = sys.argv[2]

    requests = read_requests(filename)

    algorithms = ["FCFS", "SCAN", "C-SCAN"]
    for algo in algorithms:
        movements = calculate_head_movements(requests, initial_position, algo)
        print(f"{algo} Total Movements:", movements)


    print("Optimized SCAN Total Movements:", optimized_scan(requests, initial_position))
    print("Optimized C-SCAN Total Movements:", optimized_cscan(requests, initial_position))
    print("Optimized FCFS Total Movements:", optimized_fcfs(requests, initial_position))
