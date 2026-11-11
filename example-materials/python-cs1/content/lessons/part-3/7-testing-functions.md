---
id: part-3/7-testing-functions
part: 3
order: 7
title: Testing Functions
---

## Learning Objectives

- You can use `assert` to check a function call against an expected result.
- You can choose normal, boundary, empty, and otherwise revealing test cases.
- You can interpret a failing assertion as evidence that an expectation was not met.
- You can explain why calculation functions are easier to test than whole interactive programs.
- You can use tests while refactoring to check that behavior has stayed the same.

You have already tested programs by checking boundaries, empty sequences, no-match cases, and other revealing inputs. Functions make this habit easier to automate.

## A Test Compares Actual and Expected Behavior

Run this example:

```python runnable id=part-3-7-testing-functions-example-1
def double(number):
    return number * 2

assert double(5) == 10
print("The check passed.")
```

`assert` records an expectation directly. Read it as:

> I expect `double(5)` to equal `10`.

If the expression after `assert` is true, Python continues silently and the example reaches its `print` call.

If it is false, Python raises an `AssertionError`.

Change the expected `10` to `11` and run the example again. The assertion fails because the function returns `10`.

When a program is run normally, a failed assertion stops it at that statement, so statements later in the program are not run.

A passing `assert` produces no output; the example's success message comes from `print`.

## Build a Revealing Test Set

This test is useful:

```python
assert double(5) == 10
```

but it only checks one input.

A more informative set might be:

```python
assert double(5) == 10
assert double(0) == 0
assert double(-3) == -6
```

These cover:

- an ordinary positive value;
- zero;
- a negative value.

The categories depend on the function. Ask:

> **Which inputs are most likely to reveal that my implementation does not match the intended behavior?**

You can group related assertions in an ordinary function. For the `double` function from the start of the chapter, place this after its definition:

```python
def check_double():
    assert double(8) == 16

check_double()
```

Defining `check_double` does not run its assertion. Calling it runs the check. Add more assertions to the function to check more inputs; they run in order until one fails or all have passed.

Write a few checks of your own, then trace what happens when an assertion fails:

Write assertions for a calculation, then trace what Python does when assertions pass and fail.

:::exercise c7de8a34-6351-4dd5-bee6-3afb88b44a82

:::exercise 7012827e-ca6e-4d8c-9653-292d120db632

:::exercise 0b0ad9b9-01c3-4f61-adb0-38c9368c2e09

## Boundary Cases from Part 1

Consider:

```python
def ticket_price(age):
    if age < 7:
        return 0
    elif age < 18:
        return 8
    else:
        return 12
```

A weak test set might be:

```python
assert ticket_price(5) == 0
assert ticket_price(12) == 8
assert ticket_price(30) == 12
```

Those tests cover each branch, but not the exact boundaries:

```python
assert ticket_price(6) == 0
assert ticket_price(7) == 8
assert ticket_price(17) == 8
assert ticket_price(18) == 12
```

These assertions record and rerun checks at the points where the result changes.

## Testing Functions That Process Lists

Consider:

```python
def count_positive(values):
    count = 0

    for value in values:
        if value > 0:
            count = count + 1

    return count
```

A useful test set could include:

```python
assert count_positive([4, -2, 7]) == 2
assert count_positive([1]) == 1
assert count_positive([-4, -2]) == 0
assert count_positive([]) == 0
assert count_positive([0, 1, 0]) == 1
```

These cases ask:

- Does ordinary mixed input work?
- Does a single item work?
- What happens when there are no matches?
- What happens when the list itself is empty?
- Is zero correctly excluded by `> 0`?

They turn familiar edge-case reasoning into executable checks.

## Testing a Function That Mutates a List

Some functions return a new result. Others deliberately change a mutable value that the caller supplied. In that case, test the changed value:

```python
def replace_negative_values_with_zero(values):
    for index in range(len(values)):
        if values[index] < 0:
            values[index] = 0

temperatures = [4, -2, 7, -1]
replace_negative_values_with_zero(temperatures)
assert temperatures == [4, 0, 7, 0]
```

The assertion checks `temperatures` after the call because the function's stated responsibility is mutation, not returning a list.

An empty list is useful here too:

```python
temperatures = []
replace_negative_values_with_zero(temperatures)
assert temperatures == []
```

Test the intended interface: inspect a returned result or, when mutation is intended, the changed object.

## Tests Should Match the Intended Behavior

Suppose you write:

```python
def is_long_session(minutes):
    return minutes > 30
```

Then you write:

```python
assert is_long_session(30) == False
```

The test passes.

But what if the actual requirement was:

> A session of **at least 30 minutes** is long.

Now both the implementation and the test are wrong in the same way.

> **A test only checks the expectation you wrote down. It does not decide whether that expectation was the right one.**

As in the first exercise, group related assertions in a check function and call it after the definitions.

Investigate a small function whose supplied test passes. Choose more tests from its required behavior, then repair the implementation:

:::exercise 21aa840b-2775-4971-977b-5af81480300f

## Why Functions Are Easier to Test Than Whole Interactive Scripts

Repeatedly testing interactive `read_sessions` requires typing values, stopping the loop, and inspecting output.

Compare that with an assertion for `count_positive` from earlier in this chapter:

```python
assert count_positive([4, -2, 7]) == 2
```

The input and expectation are visible together and can be rerun after every change.

- functions that perform calculations from parameters are straightforward to call from tests;
- functions whose main purpose is keyboard input or printing usually require more elaborate testing techniques.

For now, focus automated tests on the calculation logic.

Also run the complete program through representative interactions. Helper tests do not check whether input, calculations, and output are connected correctly.

## Testing Before and After Refactoring

When refactoring, use the same inputs before and after the change. For example, run the festival dashboard with an empty line, one count, and a mixture of busy and quiet periods, and keep the output for comparison.

After extracting a calculation, also test it directly, as you did with `count_positive` earlier in this chapter. Once those checks pass, run the complete program again to check that it uses the result correctly.

Passing the same cases provides evidence that the refactoring preserved behavior, though it is not proof. If you introduced a parameter, test more than the value the original script used.

Choose tests that expose boundary, search, empty-input, and refactoring mistakes:

Select tests that challenge the requirements and reveal changes introduced during refactoring.

:::exercise dd83d776-6731-4b23-8ef5-4694f8f3349f

:::exercise b45cb13c-ad2f-4cb4-bf06-9a2cf8f41533

:::exercise 0e3f77f5-5145-4785-8a59-f89a2efc0536

:::exercise deca2a64-385a-4a09-a8ab-9d382a3efceb

**Tests Are Not User-Input Validation**

The assertions in this chapter are checks that a programmer runs while developing a program. They do not replace `if` conditions or the input-validation techniques in the next chapter.

For example, `assert ticket_price(7) == 8` checks the implementation. It does not prevent a user from entering text when the program expects an age.

## Check Your Understanding

1. What happens when the expression in an `assert` statement is false?
2. Why are boundary values often useful test inputs?
3. Why can one ordinary example fail to reveal an early-return bug in a loop?
4. Why are calculation functions usually easier to test than functions that call `input(...)`?
5. Why can a program and its tests both agree with each other and still violate the actual requirement?

[Validation and Errors](#/part-3/8-validation-and-errors) next applies function design to safe interactive input. [Specifications, Verification, and AI](#/part-3/9-specifications-verification-and-ai) then returns to the relationship between implementations, tests, and requirements.
