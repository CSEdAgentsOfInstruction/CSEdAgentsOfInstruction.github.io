---
id: part-3/1-overview
part: 3
order: 1
title: Overview
---

In Part 2, you learned to collect an unknown amount of input, store several values in lists, process them with loops, and build new results one item at a time.

## From Loops to Functions

A longer program can become difficult to read even when each of its loops works correctly.

**Functions** let you give a piece of behavior a name. A function can receive information, perform one job, and return a result. In this part, you will use functions to divide longer programs into understandable responsibilities.

Consider this program, which collects measurements and then summarizes them:

```python
measurements = []

while True:
    text = input("Measurement, or done: ").strip().lower()

    if text == "done":
        break

    measurement = float(text)
    measurements.append(measurement)

usable = []

for measurement in measurements:
    if measurement >= 0:
        usable.append(measurement)

if len(usable) == 0:
    print("No usable measurements")
else:
    total = 0

    for measurement in usable:
        total = total + measurement

    average = total / len(usable)
    print(f"Average: {average}")
```

For now, assume that every entry other than `done` is a valid number. Later in this part, you will learn how to respond when a user types something that cannot be converted to a number.

In Part 2, you divided programs like this into phases. This program has four jobs:

- reading input;
- selecting usable values;
- calculating a summary;
- presenting the result.

Once a function works, the rest of the program can use it without repeating its implementation.

You have already used functions throughout the course:

```python
print("Hello")
name = input("Name: ")
length = len(name)
```

Someone else defined `print`, `input`, and `len`. In this part, you will begin defining functions of your own.

Functions also make another important programming habit much easier: **testing**. Instead of running an entire interactive program and manually checking everything, you can call one calculation function with a known input and check whether it returns the expected result.

You will continue to check explanations and AI-generated code against a program's behavior. For a function, ask:

> **Does this function actually satisfy the behavior that was requested?**

After working through this part, you should be able to **write, trace, test, and explain programs built from functions, with clear inputs, results, and handling of invalid input**.

The structure of this part is as follows:

- [Defining and Calling Functions](#/part-3/2-defining-and-calling-functions) introduces your own function definitions and separates defining a function from running it.
- [Parameters and Return Values](#/part-3/3-parameters-and-return-values) introduces arguments, parameters, returned values, and the difference between returning and printing.
- [Names, Objects, and Mutable Lists](#/part-3/4-names-objects-and-mutable-lists) explains how names refer to values and why changing a shared list differs from reassigning a local name.
- [Building Functions with Lists](#/part-3/5-building-functions-with-lists) applies familiar loops inside functions and examines searches, empty inputs, and function composition.
- [Designing Programs from Functions](#/part-3/6-designing-programs-from-functions) uses functions to separate larger programs into understandable phases and responsibilities.
- [Testing Functions](#/part-3/7-testing-functions) introduces `assert` and systematic checks for normal, boundary, empty, and refactoring cases.
- [Validation and Errors](#/part-3/8-validation-and-errors) introduces `try` and `except` for input that cannot be converted to the expected type.
- [Specifications, Verification, and AI](#/part-3/9-specifications-verification-and-ai) makes function behavior explicit before implementation and uses specifications and tests to evaluate generated code.
- [Recap](#/part-3/10-recap-and-feedback) brings the ideas together in a larger reading-tracker exercise.

## Recommended Order of Work

A useful rhythm for this part is:

1. read each chapter in order;
2. type and run the examples rather than only reading them;
3. complete the exercises as you go;
4. when a function call is confusing, trace the values passed in, any changes made, and the returned result;
5. when you write a function, test it with more than one kind of input;
6. finish with the recap.

After [Names, Objects, and Mutable Lists](#/part-3/4-names-objects-and-mutable-lists), pause to check that you can trace a function call, distinguish printing from returning, and explain whether a list argument changes. Those ideas will help you build the larger programs later in the part.

When writing a function, ask three questions:

> **What is this function responsible for?**  
> **What information does it need?**  
> **What does it give back?**
