---
id: part-3/5-building-functions-with-lists
part: 3
order: 5
title: Building Functions with Lists
---

## Learning Objectives

- You can use a list parameter with familiar loop patterns.
- You can explain how the placement of `return` affects a loop.
- You can handle an empty list according to a stated requirement.
- You can use one function's returned value in another function.

[Names, Objects, and Mutable Lists](#/part-3/4-names-objects-and-mutable-lists?anchor=lists-as-function-arguments) explained what happens when a function receives a list. This chapter concentrates on the algorithms inside such functions: searches, empty inputs, and functions built from other functions.

## Familiar Loops Can Live Inside Functions

The selected-count pattern from Part 2 changes very little inside a function:

```python runnable id=part-3-5-building-functions-with-lists-example-1
def count_long_words(words, minimum_length):
    count = 0

    for word in words:
        if len(word) >= minimum_length:
            count = count + 1

    return count

words = ["ant", "elephant", "tiger", "ox"]
print(count_long_words(words, 5))
```

The function receives the list and boundary through parameters, calculates a count, and returns it. It does not decide how the result should be displayed.

## A `return` Ends the Current Call

[Parameters and Return Values](#/part-3/3-parameters-and-return-values?anchor=return-ends-the-current-call) established that `return` ends a function call immediately. Its position is especially important inside a loop:

```python
def contains_negative(values):
    for value in values:
        if value < 0:
            return True
        else:
            return False
```

This function examines only the first item. On the first iteration, one of the two returns always runs, so the call ends before the loop can reach later values.

Return `False` only after the loop finishes without finding a negative value:

```python
def contains_negative(values):
    for value in values:
        if value < 0:
            return True

    return False
```

The function may return `True` as soon as one negative value is found. It can return `False` only after the loop has checked every value without finding one.

For an empty list, the loop runs zero times and execution reaches `return False`. That matches the requirement: an empty list contains no negative value.

First, trace several return placements:

Then, write a function of your own for searching a list:

:::exercise 48f766af-dc3c-4457-b52a-406367b8cf37

## Empty Inputs Need Deliberate Behavior

Some list functions have a natural result for an empty list. A count or total can return `0`, and a search can return `False`.

Other calculations need a design decision:

```python
def largest_value(values):
    largest = values[0]

    for value in values:
        if value > largest:
            largest = value

    return largest
```

This function cannot use index `0` when `values` is empty. Possible designs include returning a special value or requiring a nonempty input. Returning `0` only to avoid the problem would be misleading: zero is not the largest member of an empty list.

A **precondition** states something that must be true before a function is called. For the version above, the precondition could be "`values` is nonempty." The caller must ensure that `values` is nonempty. If the list can be empty, handle that case before the call.

Use the stated requirement to decide whether the function accepts an empty list and what it should do with one. [Specifications, Verification, and AI](#/part-3/9-specifications-verification-and-ai?anchor=a-small-function-specification) looks more closely at writing these requirements.

## Functions Can Use Other Functions

Small functions can become building blocks:

```python
def total_values(values):
    total = 0

    for value in values:
        total = total + value

    return total

def average_value(values):
    total = total_values(values)
    return total / len(values)
```

`average_value` delegates summing to `total_values` and uses the returned number. This is **function composition**: one function call supplies information used by another calculation.

This version of `average_value` requires a nonempty list because an empty list has no average. Its caller must ensure that this precondition holds.

The next exercise combines several list calculations. Work on one function at a time and test ordinary cases. Test empty input where the contract accepts it; use nonempty lists for the average and summary functions. Then connect the returned results:

:::exercise 331fb3b3-d198-4046-aa8a-04cc237b743d

**Trace the Function Boundary**

For each call, identify:

1. which objects the argument expressions produce;
2. which local parameter names are bound to them;
3. where each possible `return` ends the call;
4. which value is returned to the caller.

## Check Your Understanding

1. Why does `count_long_words` receive both a list and a minimum length as parameters?
2. How can placing `return` inside a loop prevent later items from being checked?
3. How should a function's requirements guide its behavior when the list is empty?
4. How can one function use a value returned by another function?
