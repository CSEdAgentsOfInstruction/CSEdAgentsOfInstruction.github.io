---
id: part-2/8-recap-and-feedback
part: 2
order: 8
title: Recap
---

In this part, you learned to treat strings as sequences, repeat work with `for`, store several values in lists, process and change lists, and collect an unknown amount of input with `while True` and `break`.

The central idea is matching repetition to its job:

- use direct iteration when every existing item should be processed;
- use indexes when positions are needed;
- use `range(...)` when the repetition count is known;
- use `while True` with `break` when an interaction decides when to stop.

## Putting the Patterns Together

Larger programs often become easier to reason about when they are divided into phases. One loop can collect raw data, another can select the usable values, and a final loop can summarize them. Between phases, check what the lists contain and whether any of them are empty.

The summary must use only the values that passed the filter. For example, if the measurements are `4`, `-2`, and `0`, and negative measurements are invalid, the usable values are `4` and `0`. Their total is `4`, and their average is `2`. There are three entered measurements but only two valid ones.

A filtered list can be empty even when the original list contains several measurements. Then there is no average to calculate. Dividing by the length of that empty list would fail, so the program needs to handle this case separately.

The rainfall exercise applies that design to a familiar kind of measurement. It contains the full program requirements; use the patterns from the earlier chapters to decide what belongs in each phase.

:::exercise 0dd5abed-9b40-4866-8fab-e95f0ebfe435

## Compare Finished Designs

Two programs can produce the same result while storing different values. Compare what each program remembers, how it handles the case with no valid measurements, and when each design might be useful.

## Check Your Understanding

1. What do strings and lists have in common as sequences?
2. When does a loop need an index rather than only the current value?
3. What is the purpose of `break` in a sentinel loop?
4. How can filtering a nonempty list produce an empty list?
5. Why should immediate stopping and empty-list behavior be considered deliberately?

## Looking Ahead

Programs with several phases can grow into one long block of code. In Part 3, you will learn how **functions** divide a program into smaller pieces with clear responsibilities. You will also learn tools for responding safely when input cannot be converted to the expected type.
