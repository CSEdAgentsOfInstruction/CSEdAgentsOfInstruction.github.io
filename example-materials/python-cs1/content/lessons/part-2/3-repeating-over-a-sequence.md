---
id: part-2/3-repeating-over-a-sequence
part: 2
order: 3
title: Repeating over a Sequence
---

## Learning Objectives

- You can use a `for` loop and conditions to process characters in a string.
- You can build a count or a text result across loop iterations.
- You can use `range(...)` for a fixed number of repetitions or to visit string indexes.
- You can trace a loop one iteration at a time, following the loop variable and any remembered results.

The previous chapter ended by printing the characters at indexes `0`, `1`, `2`, and so on. That required a separate statement for every position. On a shorter word, an index would be out of range; on a longer word, the extra characters would not be printed.

The purpose was simple: do the same thing once for every character. Python has a direct way to express that idea.

## Your First `for` Loop

```python runnable id=part-2-3-repeating-over-a-sequence-example-1
word = "python"

for character in word:
    print(character)
```

The output is:

```text
p
y
t
h
o
n
```

Read the loop as:

> For each character in `word`, print that character.

The indented block is the **loop body**. Python runs it once for each item in the sequence.

The name `character` is the **loop variable**. On the first iteration it refers to `"p"`, on the second to `"y"`, and so on.

You choose the loop-variable name. This works too:

```python
for letter in word:
    print(letter)
```

`letter` communicates the purpose more clearly than a vague name such as `x`.

A loop runs once for every item. If the string is empty, it has no items, so the loop body runs zero times. A program that only prints inside such a loop prints nothing for an empty word.

Now write a loop that prints the characters of an entered word.

:::exercise e2ef5689-6c01-4fd0-b23c-25e0a99e57b4

## Trace One Iteration at a Time

Consider:

```python
word = "ivy"

for character in word:
    print(f"Character: {character}")
```

A trace can be written as:

| Iteration | `character` | Output |
| ---: | --- | --- |
| 1 | `"i"` | `Character: i` |
| 2 | `"v"` | `Character: v` |
| 3 | `"y"` | `Character: y` |

On each iteration, Python assigns the next character to `character` and runs the loop body. Trace those assignments in order, as you traced changing variable values in Part 1.

## Doing Something with Each Character

The body can contain any code appropriate for the current character:

```python
word = "hello"

for character in word:
    print(character.upper())
```

The output is:

```text
H
E
L
L
O
```

The loop does not change `word`. Each iteration takes one character, produces an uppercase version, and prints it.

## Conditions Inside Loops

Everything you learned about `if` statements still applies inside a loop.

```python
word = "banana"

for character in word:
    if character == "a":
        print("Found an a!")
```

The condition is checked once per iteration. The message is printed on the iterations where the current character equals `"a"`.

This is an important combination:

> A loop decides **when to repeat**. An `if` decides **what to do on a particular repetition**.

:::exercise f85d4c81-51e8-46ec-80ae-fde5d245da4d

## Remembering Across Iterations

Sometimes printing something on each iteration is not enough. You need the program to remember what has happened so far.

Suppose you want to count the letter `s`:

```python
word = "season"
s_count = 0

for character in word:
    if character == "s":
        s_count = s_count + 1

print(s_count)
```

The output is:

```text
2
```

The initialization `s_count = 0` runs **once, before** the loop. Putting it inside the loop would reset the count on every iteration. Initializing it before the loop also gives it a value when the word is empty and the loop body never runs.

Trace the important values:

| Character | Is it `s`? | `s_count` afterwards |
| --- | --- | ---: |
| `s` | yes | 1 |
| `e` | no | 1 |
| `a` | no | 1 |
| `s` | yes | 2 |
| `o` | no | 2 |
| `n` | no | 2 |

This pattern has three parts:

1. initialize a variable before the loop;
2. update it on relevant iterations;
3. use the final value after the loop.

You will reuse this pattern with lists later in the part.

**Repeating and Remembering**

The `for` loop performs the **repeating**. The variable `s_count` performs the **remembering**.

