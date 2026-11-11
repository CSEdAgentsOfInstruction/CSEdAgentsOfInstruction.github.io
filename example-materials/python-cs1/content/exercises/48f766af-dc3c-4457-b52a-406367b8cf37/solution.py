def contains_signal(messages, signal):
    for message in messages:
        if message == signal:
            return True

    return False

