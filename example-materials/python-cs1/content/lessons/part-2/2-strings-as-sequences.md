---
id: part-2/2-strings-as-sequences
part: 2
order: 2
title: Strings Are Sequences
---

## Learning Objectives

- You understand that a string is an ordered sequence of characters.
- You can use an index to access an individual character.
- You can use `len(...)` to find the length of a string.
- You can use `in` to test whether a string contains a character or another piece of text.
- You can reason about valid and invalid string indexes.

In Part 1, you used strings as complete text values:

```python
name = "Ada"
message = "Welcome to the course"
```

That view is still useful. A string is one value. But a string also has an internal structure: it contains characters in a particular order.

```text
python
```

contains six characters:

```text
p  y  t  h  o  n
```

Because those characters have an order, Python can refer to their positions.

## Positions Start at Zero

Python numbers sequence positions starting from zero. These positions are called **indexes**.

For the string `"python"`:

| **Index**     | `0` | `1` | `2` | `3` | `4` | `5` |
| ---           | --- | --- | --- | --- | --- | --- |
| **Character** | `p` | `y` | `t` | `h` | `o` | `n` |

You access a character by writing the index in square brackets:

```python
word = "python"

print(word[0])
print(word[3])
```

The output is:

```text
p
h
```

The first character has index `0`, not index `1`. This convention appears throughout Python and many other programming languages.

## The Length of a String

The `len(...)` function tells you how many characters a string contains:

```python
word = "python"
print(len(word))
```

The output is:

```text
6
```

There is an important relationship between the length and the indexes:

> If a string has length `6`, its non-negative indexes are `0` through `5`.

The final valid non-negative index is therefore one less than the length.

```python
word = "python"
last_index = len(word) - 1
print(word[last_index])
```

This prints:

```text
n
```

Trying to access a position outside the string causes an error:

```python
word = "python"
print(word[6])
```

Python raises an `IndexError` because there is no character at index `6`.

**Length and Last Index**

For a non-empty sequence:

- the number of items is `len(sequence)`;
- the first index is `0`;
- the last non-negative index is `len(sequence) - 1`.

The difference between a count and an index is an important source of boundary mistakes. When a loop later works with positions, keep this relationship in mind.

An empty string has length `0` and contains no characters, so it has no valid indexes.

Connect a string's length with its valid index range.

:::exercise 4259f1b2-6536-4be8-b002-38abbc73e213

:::exercise 6fc4da31-da75-40a3-a43a-e54574683eff

## Negative Indexes

Python also allows negative indexes. They count backwards from the end:

```python
word = "python"

print(word[-1])
print(word[-2])
```

The output is:

```text
n
o
```

`-1` means the last character, `-2` means the second-to-last character, and so on.

Negative indexes still have limits. For a non-empty string of length `n`, the valid negative indexes are `-n` through `-1`. Because `"python"` has length `6`, `-6` refers to its first character:

```python
word = "python"
print(word[-6])
```

This prints:

```text
p
```

An index that goes further back is invalid:

```python
print(word[-7])
```

Python raises an `IndexError` because the string has no character at that position. An empty string has no valid indexes, positive or negative.

Negative indexing is convenient, but it is not essential for most of the loops in this part. Use it when it makes the intention clearer.

Practise reading negative indexes in the next exercise. Work out what each program does before running it.

A launch console stores a signal as a string. Work out what each program does.

:::exercise f0a58c8c-ba6e-4b8b-831f-845247168eb9

## Membership with `in`

Sometimes you do not need to know *where* something occurs. You only need to know whether it is present.

The `in` operator answers this question:

```python
word = "programming"

print("a" in word)
print("z" in word)
```

The output is:

```text
True
False
```

The result is a boolean value, so it can be used in an `if` statement. For example, a program can act when a fixed piece of text is present:

```python
title = "Python programming"

if "Python" in title:
    print("This title mentions Python.")
```

Membership can also test for a longer piece of text:

```python
print("gram" in "programming")
```

This produces `True`.

String membership is case-sensitive. For example, `"e" in "EAGLE"` is `False` because lowercase `"e"` and uppercase `"E"` are different characters. When letter case should not matter, normalize the text first using the string methods from Part 1:

```python
word = input().strip().lower()

if "e" in word:
    print("The word contains e.")
```

The call to `.lower()` produces the lowercase string that the membership test actually checks. Calling the method without using its result would leave `word` unchanged.

:::exercise 6adfc743-a5ca-42d5-8b49-bdcb6b13e941

## One Character Is Still a String

Consider:

```python
word = "fox"
letter = word[0]
```

The value of `letter` is `"f"`. Python does not have a separate basic character type here: a valid single index into a string gives you another string exactly one character long.

This means familiar string methods still work:

```python
letter = "f"
print(letter.upper())
```

The `.upper()` method produces an uppercase version of a string, so the output is:

```text
F
```

Like `.lower()` from Part 1, `.upper()` produces a new string. It does not change the original string in place.

Check the type of an indexed character and predict the result of a string method. Then write a small program that finds the first character, last character, and length of an entered word.

Connect indexing with the string values and methods you already know.

:::exercise 69620b8b-bb94-4bda-8d8b-11600d5de7d0

:::exercise 9e39e8ac-a171-44f8-8638-35302a7b6084

## Indexing Is Useful, but Repetition Is Better for Every Character

Suppose you want to print every character in `"python"`. You could write:

```python
word = "python"

print(word[0])
print(word[1])
print(word[2])
print(word[3])
print(word[4])
print(word[5])
```

These statements print every character only when the string has exactly six characters. A shorter string raises an `IndexError`; a longer string leaves the remaining characters unprinted.

A better question is:

> Can Python repeat the same operation once for every character, no matter how long the string is?

That is the topic of the next chapter.

## Check Your Understanding

1. What is the first index in a Python string?
2. If a string has length `8`, what is its last non-negative index?
3. If a string has length `8`, what range of negative indexes is valid? What happens if you use `-9`?
4. What type of value does the expression `"a" in word` produce?
