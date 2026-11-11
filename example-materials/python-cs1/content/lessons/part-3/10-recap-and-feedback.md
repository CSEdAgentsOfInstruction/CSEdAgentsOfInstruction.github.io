---
id: part-3/10-recap-and-feedback
part: 3
order: 10
title: Recap
---

In this part, you learned to give pieces of behavior names, pass information into functions, return results, reason about local state, validate user input, and test calculation logic independently from the rest of a program.

The central design questions are now:

> What is this function responsible for?
> What information does it need?
> What should it return or change?
> How can I check that behavior?

A larger function can use the result of a smaller function.
## Putting the Ideas Together: Reading Tracker

The final programming exercise combines the ideas from this part in a small reading tracker. Read its handout for the function contracts, accepted input, and required output.

The program separates its work into three layers:

```text
read_sessions()
       v sessions
calculation functions
       v returned results
print_summary(...)
```

`main()` connects these steps. The input function asks for session lengths and handles invalid input. The calculation functions receive the collected list, return their results, and leave the list unchanged. The presentation function displays the summary. You can test the calculations separately by calling them with lists you choose.

## Suggested Workflow

Build and check one layer at a time:

1. Read every function contract and identify its parameters, return value or output, empty case, and allowed effects.
2. Implement the calculation functions first. Test ordinary, boundary, one-item, and empty cases, and check that the input list remains unchanged.
3. Implement and check the presentation function using known result values.
4. Implement the input function. Keep sentinel recognition, integer conversion, and positive-number validation as separate decisions, and test recovery from several invalid attempts.
5. Connect the functions in `main()` only after the individual responsibilities work.
6. Run complete examples, including stopping immediately and entering invalid input before valid input.

This order makes a failure easier to locate: first establish that each part satisfies its contract, and only then test the connections among the parts.

:::exercise c0640e66-3abc-44a8-8d12-8f9d78f49f55

## Explain the Design

When the program works, step back from its individual lines and explain why its responsibilities are separated. Connect specific input, calculation, testing, and empty-case decisions to the program's behavior.

## Check Your Understanding

1. What is the difference between a parameter and an argument?
2. What is the difference between printing a result and returning it?
3. Why can mutating a list object through a parameter be visible to the caller, while assigning another integer to a parameter changes only the function's local name?
4. What does an `assert` statement check?
5. Why should tests be based on intended behavior rather than copied from the implementation?

## Looking Ahead

Lists let you store several values, and functions let you organize the behavior that processes them. But a list such as:

```python
student = ["Ada", 42, "Computer Science"]
```

still relies on remembering what each position means.

In Part 4, you will focus on **organizing data**. Dictionaries and other structured representations will let programs give names and relationships to the information they store.
