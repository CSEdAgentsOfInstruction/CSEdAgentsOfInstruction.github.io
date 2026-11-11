---
id: part-3/6-designing-programs-from-functions
part: 3
order: 6
title: Designing Programs from Functions
---

## Learning Objectives

- You can identify separate responsibilities inside a longer script.
- You can refactor familiar logic into functions without changing its intended behavior.
- You can separate user interaction from calculation logic.
- You can use function names and return values to make the high-level flow of a program visible.
- You can recognize when creating an extra function would not make a small program clearer.

You can now define functions, pass arguments, and return results. The next question is which parts of a program should become functions. A useful function normally has one understandable responsibility.

## Start from the Jobs the Program Performs

Consider this Part 2-style program:

```python
sessions = []

while True:
    text = input("Minutes, or done: ").strip().lower()

    if text == "done":
        break

    minutes = int(text)
    sessions.append(minutes)

long_sessions = []

for minutes in sessions:
    if minutes >= 30:
        long_sessions.append(minutes)

total = 0

for minutes in sessions:
    total = total + minutes

print(f"Sessions: {len(sessions)}")
print(f"Total minutes: {total}")
print(f"Long sessions: {len(long_sessions)}")
```

The script has three jobs:

1. collect sessions;
2. calculate information about them;
3. print the summary.

Each job suggests a possible function.

## Give a Calculation a Name

Start with a small, self-contained calculation:

```python
def total_minutes(sessions):
    total = 0

    for minutes in sessions:
        total = total + minutes

    return total
```

The caller can now write:

```python
total = total_minutes(sessions)
```

Although Python has `sum(...)`, this version shows the design principle: the loop becomes a named operation.

The same can be done for the long-session count:

```python
def count_long_sessions(sessions, minimum_minutes):
    count = 0

    for minutes in sessions:
        if minutes >= minimum_minutes:
            count = count + 1

    return count
```

The main program no longer needs the calculation details.

## Separate Interaction from Calculation

User interaction is often easier to change when it is kept separate from calculation logic.

Compare these two designs.

### Mixed together

```python
def show_total():
    first = int(input("First: "))
    second = int(input("Second: "))
    print(first + second)
```

This function is tied to those prompts and that output format.

### Separated

```python
def add(first, second):
    return first + second

first = int(input("First: "))
second = int(input("Second: "))
result = add(first, second)
print(result)
```

The second design makes `add` reusable:

```python
print(add(2, 3))
print(add(10, -4))
```

It is also easier to test because calling `add` does not wait for keyboard input.

> Keep calculation functions dependent on parameters and return values when possible. Keep keyboard input and printing in the interaction code, and pass the collected values to calculation functions.

Functions named `read_sessions` and `print_summary` can reasonably interact with the user. Their names should make that responsibility explicit.

## A Function for Collecting Data

Part 2 introduced `while True` and `break` for open-ended input. That whole interaction can be given a name:

```python
def read_sessions():
    sessions = []

    while True:
        text = input("Minutes, or done: ").strip().lower()

        if text == "done":
            break

        minutes = int(text)
        sessions.append(minutes)

    return sessions
```

The main program can now begin with:

```python
sessions = read_sessions()
```

At this boundary:

- the caller passes no arguments to `read_sessions`;
- the function still obtains information by calling `input(...)`;
- a list of session lengths comes out.

Calling `input(...)` is an interaction, not a function argument. The loop is an implementation detail hidden behind `read_sessions`.

