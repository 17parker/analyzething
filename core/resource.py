import time
import os
import psutil  # lightweight library for memory tracking


def countdown_timer(seconds=60):
    """
    Runs a countdown timer for the given number of seconds.
    Prints remaining time and current memory usage each second.
    """
    process = psutil.Process(os.getpid())
    for remaining in range(seconds, 0, -1):
        mem_usage = process.memory_info().rss / (1024 * 1024)  # MB
        print(f"[TIMER] {remaining:2d}s left | Memory: {mem_usage:.2f} MB")
        time.sleep(1)

    print("[TIMER] Time budget expired!")
