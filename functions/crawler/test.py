import time
import atexit
import sys

def handle_exit():
    time.sleep(0.5)
    print("exit success")
    sys.stdout.flush()

def main():
    while True:
        print("running")
        sys.stdout.flush()
        time.sleep(10)

if __name__ == "__main__":
    atexit.register(handle_exit)
    main()