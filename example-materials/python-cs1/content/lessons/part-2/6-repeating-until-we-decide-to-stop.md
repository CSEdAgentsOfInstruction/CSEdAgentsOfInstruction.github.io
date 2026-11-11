---
id: part-2/6-repeating-until-we-decide-to-stop
part: 2
order: 6
title: Repeating Until We Decide to Stop
---

## Learning Objectives

- You can use `while True` to start repetition whose length is not known beforehand.
- You can use `break` to leave a loop when a stopping condition is reached.
- You can collect an unknown number of user inputs into a list.
- You can explain the different roles of `while True` and `for` in a data-entry program.
- You can reason about what happens when the user stops immediately.

A `for` loop works especially well when there is already a sequence to process:

```python
for score in scores:
    print(score)
```

Sometimes that sequence does not exist yet. A program might need to ask for tasks until the user enters an empty line. The program cannot know beforehand whether the user will enter two tasks, five tasks, or none.

This is a natural use for a `while` loop.

## Repeating Without Knowing the Count

```python runnable id=part-2-6-repeating-until-we-decide-to-stop-example-1
tasks = []

while True:
    task = input("Task (empty to stop): ")

    if task == "":
        break

    tasks.append(task)

print(tasks)
```

The condition in `while True` is always true, so the loop needs an explicit way to stop. Here, the empty string is a **sentinel**: a special value that ends input and is not part of the collected data.

When `break` runs, Python immediately leaves the loop and continues with the first statement after it. Read the structure as:

> Ask for a value. If it means "stop," leave the loop. Otherwise, remember it and repeat.

Follow the input value, the collected list, and the stopping decision in execution order.

:::exercise ab77eb58-fd0b-49d6-a0c9-e090c8c66a26

:::exercise aaea9368-eab1-4b01-8c61-77c0735d7608

## Keep the Sentinel Out of the Data

The order inside the loop matters. Each iteration should:

1. read the next value;
2. check whether it is the sentinel and break if it is;
3. append it only when it is actual data.

If the append happens before the check, the stopping value becomes part of the list. If the user enters the sentinel immediately, the correctly ordered loop runs once but leaves the list empty.

:::exercise 7accfc72-b984-4c72-a9e1-d40b4d360ffc

## A Text Sentinel with Numeric Data

When the data is numeric but the sentinel is a word, keep the input as text until after the stopping check:

```python
lap_times = []

while True:
    text = input("Lap time (finished to stop): ").strip().lower()

    if text == "finished":
        break

    lap_times.append(float(text))
```

Calling `.strip().lower()` lets inputs such as ` Finished ` work as the same command. The stopping command never reaches `float(...)`; every other entry is passed to it for conversion.

During Parts 1 and 2, you may assume that values expected to be numeric are entered in a valid numeric form. Part 3 introduces more systematic validation and exception handling.

:::exercise e9fe994b-d577-4f49-8e4d-b924e4e19731

## A Numeric Sentinel

A reserved number can also signal the end of input. When input is guaranteed to be numeric, convert it first and then compare the number with the sentinel:

```python
distances = []

while True:
    distance = float(input("Distance (-1 to stop): "))

    if distance == -1:
        break

    distances.append(distance)
```

Because the comparison happens after conversion, `-1` and `-1.0` represent the same numeric sentinel. The reserved value cannot also be used as data, and it must still be checked before appending.

## Collect First, Process Afterwards

After the collection loop ends, there is a completed list to process. That suggests two loops with different jobs:

- a `while True` loop collects an amount of input that is not known in advance;
- a `for` loop later visits each item in the completed list once.

Before collection, you do not know how many values the user will enter. Once it ends, you can process the completed list without asking for more input.

A music-request kiosk collects song requests until the user enters `done`, and then displays the saved requests. Review the loop chosen for each phase.

:::exercise 9480f91d-a52d-42a0-a0ec-7290c3c9341a

:::exercise 04bf76da-0ef9-4851-b8eb-7dcd798cea99

:::exercise 1bf1f38d-0b60-480c-a376-3be47526f4fb

## Summarizing Collected Data

Suppose the earlier loop has finished collecting `lap_times`. A separate loop can calculate their total:

```python
total_time = 0

for lap_time in lap_times:
    total_time = total_time + lap_time

print(f"Number of laps: {len(lap_times)}")
print(f"Total time: {total_time}")
```

If the user stopped immediately, `lap_times` is empty. The `for` loop then runs zero times, so `total_time` remains `0`. A program should handle this case deliberately unless its task guarantees at least one item.

:::exercise e6e89857-58c3-4a3e-9882-0410249733d0

## What `break` Skips

`break` skips the rest of its current loop body as well as all later iterations:

```python
while True:
    action = input("Action: ").strip().lower()

    if action == "exit":
        break

    print(f"Accepted: {action}")

print("Goodbye.")
```

For the stopping input, the `Accepted` line does not run. The `Goodbye` line does run because it is after the loop. Trace statements in execution order: indentation shows whether a statement is inside or after the loop.

In the next questions, trace how statement order affects what happens on the stopping iteration.

Predict what runs before, during, and after the stopping iteration.

:::exercise 2cbe60d1-3a00-4c57-b310-3014b8cc5d4a

**A Focused Use of while**

Python allows many conditions after `while`. In this part, you will mainly use `while True` with `break` when the input says to stop.

The loop can **keep asking for input without knowing how many values the user will provide**.

## Check Your Understanding

1. Why does `while True` need some reachable way to execute `break`?
2. Why is the sentinel normally checked before `.append(...)`?
3. Why must a word sentinel be checked before converting numeric data?
4. Why is a `for` loop often a good choice after collection finishes?
5. What happens when the user enters the sentinel on the first iteration?
