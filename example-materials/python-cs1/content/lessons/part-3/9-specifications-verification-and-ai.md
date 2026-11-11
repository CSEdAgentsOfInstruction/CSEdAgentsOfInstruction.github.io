---
id: part-3/9-specifications-verification-and-ai
part: 3
order: 9
title: Specifications, Verification, and AI
---

## Learning Objectives

- You can describe a function in terms of its purpose, parameters, return value, effects, and important edge cases.
- You can write tests from a specification rather than from an implementation.
- You can use tests and code reading to check whether an implementation, including AI-generated code, satisfies the requested behavior.
- You can explain why making requirements precise is part of programming.

[Testing Functions](#/part-3/7-testing-functions) introduced executable tests, and [Validation and Errors](#/part-3/8-validation-and-errors) separated a testable rule from interactive user-input handling. Both depend on deciding what a test should expect.

Before writing a function, you can describe what it accepts, returns, prints, or changes. This description of what the function **should** do is a **specification**.

## Implementation and Requirement Are Different Things

Consider:

```python
def summarize_sessions(sessions):
    return len(sessions)
```

The code is valid and readable, but the name does not tell us enough to decide whether it is correct.

If the requirement is to return the number of sessions, this implementation fits. If the requirement is to return the total time spent reading, it does not: for `[10, 20]`, the function returns `2` instead of `30`.

Correctness depends on whether the implementation matches the intended behavior.

## A Small Function Specification

A useful specification can answer questions such as:

- What is the function called, and what is its purpose?
- What parameters does it receive, and which values are accepted?
- What does it return, and which rules determine that result?
- Does it print anything or change a supplied list?
- What should happen in important empty, boundary, or invalid cases?

For example:

> **Function:** `count_long_sessions(sessions, minimum_minutes)`  
> **Parameters:** `sessions` is a list of nonnegative integer session lengths in minutes; `minimum_minutes` is a nonnegative integer and the smallest length counted as long.  
> **Returns:** the number of values in `sessions` that are greater than or equal to `minimum_minutes`.  
> **Empty list:** returns `0`.  
> **Does not:** print or change `sessions`.

## Derive Tests from the Specification

The specification already suggests useful tests:

```python
sessions = [10, 30, 45]

assert count_long_sessions(sessions, 30) == 2
assert sessions == [10, 30, 45]
assert count_long_sessions([30], 30) == 1
assert count_long_sessions([29], 30) == 0
assert count_long_sessions([], 30) == 0
assert count_long_sessions([35, 45], 40) == 1
assert count_long_sessions([0, 5, 0], 0) == 3
```

Choose the expected results from the specification before implementing or inspecting the function. Otherwise, a test may repeat a mistake in the implementation. For example, the `[30]` case above expects `1` because a session exactly at the minimum qualifies.

Derive expected results and revealing tests from written function specifications.

:::exercise e6b282a5-d1c1-406e-8cab-9e46bd4fd343

:::exercise 52848eff-903b-4bde-95e7-f3f931a91e44

## A Specification Can Live Next to the Function

With the expected results written down, we can implement the session count and record its contract in the function itself.

A string used as the first statement inside a function is called its **docstring**. Triple quotation marks (`"""`) let the string span several lines. A docstring documents the function; unlike a `#` comment, Python keeps it as part of the function's documentation:

```python
def count_long_sessions(sessions, minimum_minutes):
    """Return the number of sessions at least minimum_minutes long.

    An empty sessions list returns 0. The function does not modify sessions.
    """

    count = 0

    for minutes in sessions:
        if minutes >= minimum_minutes:
            count = count + 1

    return count
```

Place the earlier assertions below this definition and run the program to check it.

A short docstring records the contract rather than narrating each implementation step. Avoid:

```python
"""Set count to zero, loop through sessions, add one when..."""
```

The docstring in the function above instead states the returned result, the empty case, and the promise not to change the supplied list.

## Edge Cases Are Design Decisions

For `longest_session([20, 45, 30])`, a natural result is `45`. An empty list has no longest item, so the specification must decide what `longest_session([])` means. It could:

- require a nonempty list, with callers ensuring that this precondition holds;
- return `None` to mean that no longest session exists;
- return a deliberately chosen domain value, such as `0` when every valid session length is positive.

For example, a reading tracker that accepts only positive session lengths can use `0` to mean that no session was recorded. That meaning belongs in the contract; an accumulator's initial value alone does not decide the empty-case behavior.

## AI Makes Vague Requirements More Visible

Suppose you ask an AI system:

> Write a function that finds long study sessions.

Does "find" mean return the sessions or count them? What counts as long? An AI may fill those gaps with plausible choices and produce valid code for the wrong problem.

Use the `count_long_sessions` specification from earlier in this chapter in the request. It supplies those decisions, together with the accepted inputs, empty-case result, and allowed effects. The same contract gives you a way to check the proposed code.

## Verify Generated Code Against the Rule

Imagine an AI returns:

```python
def count_long_sessions(sessions, minimum_minutes):
    count = 0

    for minutes in sessions:
        if minutes >= minimum_minutes:
            count = count + minutes

    return count
```

The variable is called `count`, but the loop adds each qualifying session's length. The specification asks how many sessions qualify, not how many minutes they contain.

This test exposes the mismatch:

```python
assert count_long_sessions([30, 45], 30) == 2
```

The implementation returns `75`. Comparing that result with the specification shows why the accumulator should increase by one for each qualifying session.

Use each specification to decide what evidence would reveal a mistake in the following implementations:

Compare each implementation with its written contract instead of judging by appearance alone.

:::exercise c93b3501-afa5-4c63-b229-ed0ba414d9a2

:::exercise 458fd1bc-6975-47d8-8b0c-75a860a35f17

:::exercise 15db9d24-cd4a-4595-9ab3-e3ed57962d33

## A Practical Workflow

Use this sequence when implementing a small function yourself or with AI assistance:

1. **Specify.** Write what the function accepts, returns, prints or changes, and does on important cases.
2. **Choose tests.** Turn the specification into representative examples and boundaries.
3. **Implement.** Write the code yourself or use an AI assistant.
4. **Run the tests.** Find cases where actual and expected behavior differ.
5. **Read and revise.** Explain why the code produces the expected results, and fix any mismatch. If the original requirement was unclear, clarify it and update the tests too.

Tests make selected requirements executable; the specification tells the tests what to expect.

**Check the Requirements Yourself**

Code, tests, and a specification proposed by the same AI can share one mistaken assumption. You remain responsible for deciding the required behavior and verifying the implementation against it.

Apply that workflow in a larger programming task:

:::exercise 50ba6bd1-b2c0-49cd-adaf-4705e943f58c

## Check Your Understanding

1. Why can valid-looking Python code still be incorrect?
2. What should a specification say about output and mutable arguments in addition to parameters and a return value?
3. Why is it useful to write tests from the specification before inspecting an implementation?
4. What is the purpose of a docstring in the examples above?
5. What test would distinguish counting qualifying sessions from adding their lengths?
