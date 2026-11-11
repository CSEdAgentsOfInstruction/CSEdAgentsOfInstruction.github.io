---
id: part-1/6-making-decisions
part: 1
order: 6
title: Making Decisions
---

## Learning Objectives

- You can write comparison expressions that evaluate to `True` or `False`.
- You can write `if`, `if/else`, and `if/elif/else` statements.
- You can predict which branch runs for a given input and explain why.
- You can pay deliberate attention to boundary values and branch order.
- You can combine simple boolean expressions using `and`, `or`, and `not` when one decision depends on more than one condition.

Until now, the programs in this part have mostly followed one straight path. They ask questions, perform calculations, and print results. Real programs often need to behave differently in different situations.

A ticket may cost less for a child. A study session may be classified as short or long. A login message may depend on whether the user entered the expected code.

To make those choices, a program needs expressions that answer yes-or-no questions and a way to use those answers to decide what happens next.

## Comparisons Produce Boolean Values

Python has comparison operators for values:

| Operator | Meaning |
| --- | --- |
| `==` | equal to |
| `!=` | not equal to |
| `<` | less than |
| `<=` | less than or equal to |
| `>` | greater than |
| `>=` | greater than or equal to |

Examples:

```python
print(5 > 3)
print(5 == 3)
print(5 != 3)
```

The output is:

```text
True
False
True
```

The result of a comparison is a boolean value.

Decide whether each comparison produces `True` or `False`.

:::exercise 13bc3c96-e898-4a7b-b9cd-2899c0439e6a

:::exercise 301ed5ba-6806-49e3-a662-09f59a059319

:::exercise de5f1b27-289f-49fb-a318-65fb5023fafb

:::exercise c1061c87-03eb-461e-a6f5-4e497af12041

:::exercise 95f1bed4-492b-4c3d-9461-e55c477995b5

:::exercise 758d9a97-72e7-4bea-b679-4d4aa4055b9b

## `=` and `==` Are Different

One of the most common beginner mistakes is confusing assignment with equality comparison.

```python
score = 10
```

assigns the value `10` to `score`.

```python
score == 10
```

asks whether the current value of `score` equals `10` and produces `True` or `False`.

Read them differently:

- `=` means **store this value under this name**;
- `==` means **are these two values equal?**

Decide whether each line changes program state or asks a boolean question.

:::exercise 9e622b03-34a8-4604-8951-a1b493a8df22

:::exercise 65fc3c5d-d415-44ac-b539-97fac9ec02d7

:::exercise 7356a7ac-9030-4e40-b376-0ca997b206f8

:::exercise a7c3c694-f9ca-4041-9686-546f825a908b

## Comparing Strings

Strings can be compared for equality too:

```python
answer = "yes"
print(answer == "yes")
```

This is case-sensitive:

```python
print("YES" == "yes")
```

is `False`.

This is why normalizing user input is often useful:

```python
answer = input("Continue? ").strip().lower()
print(answer == "yes")
```

Now inputs such as `YES`, ` yes `, and `Yes` all become `yes` before comparison.

## The Basic `if`

A boolean expression becomes especially useful when it controls whether some code runs.

An `if` statement runs a block of code only when its condition is true.

```python
minutes = 75

if minutes >= 60:
    print("That was at least an hour.")

print("Session recorded.")
```

The indented line belongs to the `if`. The final line does not.

If `minutes` is `75`, both messages are printed. If `minutes` is `30`, the first message is skipped and `Session recorded.` is still printed.

Two syntax details matter:

- the `if` line ends with a colon (`:`);
- the body is indented, normally by four spaces.

You can read the statement almost like ordinary language:

> If `minutes >= 60` is true, print the message.

:::exercise becf1d5c-58ea-4681-81a4-7e9c29bb0b54

## `else` for the Alternative

Often there are two mutually exclusive cases:

```python
age = int(input("Age: "))

if age >= 18:
    print("Adult ticket")
else:
    print("Youth ticket")
```

Exactly one branch runs.

The `else` does not need its own condition. It means "if the previous condition was false."

:::exercise 45f21fde-69d6-47e0-969b-c4769fbcc7ce

## `elif` for Several Cases

When there are more than two categories, use `elif`:

```python
minutes = int(input("Minutes: "))

if minutes < 20:
    print("Short session.")
elif minutes <= 60:
    print("Solid session.")
else:
    print("Long session.")
```

Python checks the conditions from top to bottom. As soon as one condition is true, that branch runs and the rest are skipped.

If `minutes` is `45`:

1. `45 < 20` is false;
2. `45 <= 60` is true;
3. the second branch runs;
4. the `else` is skipped.

:::exercise 6f718274-e5ff-4323-a43e-84520c5eaf0d

## Branch Order Matters

Consider this code:

```python
age = 12

if age < 18:
    print("Minor")
elif age < 13:
    print("Child")
```

The second branch can never run. Anyone younger than 13 is already younger than 18, so the first condition catches them first.

A better order is:

