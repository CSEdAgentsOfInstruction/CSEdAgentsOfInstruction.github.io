---
id: part-3/4-names-objects-and-mutable-lists
part: 3
order: 4
title: Names, Objects, and Mutable Lists
---

## Learning Objectives

- You can explain how a function call gives its arguments local parameter names.
- You can distinguish reassigning a name from modifying a mutable object.
- You can predict changes made through a list parameter or an alias.
- You can write functions that change a supplied list or return a separate result, according to their purpose.

The previous chapter used parameters with numbers and strings. A function can also receive a list. To understand when a call changes that list, we need to look more closely at how names refer to values.

## Variables Are Names for Objects

In Part 1, a variable gave a value a name. We can describe that relationship more precisely:

> **A variable is a name bound to an object.**

An **object** is a Python value. Integers, strings, booleans, and lists are all objects. Numbers, strings, and booleans are **immutable**: they cannot be changed in place. Lists are **mutable**: their contents can change.

Assignment makes a name refer to an object:

```python
score = 10
```

This can be pictured as:

```text
score --> 10
```

Assignment and function calls do not automatically duplicate the object.

## Local Names and Scope

Run this as a separate program:

```python
def double(number):
    result = number * 2
    return result

answer = double(5)
print(answer)
print(result)
```

Inside the function, `number` and `result` are local names. The call returns `10`, which the main program stores as `answer`. The first `print` displays `10`, so the returned value is available to the caller.

The next statement, `print(result)`, stops the program with a **`NameError`**. Python reports this error when it cannot find a name used by the program. Here, `result` is available inside `double`, but the main program has no name `result`.

The part of a program where a name can be used is its **scope**. For now, the most important distinction is:

- names created inside a function are normally available only in that function's body;
- names created in the main program are outside that local scope.

Parameters are local names too. Each call has its own local names, even when several calls use the same function definition.

## The Same Spelling Can Be Used in Different Scopes

```python
message = "outside"

def show_message():
    message = "inside"
    print(message)

show_message()
print(message)
```

This prints:

```text
inside
outside
```

The two names are spelled alike but belong to different scopes. Assigning the local `message` does not reassign the outside `message`.

## Prefer Visible Inputs

A function can read a name from outside when it has no local name with the same spelling:

```python
tax_rate = 0.24

def tax(amount):
    return amount * tax_rate
```

This works, but it gives `tax` a dependency that is not visible in its parameters. A clearer small calculation function is often:

```python
def tax(amount, tax_rate):
    return amount * tax_rate
```

This is a rule of thumb rather than an absolute prohibition: prefer passing required information as a parameter when doing so makes the function's inputs clearer.

## Reassigning a Parameter

When a function is called, the argument expression is evaluated and the parameter becomes a local name for that object:

```python runnable id=part-3-4-names-objects-and-mutable-lists-example-1
def increase(number):
    number = number + 1

score = 10
increase(score)
print(score)
```

At the beginning of the call, the names can be pictured as:

```text
score  --> 10
number --> 10
```

The integer object `10` is immutable: it cannot be changed in place. The expression `number + 1` produces the integer `11`, and assignment rebinds only local `number`:

```text
score  --> 10
number --> 11
```

This does not assign to the caller's name `score`. The same reassignment rule applies to every parameter, including list parameters.

Trace what happens to names inside and outside a function during a call:

Trace names that belong to individual function calls and names that belong to the main program.

:::exercise 5fe88bcf-9fb3-4a15-9ad4-5538d8cc38cb

## Lists as Function Arguments

Lists can be supplied as arguments just like numbers and strings:

```python
def total_values(values):
    total = 0

    for value in values:
        total = total + value

    return total
```

`total_values([5, 8, 2])` returns `15`. The accumulator and loop are familiar from Part 2; only the function boundary is new.

A list is mutable, so a function can also modify the list object supplied by its caller:

```python runnable id=part-3-4-names-objects-and-mutable-lists-example-2
def add_score(scores, score):
    scores.append(score)

results = [10, 12]
add_score(results, 15)
print(results)
```

Trace the call. The caller's `results` and local `scores` refer to one list. `append` changes that list while both names keep referring to it.

```python runnable id=part-3-4-names-objects-and-mutable-lists-trace-1
def add_score(scores, score):
    scores.append(score)

results = [10, 12]
add_score(results, 15)
print(results)
```

Following the statements in execution order produces:

```text
[10, 12, 15]
```

When the call finishes, its local frame closes. The caller observes the changed list through `results`.

## Rebinding Is Not Mutation

Compare the preceding example with:

```python runnable id=part-3-4-names-objects-and-mutable-lists-example-3
def replace_scores(scores):
    scores = [0, 0, 0]

results = [10, 12]
replace_scores(results)
print(results)
```

Watch the two names again. The assignment creates a separate list and makes only local `scores` refer to it. The caller's `results` stays bound to the original list.

```python runnable id=part-3-4-names-objects-and-mutable-lists-trace-2
def replace_scores(scores):
    scores = [0, 0, 0]

results = [10, 12]
replace_scores(results)
print(results)
```

Following the statements in execution order produces:

```text
[10, 12]
```

The program prints `[10, 12]`. Rebinding `scores` did not modify the original list or rebind `results`.

```python
scores.append(15)       # modifies the existing list
scores = [0, 0, 0]      # rebinds the local name
```

The rule did not change between the number and list examples:

- a parameter is a local name bound to the argument object;
- reassigning the parameter changes only that local binding;
- mutating a shared mutable object is visible through every name bound to it.

## Aliasing Outside Functions

This behavior is not specific to parameters:

```python
first = [1, 2]
second = first
second.append(3)

print(first)
print(second)
```

Both lines print `[1, 2, 3]`. Assignment did not create an independent list. It bound `second` to the same list as `first`.

More than one name for the same object is called **aliasing**. When aliases refer to a mutable list, a change made through one name is visible through the others.

## Mutation Should Be Deliberate

A function whose stated purpose is to change a supplied list may reasonably use indexed mutation:

```python
def increase_each(values):
    for index in range(len(values)):
        values[index] = values[index] + 1
```

Apply that pattern to a conditional cleanup:

:::exercise 9c52fac6-0c97-4ddf-a3dd-512166f73a8b

A calculation function should usually return its result without unexpectedly changing its input. The earlier `total_values` function does this: it reads the items and returns their total without changing the list.

Sometimes a caller needs an updated list while keeping the original values. The function can return a separate list instead of changing the supplied one. Building a result list uses the same loop and list operations as in Part 2.

Practise that choice by recording another sensor reading:

:::exercise ce8f0d37-f8bc-4879-bafc-f8554331e27f

Returning a list does not automatically copy it. In the exercise, the function must create a separate list because the caller needs both the original log and the extended log. The earlier cleanup exercise instead changes the existing list and returns `None`. Follow the function's stated purpose when deciding which behavior to use.

## Check Your Understanding

1. When a list is passed to a function, what do the caller's name and the parameter refer to?
2. Why can a caller use a returned value even though the function's local names are unavailable there?
3. How does assigning a new list to a parameter differ from changing an item in the supplied list?
4. What does it mean for two names to be aliases?
5. How would you decide whether a function should change its input list or return a separate list?
