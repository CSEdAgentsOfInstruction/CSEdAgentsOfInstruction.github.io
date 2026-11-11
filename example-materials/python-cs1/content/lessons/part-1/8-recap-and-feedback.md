---
id: part-1/8-recap-and-feedback
part: 1
order: 8
title: Recap
---

In this part, you learned to write small interactive Python programs. You worked with input and output, text and numbers, variables, expressions, and decisions. You also practised predicting output, tracing changing values, explaining behavior, and modifying one part of a larger program.

You should now be able to combine these ideas in a complete short program. If an exercise reveals something you do not yet understand, return to the relevant chapter and try its examples again.

## The Core Ideas in One Program

Consider this program:

```python
name = input("Name: ").strip()
age = int(input("Age: "))
hours = float(input("Hours studied this week: "))

target_reached = hours >= 5

if age < 18:
    group = "under 18"
else:
    group = "adult"

print(f"{name}: {group}")

if target_reached:
    print("Weekly study target reached.")
else:
    print("Weekly study target not reached yet.")
```

This small program contains many of the ideas from the part:

- input;
- strings;
- numeric conversion;
- variables;
- a boolean value;
- comparisons;
- two separate decisions;
- f-string output.

A useful final check is whether you can trace it without running it first.

## Parcel Delivery Quote

The following exercise brings together input, numeric calculations, text normalization, decision boundaries, and formatted output.

:::exercise 92ee07d5-3fee-4e5b-ac2e-cb2064728ffb

## Looking Ahead

In Part 2, you will learn how programs can repeat actions and work with several values. Loops, lists, and closer study of strings will let you build programs that do more than handle one set of inputs at a time.
