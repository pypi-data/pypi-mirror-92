from pathlib import Path
import time

def main():
    count = 0
    while True:
        Path('/home/volker/test.txt').touch()
        time.sleep(8)
        count += 1
        if count == 5:
            time.sleep(20)


if __name__ == '__main__':
    main()
