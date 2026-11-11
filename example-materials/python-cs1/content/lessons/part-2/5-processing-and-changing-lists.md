---
id: part-2/5-processing-and-changing-lists
part: 2
order: 5
title: Processing and Changing Lists
---

## Learning Objectives

- You can write loops that calculate a result or build a new list, choosing a suitable starting value.
- You can use a boolean flag to remember whether every item passes a condition.
- You can use indexes to replace items in a list.
- You can explain how replacing an item differs from changing a list's length during iteration.
- You can trace and test list-processing loops, including boundary values and empty lists.

A list remembers several values. A loop can apply the same rule to each of them.

In [Repeating over a Sequence](#/part-2/3-repeating-over-a-sequence?anchor=remembering-across-iterations), you already learned one important loop pattern by counting characters. The patterns in this chapter are extensions of the same idea: initialize some state, process the items one at a time, and update the state when necessary.

The chapter has two main stages:

1. **Processing values and remembering results:** calculate a result, answer a question, or build a new list.
2. **Replacing items by position:** use indexes when the task requires changing items in an existing list.

## Processing Values and Remembering Results

### Calculating a Total

Suppose you have several reading-session lengths:

```python
minutes = [25, 40, 15, 30]
```

To calculate the total, start from zero and add each value:

```python runnable id=part-2-5-processing-and-changing-lists-example-1
minutes = [25, 40, 15, 30]
total = 0

for value in minutes:
    total = total + value

print(total)
```

The output is:

```text
110
```

The changing state is `total`:

| `value` | `total` afterwards |
| ---: | ---: |
| 25 | 25 |
| 40 | 65 |
| 15 | 80 |
| 30 | 110 |

This is often called an **accumulator** pattern because the variable accumulates a result across iterations.

The next starter reads words into a list. Calculate how many characters those words contain altogether.

:::exercise 51e43ea0-5a56-459d-8b4c-30cbd1cf0aab

### Counting Selected Values

You have already counted selected characters. The same pattern works with list items:

```python
ratings = [5, 2, 4, 5, 3]
recommended_count = 0

for rating in ratings:
    if rating >= 4:
        recommended_count = recommended_count + 1

print(recommended_count)
```

The counter works in the same way whether its input is a string or a list. You can reuse the idea by changing what each iteration checks.

Now use a list of words to answer a different question: how many words contain at least five characters?

:::exercise 1863f769-13d9-4e7f-b4fe-fadafeb6c8f6

### Finding the Largest Value

For a non-empty list, one straightforward approach is to start with the first item as the current best candidate:

```python
distances = [14, 9, 18, 11]
longest = distances[0]

for distance in distances:
    if distance > longest:
        longest = distance

print(longest)
```

The output is `18`.

On the first iteration, the first value is compared with itself. That comparison is unnecessary, but harmless. Keeping the loop this way makes the code simple: every value is processed by the same loop.

This version assumes that the list is not empty because `distances[0]` requires a first item. A program that may receive an empty list must handle that case separately.

The same idea finds the smallest value by reversing the comparison.

Starting from the first item is important. Starting from `0` is not correct for every list:

```python
distances_below_sea_level = [-14, -5, -9]
highest = 0  # Incorrect: 0 is not one of the values.

for distance in distances_below_sea_level:
    if distance > highest:
        highest = distance

print(highest)
```

This program prints `0`, even though the largest item is `-5`. None of the negative values can replace the incorrect starting value. In contrast, starting with the first item gives the loop a real candidate and works for all-negative data as well.

Trace, diagnose, and implement a best-so-far loop.

:::exercise 143c7e1b-2b39-4ccd-bb9a-79e1f542544c

:::exercise 2ed4d5be-5914-46e4-8c89-ce67675f0f3e

### Building a New List

A program can collect selected values into a new list:

```python
package_weights = [1.2, 4.5, 2.8, 6.0]
heavy_weights = []

for weight in package_weights:
    if weight >= 4:
        heavy_weights.append(weight)

print(heavy_weights)
```

The output is:

```text
[4.5, 6.0]
```

Keep separate records of the two lists as you trace this example. Follow how `weight` receives each input item while only the values that pass the condition are appended to `heavy_weights`. The original list does not change.

```python runnable id=part-2-5-processing-and-changing-lists-trace-1
package_weights = [1.2, 4.5, 2.8, 6.0]
heavy_weights = []

for weight in package_weights:
    if weight >= 4:
        heavy_weights.append(weight)

print(heavy_weights)
```

Following the statements in execution order produces:

```text
[4.5, 6.0]
```

Selecting some input items and collecting them in a new list is often called **filtering**. The pattern has a clear structure:

1. start with an empty result list;
2. inspect each input item;
3. append the items that satisfy the rule.

Filtering is also useful for a small search: inspect each archive title and collect the ones containing a search term. The next exercise keeps the original titles intact while building a separate result list.

:::exercise 77d25f3f-c6da-4887-a157-ddb209fa581d

The examples so far used different kinds of remembered state. Before comparing them side by side, check that you can choose a suitable starting value for each job.

Choose a suitable starting value for the result each loop needs to remember.

:::exercise c9396cd1-7c29-48c2-80ad-0f8e51be968d

:::exercise 2ed21086-c9ad-45c4-97c0-d58215bdea5d

:::exercise b69e0480-7eb5-4d5c-959b-ce9dd809a889

:::exercise e6ec73fa-827a-4059-96d3-bee5a2121fde

### Remembering Whether Every Check Has Passed

Sometimes a program needs one final yes-or-no result for a whole sequence. A boolean variable can remember whether every item checked so far has passed:

```python runnable id=part-2-5-processing-and-changing-lists-example-2
temperatures = [4, 7, -2, 8]
all_non_negative = True

for temperature in temperatures:
    if temperature < 0:
        all_non_negative = False

print(all_non_negative)
```

The flag starts as `True` because no failing value has been found yet. The value `-2` makes it `False`. The later value `8` passes the check, but it must not reset the flag: a passing value does not undo an earlier failure.

An empty list leaves the flag as `True` because no value failed the check.

Trace the flag in the next exercise, then find a repair for a second version of the loop.

Repair a loop that updates a Boolean flag. Trace the flag after each value to check your repair.

:::exercise 9c4adb6e-a798-49cf-a3d5-9a40a0b46a47

### A Map of the Value-Processing Patterns

Each pattern begins by answering the same question:

> What should the remembered result be before any items have been processed?

| Pattern | Purpose | Initial state | Update during the loop | Result for an empty sequence |
| --- | --- | --- | --- | --- |
| Total | Combine numeric values | `total = 0` | Add every value | `0` |
| Selected count | Count matching values | `count = 0` | Add `1` when an item matches | `0` |
| Best so far | Find a minimum or maximum | `best = values[0]` | Replace it when a better item appears | Must be handled separately |
| New result list | Collect selected or changed values | `result = []` | Append an appropriate item | `[]` |
| Every value passes | Check a condition for the whole sequence | `all_pass = True` | Set to `False` when a value fails | `True`: no value failed |

The initial state is part of the algorithm, not just setup. For example, `0` is a sensible total before any values are added, but it is not necessarily a value that can serve as a minimum or maximum.

**Built-ins and Learning the Pattern**

Python provides built-in functions for several common summaries:

```python
total = sum(values)
smallest = min(values)
largest = max(values)
```

In everyday programs, these built-ins are often the clearest choice. Here, you implement the operations with loops so that you can see how state is initialized, checked, and updated. The same reasoning will later help with calculations for which there is no ready-made built-in.

Like the loop versions that start from `values[0]`, `min(values)` and `max(values)` require the empty case to be considered separately. Calling either function with an empty list raises a `ValueError`.

## Pause and Check Your Progress

Before moving on, check that you can answer these two questions:

1. A list contains only negative values. What starting value would you use when calculating its total, and what would you use when finding its largest value? What changes if the list is empty?
2. A flag starts as `True` and becomes `False` when an item fails a check. What should happen when a later item passes? What result should an empty list give?

If either question is difficult, return to the relevant example and try different values. This is a useful place to take a break; the next section adds a different job for indexes.

## Replacing Items by Position

### Sometimes You Need the Position

Direct iteration is usually the clearest choice:

```python
for score in scores:
    print(score)
```

But consider a different task:

> Reduce every stored price by one.

The loop variable gives you each value, but assigning to that variable does not replace the item in the list:

```python
prices = [10, 15, 8]

for price in prices:
    price = price - 1

print(prices)
```

The list is still:

```text
[10, 15, 8]
```

On each iteration, `price` was assigned a smaller number. That assignment did not replace the corresponding item in `prices`.

To replace items, you need their indexes.

### Combining `range(...)` and `len(...)` for Indexes

In [Repeating over a Sequence](#/part-2/3-repeating-over-a-sequence?anchor=using-range-values-as-indexes), you used `range(len(word))` to visit each valid string position. Lists use the same zero-based positions. Here, those positions let a program replace the stored items rather than only read their values.

So:

```python
range(len(prices))
```

provides exactly the indexes needed to visit every position in `prices`.

```python
prices = [10, 15, 8]

for index in range(len(prices)):
    prices[index] = prices[index] - 1

print(prices)
```

The output is:

```text
[9, 14, 7]
```

This is an **index-based loop**.

The whole list changes one position at a time. Predict the value at each index after each assignment, then run the program to check the final list.

```python runnable id=part-2-5-processing-and-changing-lists-trace-2
prices = [10, 15, 8]

for index in range(len(prices)):
    prices[index] = prices[index] - 1

print(prices)
```

Following the statements in execution order produces:

```text
[9, 14, 7]
```

The same changes can be summarized in a table:

| `index` | Old value | New value | `prices` afterwards |
| ---: | ---: | ---: | --- |
| 0 | 10 | 9 | `[9, 15, 8]` |
| 1 | 15 | 14 | `[9, 14, 8]` |
| 2 | 8 | 7 | `[9, 14, 7]` |

**Use Indexes When They Serve a Purpose**

Do not replace every direct `for` loop with `range(len(...))`.

If you only need each value, prefer:

```python
for price in prices:
```

If you need the position itself, or need to replace items at those positions, an index-based loop may be appropriate:

```python
for index in range(len(prices)):
```

The goal is not to use the most complicated loop form. The goal is to express the task clearly.

Practise updating list items by position. First trace some updates, then write a loop to clean up a list of readings.

Trace energy readings as they change, then write a loop to clean up invalid readings.

:::exercise 8a67139a-e13c-46b9-9ca8-e43f127426b4

### Do Not Change a List's Length While Traversing It

Replacing list items does not add or remove positions. In this example, the list has three items before, during, and after the loop:

```python
numbers = [2, 4, 6]

for index in range(len(numbers)):
    numbers[index] = numbers[index] * 2
```

Changing the **structure** of the list being traversed is different. For example, do not run this loop:

```python
numbers = [2, 4, 6]

for number in numbers:
    numbers.append(number + 1)  # Incorrect: the list keeps growing.
```

The loop reaches newly appended items and appends still more items. It does not finish normally. Other changes to a list's length can make items move and cause a loop to skip or revisit them.

A loop over `range(len(numbers))` behaves differently: Python determines the range before the loop begins. Appending an item does not extend that range, so the loop does not visit the newly appended positions. Finishing the loop does not show that every item in the resulting list was processed.

When a task needs a different number of items, build a separate result list instead:

```python
numbers = [2, 4, 6]
with_successors = []

for number in numbers:
    with_successors.append(number)
    with_successors.append(number + 1)

print(with_successors)
```

The original list remains stable while the loop traverses it. This is the same safe idea used earlier when building `heavy_weights`.

**Replacement or Structural Change?**

- Replacing `values[index]` changes the item at an existing position without changing the list's length.
- Appending or removing items changes the list's structure. Do not do that to the list currently being traversed; collect the desired items in a separate list.

## Verify Repeated State Changes

When a loop produces the wrong result, the final value does not always show which iteration went wrong. A temporary `print` inside the loop can make its decisions visible.

The following program should count readings that are **at least 10**. Before running it, predict which readings appear in the debug output and what the final count will be:

```python
readings = [9, 10, 14, 6]
count = 0

for reading in readings:
    if reading > 10:
        print(f"DEBUG counting {reading}")
        count = count + 1

print(f"Readings at least 10: {count}")
```

Run the program and compare its output with the requirement:

```text
DEBUG counting 14
Readings at least 10: 1
```

The final line shows that the count is wrong: both `10` and `14` should count. The debug line tells us which value actually reached the update. The missing `10` points us toward the condition, where `>` excludes the boundary. Change the comparison to `>=` and run the same input again.

Choose a debug print that answers a particular question. Printing inside the matching branch shows which items cause an update. Printing the remembered state after the loop shows the result before later code uses it. If the updates themselves are suspect, print the current item and the remembered value just after each update.

Try the repaired loop with an empty list, with no matching readings, and with several readings equal to `10`. Predict the output before each run. Then remove the temporary debug print; ordinary output should contain only what the program or exercise requires.

Use the same observations when checking code from someone else, including an AI assistant. The loop's actual decisions should agree with the stated rule.

Trace how loops change stored lists, and repair programs to produce the required results.

:::exercise f95811c5-c5fe-41eb-80f9-3eec58db390a

:::exercise 4fec3d26-0a57-4fcd-99de-10779927a8ff

:::exercise 40923a1b-d083-4e0a-be4a-ee07846e402b

:::exercise 36ebd9b2-4821-40e7-a607-9edc138a4ac2

## Check Your Understanding

1. Why does assigning `score = score + 1` inside `for score in scores` not replace the list item?
2. When is `for index in range(len(values))` preferable to direct iteration?
3. Why is replacing `values[index]` different from appending to `values` while a loop traverses it?
4. Why can a loop over `range(len(values))` stop even when its body appends to `values`?
5. How would you test a loop intended to replace negative values with zero? Include boundary values and an empty list.
