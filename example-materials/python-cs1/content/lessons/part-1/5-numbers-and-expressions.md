---
id: part-1/5-numbers-and-expressions
part: 1
order: 5
title: Numbers and Expressions
---

## Learning Objectives

- You can use integers and floating-point numbers in calculations.
- You can write arithmetic expressions using `+`, `-`, `*`, `/`, `//`, and `%` where appropriate.
- You can translate a small word problem into variables and expressions.
- You understand enough operator precedence to read common expressions and know when to use parentheses for clarity.
- You can use intermediate variables to make calculations easier to read and explain.

Programs often need to do more than store values. They calculate with them. This chapter introduces the arithmetic tools you need for small programs and, more importantly, the habit of translating a real situation into clear expressions.

## Calculating with Integers and Floats

The previous chapter distinguished `int` and `float` values. This chapter focuses on what you can calculate with them. Recall that:

- `int` for whole numbers;
- `float` for floating-point numbers.

Examples:

```python
students = 28
temperature = 21.5
```

Basic arithmetic works much as you would expect:

```python
print(10 + 3)
print(10 - 3)
print(10 * 3)
print(10 / 3)
```

The `/` operator performs division and produces a float:

```python
print(10 / 2)
```

prints `5.0`.

You can try out the examples in the editor below. Type them in, run them, and check that the output is what you expect.

```python runnable id=part-1-5-numbers-and-expressions-example-1
print(10 + 3)
print(10 - 3)
print(10 * 3)
print(10 / 3)
```

## Other Useful Arithmetic Operators

Python has several additional numeric operators.

### Floor Division

The `//` operator performs **floor division**: it divides and rounds the quotient down.

```python
print(17 // 5)
```

This gives `3`: the quotient `3.4` is rounded down to `3`.

### Remainder

`%` gives the remainder after division:

```python
print(17 % 5)
```

This gives `2`.

Together, these are useful for converting a number of minutes into hours and leftover minutes:

```python
minutes = 95
hours = minutes // 60
remaining_minutes = minutes % 60

print(f"{hours} h {remaining_minutes} min")
```

The output is:

```text
1 h 35 min
```

:::exercise d8674a87-3525-49b6-a6a6-6e205ee1e50f

## From Input to Calculation

Remember that `input(...)` returns text. A calculation therefore usually starts with conversion:

```python
minutes = int(input("Minutes: "))
hours = minutes / 60
print(hours)
```

:::exercise 98906656-32a2-46ad-af2c-d1cf284d7790

## Operator Precedence

Consider:

```python
result = 2 + 3 * 4
```

Python performs multiplication before addition, so the result is `14`, not `20`.

Parentheses can change the grouping:

```python
result = (2 + 3) * 4
```

Now the result is `20`.

You do not need to memorize a huge precedence table. For the expressions in this course, the following is usually enough:

1. parentheses first;
2. multiplication, division, floor division, and remainder;
3. addition and subtraction.

When an expression is even slightly difficult to read, use parentheses or intermediate variables. Code is read far more often than it is typed.

## Translating a Word Problem into Code

Suppose the task is:

> A cinema ticket costs 12 euros. Ask how many tickets the user wants and calculate the total price.

A useful approach is to identify the quantities:

- ticket price;
- number of tickets;
- total price.

Then turn them into variables:

```python
ticket_price = 12
ticket_count = int(input("How many tickets? "))
total_price = ticket_price * ticket_count
print(f"Total: {total_price} euros")
```

The program is simple because the representation is simple. The variable names line up with the quantities in the problem description.

## Intermediate Variables Are Often Better

It is possible to write many calculations in one line. For instance, the above program could be written as:

```python
print(f"Total: {12 * int(input('How many tickets? '))} euros")
```

This works, but it is harder to inspect and explain. Extra variables are not waste. They name the pieces of the reasoning and make it easier to read, trace, and explain. Prefer the following more explicit version over one-liners:

```python
ticket_price = 12
ticket_count = int(input("How many tickets? "))
total_price = ticket_price * ticket_count
print(f"Total: {total_price} euros")
```

Identify what a dense expression computes. Consider which intermediate names would make it easier to read.

:::exercise 4f57f074-6cfe-46f8-b77a-27d449b8527f

## Formatting Numeric Output

Sometimes a calculation produces more decimal places than you want to show.

```python
hours = 95 / 60
print(hours)
```

The exact output may contain many digits. In an f-string, you can request a fixed number of decimal places:

```python
print(f"{hours:.1f} hours")
```

This displays one digit after the decimal point.

```text
1.6 hours
```

Formatting changes how the number is shown. It does not change the stored value in `hours`.

:::exercise c614d7ea-b627-4758-b481-00d4366473d3

## Common Pitfalls

A few common problems:

- trying to add an integer to an unconverted input string;
- using integer conversion when the input may contain a decimal point;
- confusing `/` with `//`;
- writing a correct but unreadable expression with too many operations on one line;
- forgetting that units matter.

The last point is easy to underestimate. A value called `time` is less informative than `time_minutes` or `time_hours`. The variable name can carry the unit and prevent mistakes.

Apply the earlier input-conversion lesson to repair an arithmetic program.

:::exercise 9a2d50e6-5c33-4fe0-bbef-64b650d6e8ca

Use the following exercise to apply the chapter's arithmetic tools in one complete calculation.

:::exercise 17571978-8f7a-4cce-8650-212c92e085d1

## Check Your Understanding

1. What is the difference between `/` and `//`?
2. What does `%` calculate?
3. Why does `2 + 3 * 4` produce `14`?
4. Why can intermediate variables make a calculation easier to understand?
5. Why must numeric user input usually be converted before arithmetic?
6. What is the difference between changing a float's value and merely formatting it for display?
