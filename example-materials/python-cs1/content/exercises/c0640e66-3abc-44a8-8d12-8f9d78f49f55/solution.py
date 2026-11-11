def read_sessions():
    sessions = []

    while True:
        text = input("Minutes, or done: ").strip()

        if text.lower() == "done":
            break

        try:
            minutes = int(text)
        except ValueError:
            print("Please enter a positive integer or done.")
            continue

        if minutes <= 0:
            print("Please enter a positive integer or done.")
            continue

        sessions.append(minutes)

    return sessions


def total_minutes(sessions):
    total = 0

    for minutes in sessions:
        total = total + minutes

    return total


def longest_session(sessions):
    if len(sessions) == 0:
        return 0

    longest = sessions[0]

    for minutes in sessions:
        if minutes > longest:
            longest = minutes

    return longest


def count_long_sessions(sessions, minimum_minutes):
    count = 0

    for minutes in sessions:
        if minutes >= minimum_minutes:
            count = count + 1

    return count


def print_summary(session_count, total, longest, long_count):
    print(f"Sessions: {session_count}")
    print(f"Total minutes: {total}")

    if session_count == 0:
        print("Longest session: none")
    else:
        print(f"Longest session: {longest}")

    print(f"Long sessions: {long_count}")


def main():
    sessions = read_sessions()
    total = total_minutes(sessions)
    longest = longest_session(sessions)
    long_count = count_long_sessions(sessions, 30)
    print_summary(len(sessions), total, longest, long_count)


if __name__ == "__main__":
    main()
