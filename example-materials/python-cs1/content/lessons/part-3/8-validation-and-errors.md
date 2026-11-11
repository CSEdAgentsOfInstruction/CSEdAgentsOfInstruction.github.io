---
id: part-3/8-validation-and-errors
part: 3
order: 8
title: Validation and Errors
---

## Learning Objectives

- You can distinguish text that cannot be converted to an integer from an integer that is outside an allowed range.
- You can handle `ValueError` with a `try` block focused on the conversion.
- You can trace how `continue` starts another attempt in an input loop.
- You can write an input function that asks again until it can return a valid value.

Part 2 used input loops such as:

```python
while True:
    text = input("Value, or done: ").strip().lower()

    if text == "done":
        break

    value = float(text)
```

Those examples assumed that anything other than `done` was numeric. Real users may enter something else.

This chapter focuses on **user-input validation**: converting a user's text, checking whether the resulting value is acceptable for the task, and asking again when it is not.

What happens here?

```python
value = float("hello")
```

Python cannot convert this text. It raises **`ValueError`**; if nothing handles the error, the program stops with a traceback.

## Exceptions Report That an Operation Could Not Be Completed

An **exception** signals that an operation failed while the program was running. For example:

```python
int("hello")
```

cannot perform the requested conversion.

Different problems produce different exception types. You do not need to memorize them; the important point is to catch the specific failure your program knows how to recover from. This chapter focuses on invalid conversion and `ValueError`.

## Catching a `ValueError`

Use `try` and `except` when the program can respond meaningfully to a particular failure:

```python runnable id=part-3-8-validation-and-errors-example-1
text = input("Integer: ")

try:
    number = int(text)
except ValueError:
    print("That was not an integer.")
```

> Try this operation. If it raises `ValueError`, run the recovery block instead of ending the program.

On success, `number` refers to the integer and `except` is skipped. The retry loop below shows how to use `number` only after success.

If the conversion fails, Python jumps to:

```python
except ValueError:
```

and runs its block.

An optional sign is valid integer text: for example, `int("-4")` produces `-4`. Conversion answers whether the text represents an integer; a program can separately decide later whether a negative integer is acceptable for its purpose.

## Catch the Error You Expect

Different operations can fail in different ways. An `except ValueError` handler responds to that exception type; it does not handle every error raised inside its `try` block.

Consider this version:

```python
try:
    number = int(input("Number: "))
    result = 100 / number
    print(result)
except ValueError:
    print("Not an integer")
```

The handler is intended for invalid integer text, but `try` also contains division and printing. Input `0` converts successfully, then the division raises `ZeroDivisionError`. The `ValueError` handler does not catch it: zero is an integer, but it cannot be used as the divisor here.

Keep only the conversion inside the `try` block so it is clear which failure the handler is meant to recover from. If another operation in a larger block also raised `ValueError`, the same handler would catch it and could mistake a programming error for invalid input.

Use `except ValueError` rather than a bare `except:` for this recovery. A bare handler also catches unrelated errors, which can hide a programming mistake behind an invalid-input message.

The retry-loop example below keeps the block focused and uses `number` only after a successful conversion.

## Ask Again Until the Input Is Valid

The `while True` pattern from Part 2 now becomes especially useful. Python's `continue` statement immediately starts the next iteration of the surrounding loop:

```python runnable id=part-3-8-validation-and-errors-example-2
while True:
    text = input("Integer: ")

    try:
        number = int(text)
    except ValueError:
        print("Please enter an integer.")
        continue

    break

print(f"Accepted: {number}")
```

Enter `hello` and `42` on separate lines in the input box before running this example. Trace how `text` changes after each input. The expected output below shows only the messages from `print`; Run also displays the `Integer: ` prompts.

```python runnable id=part-3-8-validation-and-errors-trace-1
while True:
    text = input("Integer: ")

    try:
        number = int(text)
    except ValueError:
        print("Please enter an integer.")
        continue

    break

print(f"Accepted: {number}")
```

Following the statements in execution order produces:

```text
Please enter an integer.
Accepted: 42
```

The first conversion fails before assigning `number`. Using that name at this point would raise `NameError`, even after the handler printed its message. Here, `continue` skips `break` and starts another attempt. The next conversion succeeds, so execution reaches `break` and then prints the accepted number.

Unlike a sentinel loop, this loop ends when conversion succeeds.

Trace how `continue` skips the rest of one iteration and begins the next attempt.

:::exercise 2c9a675a-9074-4c75-8319-8f1393a48733

## Put Reusable Validation in a Function

If several parts of a program need integer input, copying the loop each time creates duplication.

Give the behavior a name:

```python
def read_integer(prompt):
    while True:
        text = input(prompt)

        try:
            number = int(text)
        except ValueError:
            print("Please enter an integer.")
            continue

        return number
```

Now:

```python
age = read_integer("Age: ")
score = read_integer("Score: ")
```

Each call asks until it can return an integer. Failure reaches `continue`; success reaches `return`, which ends the call and gives the integer to the caller.

This is a useful combination of ideas from the part:

- a function owns one responsibility: obtaining a valid integer;
- `while True` repeats until success;
- `try` handles a failed conversion;
- `return` hands the valid result back to the caller.

## Conversion Validation and Domain Validation Are Different

Suppose `read_integer` successfully returns `-5`.

The input was valid **as an integer**, but `-5` may still be invalid for a particular purpose such as age or number of study minutes.

For example:

```python
def read_nonnegative_integer(prompt):
    while True:
        text = input(prompt)

        try:
            number = int(text)
        except ValueError:
            print("Please enter an integer.")
            continue

        if number >= 0:
            return number

        print("Please enter zero or a positive integer.")
```

The function handles two requirements:

- **conversion validation:** can this text become the requested type?
- **domain validation:** is the resulting value acceptable for this task?

Conditions handle the second; exceptions help with the first.

## Testing Validation Logic

A call that waits for `input(...)` needs someone to supply input. A calculation function can be tested by giving it arguments and checking its result with an assertion.

For example, a rule about acceptable ages can be placed in an ordinary calculation function:

```python
def valid_age(age):
    return age >= 0 and age <= 130

assert valid_age(25) == True
assert valid_age(0) == True
assert valid_age(130) == True
assert valid_age(-1) == False
assert valid_age(131) == False
```

These assertions are development-time tests of the age rule. They do not validate what a user types. The `try`, `except`, and `if` statements in `read_age` perform that job while the program is running.

The input function can use the same rule:

```python
def read_age():
    while True:
        text = input("Age: ")

        try:
            age = int(text)
        except ValueError:
            print("Please enter an integer.")
            continue

        if valid_age(age):
            return age

        print("Please enter an age between 0 and 130.")
```

**Put rules expressible as ordinary inputs and outputs into ordinary functions, because those functions are easy to test.**

:::exercise c4b5b8aa-98ce-43b1-ac04-fe6f525e5f11

## Check Your Understanding

1. What does a `ValueError` mean in the context of `int(text)` or `float(text)`?
2. What happens when the code inside a `try` block raises the exception named by its `except` block?
3. How can `while True`, `try`, `continue`, and `return` work together in an input function?
4. What is the difference between checking whether text can be converted to an integer and checking whether the resulting integer is a valid age?
5. Why is `except ValueError` usually preferable to a bare `except` for numeric input conversion?
