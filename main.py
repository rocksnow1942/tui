import time

import rich.progress as rich_progress


def progress() -> None:
    for _ in rich_progress.track(range(100), description="Processing..."):
        time.sleep(0.02)


def main():
    progress()


if __name__ == "__main__":
    main()
