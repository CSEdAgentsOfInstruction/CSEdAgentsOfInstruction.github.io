---
id: part-2/7-choosing-and-combining-repetition
part: 2
order: 7
title: Choosing and Combining Repetition
---

## Learning Objectives

- You can choose a loop form for a task and explain why it fits.
- You can split text into a list of strings and convert the items when you need numbers.
- You can compare corresponding or neighboring list items without using invalid indexes.
- You can combine input, lists, loops, and conditions in one program.

You now know several ways to repeat work. In this chapter, you will choose a loop that fits the task and use `.split()` to turn a line of text into a list.

## Turning Text into a List with `.split()`

`input(...)` returns one string even when the line contains several words. The string method `.split()` can put those words into a list:

Inside a Python string literal, `\t` represents one **tab character**. A tab is a kind of whitespace, like a space. You can run this example to see how `.split()` treats both:

```python runnable id=part-2-7-choosing-and-combining-repetition-example-1
text = "  red   green\tblue  "
colors = text.split()

print(colors)
```

The output is:

```text
['red', 'green', 'blue']
```

Without an argument, `.split()` separates at whitespace. Repeated spaces, tabs, and whitespace at the beginning or end do not create empty items. Text with no words produces an empty list.

The result is an ordinary list, so it can be processed with a loop:

```python
words = input("Words: ").split()

for word in words:
    print(len(word))
```

## Splitting at a Specific Separator

An argument to `.split(...)` selects an exact separator:

```python
text = "draft | review | publish"
steps = text.split("|")

print(steps)
```

This produces:

```text
['draft ', ' review ', ' publish']
```

The separator is removed, but surrounding spaces remain. Unlike `.split()` without an argument, `.split("|")` does not also treat whitespace specially. When those spaces are not part of the data, strip each item while processing it:

```python
for step in steps:
    print(step.strip())
```

Two adjacent separators also leave an empty string between them. For example, `"one,,three".split(",")` produces `['one', '', 'three']`. The next exercise avoids that case by guaranteeing a nonempty cargo name between every pair of commas.

Simple splitting is suitable for controlled text. Real file formats such as CSV have additional rules; later in the course, you will use tools designed for them.

:::exercise 016e603b-2135-452c-957a-f4e25720c8cb

## Choosing a Loop Form

Match the form of repetition to the information the task provides:

| Need | Typical form |
| --- | --- |
| process each item in a sequence | `for item in sequence` |
| work with or replace items by position | `for index in range(len(sequence))` |
| repeat a known number of times | `for ... in range(...)` |
| repeat until an input or event says to stop | `while True` with `break` |

For example, values are enough when printing every city:

```python
for city in cities:
    print(city)
```

Positions are needed when replacing items in an existing list:

```python
for index in range(len(stock)):
    if stock[index] == 0:
        stock[index] = 10
```

When there is no sequence but the count is known, `range(...)` can express the count directly. When neither a completed sequence nor a fixed count exists, user input can instead decide when a `while True` loop breaks.

These are guidelines, not laws. Prefer the form that makes the reason for repetition easiest to understand.

Match each task with the loop form that communicates its purpose most clearly.

:::exercise ada2f4c6-bb76-4478-8556-7bb62752d3c9

:::exercise a7baa4e4-15e2-4b41-8727-3b7b7176d21d

:::exercise 87cb3119-0089-4b70-9c0f-239fadb0d7dc

:::exercise 58b4659e-4eb9-45bd-8420-fd82caf428fc

## Combining Splitting and Repetition

The items produced by `.split()` are strings. Convert them when the program needs numbers:

```python
pieces = input("Prices: ").split()
prices = []

for piece in pieces:
    price = int(piece)
    prices.append(price)
```

Once conversion is complete, a second loop can process the numeric list:

```python
expensive_count = 0

for price in prices:
    if price >= 100:
        expensive_count = expensive_count + 1
```

Each loop has one job. The first turns the text pieces into numbers; the second counts prices of at least 100. If the input contains no words, both loops run zero times.

You could also update the count while converting the input. Both designs can work. In the next exercise, choose your own approach and explain to yourself what each loop does before writing it.

:::exercise 76120f21-4a6c-4018-9f93-8c6688d7961a

## Comparing Corresponding Items

Sometimes two lists describe the same positions. For example, one list can contain the words in a reference sentence while another contains the words someone typed. If the lists are equally long, an index can select the corresponding item from each list:

```python
reference_words = ["red", "green", "blue"]
typed_words = ["red", "blue", "green"]

for index in range(len(reference_words)):
    reference_word = reference_words[index]
    typed_word = typed_words[index]
    print(f"{reference_word}: {typed_word}")
```

The indexes start at zero and stop before `len(reference_words)`, so every valid position in that list is visited exactly once. This pattern requires `typed_words` to have the same length: an index that is valid for one list is not automatically valid for another. The next exercise guarantees equal word counts so that you can focus on the corresponding-position comparison.

Comparing the two current items is different from asking whether a word occurs anywhere in the other list: position matters. In the next exercise, the starter prepares the word lists, and your task is to count the matching positions.

:::exercise babaac83-2992-4e7f-a537-e58f725a7f5f

Why is checking corresponding positions different from checking whether a value occurs anywhere in another list?

## Comparing Neighboring Items

Some questions concern the relationship between consecutive items rather than one item at a time. For a list named `cards`, a comparison can use `cards[index]` and the item immediately to its right, `cards[index + 1]`.

The final card has no right-hand neighbor. Therefore, the useful left-hand positions come from:

```python
range(len(cards) - 1)
```

For five cards, this produces the indexes `0`, `1`, `2`, and `3`. Adding one gives the valid neighboring indexes `1`, `2`, `3`, and `4`; the loop never tries to read position `5`.

Practise this neighboring-item pattern in the next exercise. Combine the comparisons with the boolean flag from [Processing and Changing Lists](#/part-2/5-processing-and-changing-lists?anchor=remembering-whether-every-check-has-passed) to inspect a rack of cards. Before coding, identify the pairs you will compare and when the flag needs to change.

:::exercise 61d48d38-814e-41ce-a4cf-425fabb76e6f

Why does a neighboring-item loop use `range(len(values) - 1)` for its left-hand positions?

## Explain the Choice, Not Just the Syntax

A useful explanation connects the control structure to the job it performs. For example:

> The first loop uses `while True` because the user decides how many destinations to enter. After collection ends, the direct `for` loop visits every saved destination once, and no indexes are needed.

This says more than merely listing that the program contains `while`, `break`, and `for`. It explains what is known before each phase and why the chosen loop fits.

## Check Your Understanding

1. What does `.split()` produce, and what type does each resulting item have?
2. How does `.split(",")` differ from `.split()`?
3. When is direct iteration clearer than using indexes?
4. Which loop form naturally fits an interaction that continues until a stopping command?
5. Why might you collect values first and process the completed list in a separate loop instead of counting selected values during input?