Many useful loop algorithms are combinations of those two ideas.

Trace, repair, and apply the counter pattern.

:::exercise 3d7dff78-639d-4f39-8797-a8e309b07c65

:::exercise 9a358f00-190c-4f88-aab5-737b4d4e752c

## Joining Strings with `+`

Before building a longer string in a loop, note that `+` has a useful meaning when both values are strings: it joins them together.

```python
first_part = "rain"
second_part = "bow"
word = first_part + second_part

print(word)
```

The output is:

```text
rainbow
```

Joining strings in this way is called **concatenation**. The operation does not add a space automatically. It simply places the second string immediately after the first one.

## Building a Result One Character at a Time

A variable can also remember text:

```python
word = "robot"
result = ""

for character in word:
    result = result + character.upper()

print(result)
```

The value of `result` develops like this:

```text
""
"R"
"RO"
"ROB"
"ROBO"
"ROBOT"
```

This is another example of state changing across iterations.

You do not need to use this technique for every text-processing task. Its value here is that it makes the changing state visible.

:::exercise 86b12438-af23-42f9-8a55-2ac5db14982f

## Remembered State and Empty Strings

You have already seen that a loop over an empty string runs zero times. This also means that any state initialized before the loop keeps its initial value:

```python
word = ""
result = "No characters"

for character in word:
    result = character

print(result)
```

The assignment inside the loop never runs, so the program prints:

```text
No characters
```

The same reasoning applies to a counter initialized to `0` or a result initialized to `""`: if there are no iterations, its value does not change. This observation becomes important with lists too. Always consider what a loop does when its sequence is empty.

Check what a counter contains after a loop over an empty string.

## Repeating a Fixed Number of Times

So far, each `for` loop has processed the items in an existing string. Sometimes you instead want to repeat an action a known number of times. The `range(...)` function provides the numbers a loop can use for this:

```python
for number in range(3):
    print(f"Repetition {number + 1}")
```

The output is:

```text
Repetition 1
Repetition 2
Repetition 3
```

`range(3)` provides the values `0`, `1`, and `2`. Its stopping value, `3`, is **not included**. The loop therefore runs three times. More generally, `range(n)` provides the values from `0` through `n - 1`, so its body runs `n` times when `n` is a non-negative integer.

Use a direct loop when you already have the values to process:

```python
for character in word:
    print(character)
```

Use `range(n)` when the main idea is to repeat an action `n` times:

```python
for number in range(5):
    print("Keep practising!")
```

In the second example, the loop variable is not needed in the body. It still receives the next number on every iteration.

Every statement in the loop body repeats. This includes reading input:

```python
for number in range(2):
    answer = input()
    print(f"You entered: {answer}")
```

This program reads and responds to two input lines because both statements are inside the loop. Moving `input()` before the loop would read only once, while moving it after the loop would postpone the read until both iterations were finished.

The values from `range(5)` can do more than control five repetitions. They are `0`, `1`, `2`, `3`, and `4`, so `number + 1` can label output for people as messages 1 through 5. The next exercise uses both roles to build a tiny event announcer.

:::exercise 8e84578a-f8cb-473c-8bfd-a628db413ec3

## Using Range Values as Indexes

The numbers from `range(...)` can also serve as positions. Because `range(len(word))` provides the values from `0` through `len(word) - 1`, it provides every valid non-negative index of the string:

```python
word = "code"

for index in range(len(word)):
    print(f"{index}: {word[index]}")
```

The output is:

```text
0: c
1: o
2: d
3: e
```

Direct iteration is clearer when a program needs only each character. Using indexes is useful when the position itself matters or when the program calculates which position to inspect.

## Check Your Understanding

1. What value does the loop variable have during one iteration of a `for` loop?
2. Why is a counter usually initialized before the loop rather than inside it?
3. How many times does a `for` loop over an empty string execute its body?
4. Which values does `range(4)` provide, and why does a loop over it run four times?
5. When would you choose `for item in sequence` instead of `for number in range(n)`?
6. Why does `range(len(word))` provide valid non-negative indexes for `word`?