```python
if age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
else:
    print("Adult")
```

When conditions overlap, the order determines which one wins.

:::exercise c2b1f1d0-dcc4-4e3e-aacd-df37e03079f4

## Boundaries Need Deliberate Attention

Suppose a discount applies to customers aged **65 or older**.

The correct comparison is:

```python
age >= 65
```

not:

```python
age > 65
```

The second version wrongly excludes people who are exactly 65.

Boundary values are the values directly at the edge of a rule. They deserve special tests because a single character can change the behavior:

```text
<   versus   <=
>   versus   >=
```

When you write a classification, ask:

- What happens one step below the boundary?
- What happens exactly at the boundary?
- What happens one step above it?

This is the beginning of a testing habit you will develop more systematically in later parts.

Predict the category at each boundary, then adjust the upper boundary.

:::exercise a0176a21-37c4-42a2-a23f-9acb082063ac

## Independent `if` Statements Are Different

These two programs do not mean the same thing.

Program A:

```python
if score >= 70:
    print("Passed")

if score >= 90:
    print("Excellent")
```

Program B:

```python
if score >= 90:
    print("Excellent")
elif score >= 70:
    print("Passed")
```

If `score` is `95`, Program A prints **both** messages. Program B prints only `Excellent`.

Use separate `if` statements when several independent facts may all be true. Use an `if/elif/else` chain when you want to select one category from several alternatives.

Choose a decision structure based on whether several outcomes may occur together.

:::exercise 52098685-96dc-4fbb-9b38-718168852124

:::exercise be733765-827c-4c5d-a2b6-a801c697a088

:::exercise 63d5967a-30d1-42be-bb04-08d45bb8b786

## Combining Conditions

Sometimes one decision depends on more than one yes-or-no question. Boolean expressions can be combined for those situations.

### `and`

`and` is true only when both sides are true:

```python
age = 20
has_ticket = True

if age >= 18 and has_ticket:
    print("You may enter.")
```

The message is printed only if the person is old enough **and** has a ticket.

### `or`

`or` is true when at least one side is true:

```python
is_student = True
is_senior = False

if is_student or is_senior:
    print("Discount available.")
```

### `not`

`not` reverses a boolean value:

```python
is_closed = False

if not is_closed:
    print("The service is open.")
```

You do not need complicated boolean expressions in Part 1. In fact, complicated expressions are often easier to understand when they are split into named pieces:

```python
old_enough = age >= 18
has_permission = answer == "yes"
allowed = old_enough and has_permission

if allowed:
    print("Allowed")
```

Named conditions are often easier to trace and explain.

:::exercise f79ba895-be1c-4499-9532-72be05bb38d3

## A Complete Decision Program

Here is a small program that combines input, conversion, arithmetic, string normalization, and conditions:

```python
name = input("Name: ").strip()
minutes = int(input("Study minutes today: "))
energy = input("Energy level (low/okay/high): ").strip().lower()

hours = minutes / 60

print()
print(f"{name}, you studied for {hours:.1f} hours.")

if minutes < 20:
    print("A short session still counts.")
elif minutes <= 90:
    print("That is a solid block of work.")
else:
    print("That was a long session. Remember to take breaks.")

if energy == "low":
    print("Consider choosing a lighter next task.")
elif energy == "high":
    print("You may have energy for another focused task.")
```

Notice that the duration classification and the energy message use **separate** decision structures. They describe different aspects of the session, and both may produce output.

:::exercise 6fcd1df0-9b9e-4fe9-9ea9-d61fb867d913

## Common Pitfalls

- Writing `=` instead of `==` in a comparison.
- Forgetting the colon at the end of `if`, `elif`, or `else`.
- Using inconsistent indentation.
- Putting a broad condition before a narrower one in an `elif` chain.
- Forgetting to normalize text before comparing when case and whitespace should not matter.
- Choosing `<` when the requirement really says "less than or equal to," or vice versa.
- Assuming that if a program works on one test value, all boundary values must also be correct.
- Combining so many conditions in one expression that the rule becomes hard to explain.

Each starter program contains one small issue related to the common pitfalls in this chapter. Read the intended behavior, identify the issue, and make the smallest repair that gives the correct behavior.

:::exercise b437acf7-d0c5-4043-932f-7681428f7315

:::exercise d8813772-625d-4a95-8f65-11968c1a8661

:::exercise ed2d0d92-2e10-4833-986c-bec3d296af43

:::exercise 4d1a2d73-044f-48d7-8f8a-0dd605605843

:::exercise 490939e4-eb80-43dd-bf91-a2cbdfdb66d4

## Check Your Understanding

1. What type of value does a comparison produce?
2. What is the difference between `=` and `==`?
3. What determines whether the body of an `if` statement runs?
4. In an `if/elif/else` chain, how many branches can run?
5. Why does branch order matter?
6. Why should exact boundary values be tested deliberately?
7. What is the difference between two separate `if` statements and an `if` followed by `elif`?
8. When might one decision need `and` or `or`?
