---
id: part-1/3-talking-with-a-program
part: 1
order: 3
title: Talking with a Program
---

## Learning Objectives

- You can display output using `print(...)`.
- You can read user input using `input(...)` and store the result.
- You understand a string as text represented as a value in Python.
- You can build readable output using f-strings.
- You can apply simple string operations such as `.strip()` and `.lower()` when appropriate.

Programs become much more interesting when they can communicate with a user. In this chapter, you will write programs that show information, ask questions, remember the answers, and build new text from those answers.

## Printing Output

You used `print(...)` in the previous chapter while learning how to run and revise a program. Now the focus moves from the workflow to the values a program displays. The `print(...)` function displays a value as output.

```python
print("Hello!")
```

You can call `print` several times:

```python
print("Welcome to the course.")
print("We are writing Python now.")
```

Each call produces a line of output.

You can also print an empty line:

```python
print("Before")
print()
print("After")
```

This is useful when you want output to be easier to read.

:::exercise 55da8386-276f-429b-a161-4b77422a198a

## Strings Hold Text

Text values in Python are called **strings**. A string is written between quotation marks:

```python
"hello"
"Ada Lovelace"
"42"
""
```

The last example is an empty string: text containing zero characters.

The value `"42"` is also a string. It contains digit characters, but it is still text. Later, you will see why the distinction between the string `"42"` and the number `42` matters.

Both single and double quotation marks can be used:

```python
'hello'
"hello"
```

In this course, double quotation marks are used most often for consistency.

**Strings Now and Later**

Strings are important enough that you will return to them several times during the course. In this part, the goal is deliberately small: strings are text values that your program can receive, store, compare, clean up, and print.

You do **not** need to know yet how to access individual characters, take slices of text, loop through a string, or explain why strings cannot be changed in place.

Decide whether each Python value is a string.

:::exercise 63242cbc-73a9-41c9-b74e-5d3a0b85e28b

:::exercise a8f68299-e25e-4e51-b541-6374a4f40291

:::exercise 411eab88-fad8-49d5-9f60-32b082ccdade

:::exercise 83daca35-b05f-4867-9daa-119ff29fd2ef

## Asking for Input

The `input(...)` function shows a prompt and waits for the user to type something.

```python runnable id=part-1-3-talking-with-a-program-example-1
input("What is your name? ")
```

In this workshop app, type `Ada` in the input box before pressing **Run**. Python reads that line when it reaches `input(...)`. Nothing is stored yet, so the program cannot use the answer later. For programs with several inputs, enter each answer on its own line before running.

> Your answers remain in the input box. The output area shows what the program prints, including any prompts passed to `input(...)`. Reading an answer does not automatically print it. If the program needs more lines than you provided, add them to the input box and run again.

Usually, you want to remember the answer. A **variable** is a name that lets the program refer to a value later. Read the following as "store the result of `input(...)` in a variable named `name`":

```python
name = input("What is your name? ")
```

Now the program can use `name` later:

```python runnable id=part-1-3-talking-with-a-program-example-2
name = input("What is your name? ")
print(name)
```

In an interactive terminal, entering `Ada` would normally produce this transcript:

```text
What is your name? Ada
Ada
```

The first line of that terminal transcript contains the prompt followed by the typed answer. The second line is output from `print(name)`. In this app, input and output are separate: with `Ada` in the input box, the output area shows `What is your name? Ada` on one line, because the prompt has no newline and only `print(name)` prints the name.

The variable is what lets information move from one line of the program to another.

This is enough about variables for the interactive programs in this chapter. [Values, Variables, and Types](#/part-1/4-values-variables-and-types?anchor=assignment-changes-state) examines assignment, reassignment, and program state more carefully.

Ask for a value, store it, and use it in output.

:::exercise 04de5bac-f771-4b81-a629-d0df39ac3fee

:::exercise fef85ec1-39d9-42b4-a401-11fc449913ac

## Building Text with f-strings

A common task is combining fixed text with a variable value. Python's **f-strings** make this straightforward.

```python
name = "Ada"
print(f"Hello, {name}!")
```

The `f` before the opening quotation mark tells Python that expressions inside `{...}` should be evaluated and inserted into the string.

If `name` contains `Ada`, the output is:

```text
Hello, Ada!
```

The same works directly with user input:

```python runnable id=part-1-3-talking-with-a-program-example-3
name = input("What is your name? ")
print(f"Nice to meet you, {name}.")
```

You will use f-strings throughout the course. They are usually the clearest way to construct messages containing values.

:::exercise 8fbef474-c95b-4464-9cab-3218f6c531b5

## A Few Useful String Operations

Strings have operations associated with them. These are called **methods**. You do not need to understand methods formally yet; that arrives much later when you learn about objects. For now, you only need a few methods that make user input easier to work with.

### Removing Extra Whitespace

Users sometimes type spaces before or after an answer. The method `.strip()` removes whitespace from both ends:

```python
name = input("Name: ").strip()
```

If the user types spaces around `Ada`, the stored value becomes simply `Ada`.

### Changing Letter Case

The method `.lower()` produces a lowercase version of a string:

```python
answer = input("Continue? ").strip().lower()
```

If the user types `YES`, the value after `.lower()` is `yes`.

These operations will become useful when you compare user input in the decisions chapter.

**Objects Hiding in Plain Sight**

Strings are actually **objects** in Python. An object is a value that has operations associated with it. The operations are called **methods**.

For now, it is enough to read `name.strip()` as "produce a cleaned-up version of the string stored in `name`" and `answer.lower()` as "produce a lowercase version of the string stored in `answer`."

:::exercise bda014e6-e688-483f-81d5-e48349137c16

## A Complete Interactive Program

Here is a small program using everything from the chapter:

```python runnable id=part-1-3-talking-with-a-program-example-4
print("=== Tiny Profile ===")
print()

name = input("Name: ").strip()
city = input("City: ").strip()
food = input("Favorite food: ").strip()

print()
print(f"Hello, {name}!")
print(f"You are from {city} and your favorite food is {food}.")
```

Before running it, work through the program from top to bottom with these imaginary inputs:

```text
Ada
London
tea
```

Ask yourself:

- What values are stored after the three `input` lines?
- What does the first final `print` produce?
- What does the second final `print` produce?

Then run it and compare.

:::exercise 556a9ff6-5cb8-497f-94b6-46412d399144

## Common Pitfalls

A few mistakes are common at this stage:

- forgetting quotation marks around literal text;
- using a variable name before assigning it;
- misspelling a variable name in one place;
- forgetting the `f` before a string containing `{name}`;
- writing `{'name'}` instead of `{name}` inside an f-string: the quoted version inserts the literal text `name` rather than the value of the variable.

Compare:

```python
print("Hello, {name}")
```

with:

```python
print(f"Hello, {name}")
```

The first prints the braces and word `name` literally. The second inserts the variable's value.

:::exercise ddecd40b-29a2-46bf-9fea-230a275bedf4

## Check Your Understanding

1. What kind of value does `input(...)` return?
2. What does the `f` do in an f-string?
3. What is the purpose of `.strip()`?
4. Why might `.lower()` be useful before comparing user input?
5. What is the difference between a literal string such as `"name"` and a variable named `name`?
