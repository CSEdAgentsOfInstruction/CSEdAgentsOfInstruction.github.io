---
id: part-1/4-values-variables-and-types
part: 1
order: 4
title: Values, Variables, and Types
---

## Learning Objectives

- You understand a variable as a name referring to a value in a running program.
- You can assign and reassign variables and trace how the program state changes.
- You can distinguish common Python value types: `str`, `int`, `float`, and `bool`.
- You can convert numeric input text to an `int` or `float` when a calculation needs a number.
- You can use `type(...)` as an investigative tool.
- You can choose variable names that communicate intent.

In the previous chapter, you used variable names to carry input from one line to another. This chapter builds on that first use: it examines how assignment changes program state and why Python distinguishes different kinds of values.

## Variables and Readable Names

Consider:

```python
name = "Ada"
age = 20
```

After these lines run, the program has two variables. `name` refers to the value `"Ada"`, and `age` refers to the value `20`.

A variable is useful because a program can refer to the value by name later:

```python
print(name)
print(age)
```

The variable name should usually say something about what the value means. Compare:

```python
x = 45
```

with:

```python
study_minutes = 45
```

Python does not care which name you choose. A human reader does.

Python variable names normally use lowercase words separated by underscores. Names can contain letters, digits, and underscores, but cannot begin with a digit. Names are case-sensitive, and reserved words used by Python itself cannot be used as names.

A useful name communicates the value's role. `study_minutes` says more than `x`. Readable names reduce the amount of information a reader has to keep in their head.

:::exercise 2f84aa1a-b05a-4cf4-a19e-a9e797fe59af

## Assignment Changes State

An assignment statement gives a variable a value:

```python
count = 3
```

You can assign the same variable again:

```python
count = 3
count = 4
```

After both lines run, `count` has the value `4`. The previous value is no longer the current value of that variable.

A slightly more interesting example is:

```python
count = 3
count = count + 1
```

Python evaluates the right-hand side first. At that moment, `count` is `3`, so `count + 1` becomes `4`. Then `4` is assigned back to `count`.

The line is not an equation in the mathematical sense. It is an instruction that changes program state. Following those changes line by line is called **tracing program state**. The example below demonstrates the process. Trace how the values change, then run it to check your prediction.

```python runnable id=part-1-4-values-variables-and-types-trace-1
a = 20
print(a)
a = a + 5
print(a)
b = a
print(b)
b = b + 10
print(b)
print(a)
```

Following the statements in execution order produces:

```text
20
25
25
35
25
```

## Values Have Types

Python distinguishes different kinds of values. Some common types are:

| Type | Meaning | Examples |
| --- | --- | --- |
| `str` | text | `"Ada"`, `"42"`, `""` |
| `int` | whole number | `42`, `0`, `-7` |
| `float` | floating-point number | `3.5`, `0.0`, `-1.25` |
| `bool` | truth value | `True`, `False` |

These types support different operations.

For example:

```python
print(10 + 5)
```

prints `15`, because both values are numbers.

But:

```python
print("10" + 5)
```

raises a `TypeError`, because Python does not automatically treat the text `"10"` as a number. The text must first be converted when numeric addition is intended.

The characters look similar. The values are not the same kind of thing.

## Investigating with `type(...)`

Python can tell you the type of a value:

```python
print(type("Ada"))
print(type(42))
print(type(3.5))
print(type(True))
```

The output resembles:

```text
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

You do not need to worry yet about why Python displays the word `class`. The useful part is `str`, `int`, `float`, or `bool`.

Compare how a text value and a numeric value are displayed.

:::exercise 3c8c9440-6f9b-4abd-b62f-d1245cbe778d

:::exercise 302307fd-e330-4edb-943f-b26497954dec

`type(...)` is especially useful while investigating unfamiliar behavior.

For example:

```python
minutes = input("Minutes: ")
print(type(minutes))
```

Even if the user types `45`, the type is still `str`. `input(...)` returns text.

## Converting Between Types

Sometimes you need to convert a value from one type to another.

The most common conversions at this stage are:

```python
int("42")
float("3.5")
str(42)
```

This allows a program to turn numeric input text into actual numbers:

```python
age_text = input("Age: ")
age = int(age_text)
print(age + 1)
```

A shorter version combines the input and conversion:

```python runnable id=part-1-4-values-variables-and-types-example-1
age = int(input("Age: "))
print(age + 1)
```

Both are valid. The two-line version can be easier to debug because it keeps the raw text and converted number separate. The one-line version is more compact.

## Conversion Can Fail

What happens here if the user types `hello`?

```python
age = int(input("Age: "))
```

Python cannot convert the text `"hello"` into an integer. It raises a `ValueError`.

For now, this is acceptable. In Part 3, you will learn systematic input validation and exception handling. In this part, the instructions for exercises that expect a number can assume that the user enters a sensible numeric value.

Still, it is useful to know what the error means. The program did not fail because `int` is unreliable. It failed because the provided value did not satisfy the conversion's requirements.

> Unless an exercise specifically asks you to handle invalid input, you may assume users type values in the requested form during Parts 1 and 2.

:::exercise 89cf2f12-8148-49e3-a7fd-032a22240ff1

You have now seen `bool` alongside the other basic value types, but you do not need to operate on boolean values yet. [Numbers and Expressions](#/part-1/5-numbers-and-expressions) develops arithmetic with `int` and `float`; [Making Decisions](#/part-1/6-making-decisions) introduces comparisons, shows how they produce boolean values, and uses those values to make decisions.

## Check Your Understanding

1. What does assignment do?
2. Why is `count = count + 1` valid Python even though it is not a mathematical equation?
3. What type does `input(...)` return?
4. What is the difference between `"42"` and `42`?
5. What does `int(...)` do?
6. What are the two possible boolean values?
7. What makes a variable name useful to a human reader?
