---
id: part-2/4-lists-remembering-several-values
part: 2
order: 4
title: "Lists: Remembering Several Values"
---

## Learning Objectives

- You can create a list and access its items by index.
- You can use `len(...)` and `in` with lists.
- You can change an existing list item and append new items.
- You can use a direct `for` loop to process the values in a list.
- You understand an important difference between strings and lists: lists can be changed in place.

A string gives you a sequence of characters, but programs need many other kinds of collections. A course may have several scores. A weather program may have several temperatures. A reading log may contain several book titles.

Python **lists** let you store several values in one collection.

## Creating a List

A list is written using square brackets:

```python
scores = [12, 8, 15, 10]
```

The list contains four integer values.

Lists can also contain strings:

```python
languages = ["Python", "JavaScript", "Rust"]
```

An empty list contains no items:

```python
values = []
```

As with strings, the items in a list have positions.

## Indexing Lists

Indexing works just as it did for strings:

```python
scores = [12, 8, 15, 10]

print(scores[0])
print(scores[2])
```

The output is:

```text
12
15
```

The first index is `0`, and `len(...)` gives the number of items:

```python
print(len(scores))
```

prints `4`.

The last non-negative index is therefore `3`.

Negative indexes work as well:

```python
print(scores[-1])
```

prints the final value, `10`.

The next starter reads four city names into variables. Put those values into a list using square brackets. Print the complete list, then read its first and last items and find its length. Adding items to an existing list is introduced later in this chapter.

:::exercise fadc5e6a-ce91-4a0c-83e1-b5de8d8012ce

## Membership Works with Lists Too

The `in` operator tests whether a list contains a particular value:

```python
countries = ["Finland", "Norway", "Estonia"]

print("Norway" in countries)
print("Sweden" in countries)
```

The output is:

```text
True
False
```

Notice what is being compared. With a list of countries, Python looks for a complete list item. The expression `"Finland" in countries` asks whether one of the items equals `"Finland"`. A fragment such as `"land"` is not itself a list item, even though those letters occur inside `"Finland"`.

Decide what list membership compares.

:::exercise b3655937-e2d2-4bd1-97d5-c41eed03f523

:::exercise 6631fcb9-75f1-488e-9d71-d1bba6256ba5

:::exercise d50e4dd5-896c-4601-bb22-a4b6447f0180

## Lists Can Change

Here is an important difference from strings. You can replace an item in a list:

```python runnable id=part-2-4-lists-remembering-several-values-example-1
scores = [12, 8, 15]
scores[1] = 10

print(scores)
```

The output is:

```text
[12, 10, 15]
```

The list itself has changed.

Trying the corresponding operation with a string does not work:

```python
word = "cat"
word[0] = "b"
```

Python reports an error. Strings are **immutable**: their characters cannot be replaced in place. Lists are **mutable**: their items can be changed.

You do not need a detailed theory of mutability yet. For this part, remember the practical distinction:

> You can read items from both strings and lists, but you can replace items in a list.

:::exercise 547acb85-cb34-4c85-8c08-5301a89a0cc1

## Adding Items with `.append(...)`

Lists can also grow:

```python
books = []

books.append("Frankenstein")
books.append("The Odyssey")

print(books)
```

The output is:

```text
['Frankenstein', 'The Odyssey']
```

When Python displays a complete list, it uses square brackets around the list, commas between its items, and quote marks around items that are strings. Python may display single quotes even if you used double quotes when creating the strings. These quote marks show where each string item begins and ends; they are not part of the book titles themselves.

For example, printing one item displays only the text stored in that string:

```python
print(books[0])
```

The output is:

```text
Frankenstein
```

`.append(...)` changes the existing list by adding one item at the end.

Write:

```python
books.append("Frankenstein")
```

Do **not** write:

```python
books = books.append("Frankenstein")
```

The purpose of `.append(...)` here is to modify `books`, not to produce a new updated list that you assign back.

:::exercise 569b0b97-1aba-40e9-a12d-e8ade4a5a948

## `for` Works with Lists

You already know how `for` works. Lists simply provide another kind of sequence:

```python
scores = [12, 8, 15, 10]

for score in scores:
    print(score)
```

Compare the two loops:

```python
for character in word:
    print(character)
```

```python
for score in scores:
    print(score)
```

Whether the sequence contains characters, scores, or city names, each iteration gives the loop variable the next item and runs the body.

:::exercise eec3ff39-e03a-41ff-9dc3-899b63b030c8

## Explain Changes in Execution Order

Trace the program below on paper. Before each statement, predict which part of the list or program state will change. Notice that appending creates a new position, while assignment replaces the value at an existing position. The loop then visits the changed list.

```python runnable id=part-2-4-lists-remembering-several-values-trace-1
values = [3, 5]
values.append(7)
values[0] = 4

for value in values:
    print(value)
```

Following the statements in execution order produces:

```text
4
5
7
```

## Strings and Lists

At this point, the similarities and differences are useful to collect in one place:

| Operation or property | String | List |
| --- | --- | --- |
| ordered sequence | yes | yes |
| indexing | yes | yes |
| `len(...)` | yes | yes |
| membership with `in` | yes | yes |
| direct `for` loop | yes | yes |
| item can be replaced | no | yes |
| can grow with `.append(...)` | no | yes |

You will build on this comparison throughout the course. Later, other kinds of collections will have their own strengths and limitations.

## Empty Lists

An empty list behaves naturally with a `for` loop:

```python
values = []

for value in values:
    print(value)

print("Finished")
```

The loop body runs zero times.

This is often useful: an algorithm can process a list whether it has zero, one, or many items. However, operations such as `values[0]` still require at least one item. Pay attention to that distinction in the next chapter.

Check which sequence operations strings and lists share and where they differ.

:::exercise 92a0878a-40c8-4a87-af77-a4977296a806

:::exercise 76355296-dfb8-4df9-b5dc-349c3d659271

:::exercise 9769580d-5642-40cd-8b48-e0f0b44e45ae

:::exercise e7fcfb9f-4058-47b2-aba5-a3bcd4cfef6d

## Check Your Understanding

1. How are list indexes similar to string indexes?
2. What does `.append(...)` change?
3. What is the practical difference between a mutable list and an immutable string?
4. In `for score in scores:`, what value does `score` receive on each iteration?
5. When Python displays a list of strings, are the quote marks part of the stored text?