This version still assumes that every entry other than `done` is a valid integer. [Validation and Errors](#/part-3/8-validation-and-errors?anchor=put-reusable-validation-in-a-function) removes that simplifying assumption and shows how the function can ask again after invalid input.

## A Function for Presenting a Result

Printing can also be a clear responsibility. In this version, the caller calculates the values and the printing function only presents them:

```python
def print_summary(session_count, total, long_count):
    print(f"Sessions: {session_count}")
    print(f"Total minutes: {total}")
    print(f"Long sessions: {long_count}")
```

Then the main program makes the calculation and presentation phases visible:

```python
sessions = read_sessions()
total = total_minutes(sessions)
long_count = count_long_sessions(sessions, 30)
print_summary(len(sessions), total, long_count)
```

The logic now sits behind names describing the program's phases. Other designs are possible, but here `print_summary` has one responsibility and the main flow shows where calculations happen.

Review which information should cross each function boundary in a small festival program.

:::exercise 0636b45b-6807-4efe-9df4-62c32b9d9775

:::exercise 145216f9-ae83-457b-acc4-066f079a8ae8

:::exercise 3372478c-96e3-4309-813c-ef420cb305cc

## Refactoring a Program in Stages

**Refactoring** means changing the structure of code while preserving its intended, observable behavior.

If the original script works, extract one responsibility, run the program, and then continue.

For the session program above, run a few input sequences before editing and keep the output. After replacing the inline total loop with a call to `total_minutes`, run the same inputs again:

| Responses, one per line | Sessions | Total minutes | Long sessions |
| --- | ---: | ---: | ---: |
| `done` | 0 | 0 | 0 |
| `20`, `done` | 1 | 20 | 0 |
| `20`, `30`, `45`, `done` | 3 | 95 | 2 |

Check that the three printed summary lines still agree with these results before extracting another piece. If a result changes, inspect the most recent edit first.

## A Main Function Can Reveal the Program's Story

The session summary now shows the work in order: read the sessions, calculate the results, and print them. A reader can follow these calls and inspect a helper's body when they need the details.

You can give the high-level flow itself a function named `main`. For the session summary, keep the helper definitions shown earlier in this chapter. Replace the top-level input, calculation, and printing statements with the following definition and call:

```python
def main():
    sessions = read_sessions()
    total = total_minutes(sessions)
    long_count = count_long_sessions(sessions, 30)
    print_summary(len(sessions), total, long_count)

main()
```

`main` is an ordinary function that coordinates the program. The call at the end starts its work. If you omit the call, none of the statements inside `main` run.

## Do Not Turn Every Few Lines into a Function

Over-decomposition can make a program harder to follow too.

Consider:

```python
def add_one(number):
    return number + 1

def show_number(number):
    print(number)

def increase_and_show(number):
    number = add_one(number)
    show_number(number)
```

These valid functions may add more navigation than clarity in a tiny program.

A useful question is not:

> Can these lines technically be moved into a function?

Instead ask:

> Does naming this piece make the program easier to understand, test, reuse, or change?

Good programmers may reasonably choose different boundaries.

## Function Names Should Describe Responsibilities

Compare a vague name such as `process` with names such as `replace_negative_values_with_zero` and `average_temperature`. `process` says very little. A precise name tells a reader what role the function plays. The name should also match the exact behavior: a function that replaces values with zero should not be called `remove_negative_values`.

Names such as these often work well:

- `read_scores`;
- `count_vowels`;
- `calculate_average`;
- `is_valid_guess`;
- `select_passing_scores`;
- `print_summary`.

Review how the functions divide input, calculation, and presentation:

Review two proposed refactorings of a decomposed program.

:::exercise 12dd0ec6-6f1c-415e-b6a0-df5f4c1a61d8

:::exercise c4e6e50b-6991-46a9-b834-8058ca9f4dde

Now refactor a working program. Choose a calculation to give its own helper function, and check that the program still produces the same output after each change.

:::exercise 021b9d25-79d3-42b1-9026-1463a04d139b

## Check Your Understanding

1. What does refactoring mean?
2. Why are calculation functions often easier to test when they do not call `input(...)`?
3. What information comes into and out of `read_sessions` in the example above?
4. How can function names make the high-level flow of a program easier to see?
5. Why is creating the largest possible number of functions not a useful goal?
