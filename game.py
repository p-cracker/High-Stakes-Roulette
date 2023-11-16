import random
import os
import ctypes
import subprocess
import sys
import platform


def run_as_superuser():
    try:
        # If on Windows
        if platform.system() == 'Windows':
            ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                " ".join(sys.argv),
                None,
                1  # SW_SHOWNORMAL
            )
            sys.exit(0)

        # If not running as root on Linux
        elif os.geteuid() != 0:
            subprocess.check_call(['sudo', sys.executable] + sys.argv)
            sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def russian_roulette():
    drum_size = 6
    hammer_position = 1
    bullet_position = random.randint(1, drum_size)
    your_turn = True

    while True:
        print("\nDrum:", "0 " * (hammer_position - 1),
              "? " * (drum_size - (hammer_position - 1)))

        # Reset on the last position
        if hammer_position == drum_size:
            print("\nLast slot. Spinning the drum.")
            hammer_position = 1
            bullet_position = random.randint(1, drum_size)

        if not your_turn:
            print("\nSteve's turn.")
            if steve_turn(drum_size, bullet_position):
                print("\nSteve pulls the trigger")
                if hammer_position == bullet_position:
                    print("\nBang! Steve loses.")
                    return
                else:
                    print("\nClick! Steve is safe.")
            else:
                print("\nSteve points at you and pulls the trigger")
                if hammer_position == bullet_position:
                    print("\nBang! You lose.")
                    delete_random_file()
                    return
                else:
                    print("\nClick! You are safe. Steve loses.")
                    return
            your_turn = True
            input("Press Enter to continue...")
        else:
            your_turn = not your_turn
            print("1. Press the trigger")
            print("2. Shoot at Steve")

            choice = int(input("Your choice (1 or 2): "))
            if choice == 1:

                if hammer_position == bullet_position:
                    print("\nBang! You lose.")
                    delete_random_file()
                    return
            elif choice == 2:
                print("You shoot at Steve...")
                if hammer_position == bullet_position:
                    print("\nBang! Steve loses.")
                    return
                else:
                    print("\nClick! Steve is safe. You lose.")
                    delete_random_file()
                    return

        hammer_position += 1


def steve_turn(drum_size, hammer_position):
    # Probability of the bullet being in the next slot
    probability = 1 / (drum_size - hammer_position + 1)
    # Simulate Steve's decision with a random roll
    return random.random() <= probability


def list_files(folder_path):
    all_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files


def delete_random_file():
    if platform.system() == 'Windows':
        path = "C:\\Windows\\System32\\"
    else:
        path = "/boot/"
    files = list_files(path)
    if files:
        file_to_delete = random.choice(files)
        # os.remove(file_to_delete)
        print(f"\nOops! File '{file_to_delete}' went missing.")
    else:
        print("\nNo files to delete.")


run_as_superuser()
russian_roulette()
