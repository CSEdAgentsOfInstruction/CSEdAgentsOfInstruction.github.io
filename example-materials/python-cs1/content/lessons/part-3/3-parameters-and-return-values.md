---
id: part-3/3-parameters-and-return-values
part: 3
order: 3
title: Parameters and Return Values
---

## Learning Objectives

- You can distinguish a parameter from an argument.
- You can define functions with one or more parameters.
- You can return a value and use it in another expression.
- You can distinguish printed output from returned values, including `None` when a function finishes without an explicit `return`.

The functions in the previous chapter always performed exactly the same work. Parameters let different calls supply different information, and return values let a function hand information back to its caller.

## Parameters and Arguments

Consider:

```python runnable id=part-3-3-parameters-and-return-values-example-1
def greet(name):
    print(f"Hello, {name}!")

greet("Ada")
greet("Grace")
```

In the definition:

```python
def greet(name):
```

`name` is a **parameter**. It is a name used inside the function.

In the call:

```python
greet("Ada")
```

`"Ada"` is an **argument**. It is the value supplied by this call.

When Python calls a function, it evaluates each argument and gives the resulting value a local parameter name.

For the first call above, local `name` refers to the string `"Ada"`. For the second call, that call's local `name` refers to `"Grace"`.

## Each Call Has Its Own Local Names

In this version of `greet`, the function also gives its message a name. Trace the two calls, writing down the local names and their values. Each call has its own **frame**, which groups the names belonging to that call.

```python runnable id=part-3-3-parameters-and-return-values-trace-1
def greet(name):
    message = f"Hello, {name}!"
    print(message)

greet("Ada")
greet("Bob")
```

Following the statements in execution order produces:

```text
Hello, Ada!
Hello, Bob!
```

The first call has `name` referring to `"Ada"` and `message` referring to `"Hello, Ada!"`. When that call finishes, its frame closes. The second call starts with its own `name` and creates its own `message` for `"Bob"`.

The local names from the first call are not reused by the second call.

## More Than One Parameter

A function can receive several pieces of information:

```python
def print_session(subject, minutes):
    print(f"{subject}: {minutes} minutes")

print_session("Programming", 45)
```

This call uses **positional arguments**. Each argument is matched with a parameter by position:

```text
subject -> "Programming"
minutes -> 45
```

Python matches arguments to parameters by position, even when their intended meanings do not match:

```python
print_session(45, "Programming")
```

Both arguments can still be bound to the two parameter names, although the displayed message no longer makes sense.

## Returning Information

Printing is useful when a function's job is to communicate with the user. Many functions instead need to produce a value for other code to use. Use `return` for that:

```python runnable id=part-3-3-parameters-and-return-values-example-2
def double(number):
    result = number * 2
    return result

answer = double(6)
print(answer)
```

Trace the same program. Notice when `answer` gets its value and when output appears.

```python runnable id=part-3-3-parameters-and-return-values-trace-2
def double(number):
    result = number * 2
    return result

answer = double(6)
print(answer)
```

Following the statements in execution order produces:

```text
12
```

The call `double(6)` evaluates to the returned value `12`. It can therefore appear anywhere that value could appear:

```python
print(double(6) + 1)
print(double(double(3)))
```

The first line prints `13`. In the second line, the inner call returns `6`, which becomes the argument of the outer call. The outer call returns `12`.

## Printing and Returning Are Different Jobs

Compare:

```python
def print_double(number):
    print(number * 2)

def double(number):
    return number * 2
```

`print_double(5)` displays `10`. By contrast:

```python
result = double(5)
```

does not display the calculation. It hands `10` back to the caller and stores it in `result`.

> **Printing displays information. Returning supplies a value to the caller.**

A calculation function is usually more flexible when it returns its result. The caller can then print it, store it, compare it, or use it in another calculation.

## A Function Without an Explicit `return` Returns `None`

Run this example:

```python runnable id=part-3-3-parameters-and-return-values-example-3
def print_double(number):
    print(number * 2)

result = print_double(7)
print(f"Stored value: {result}")
```

Trace the same program. Compare what is printed with the value assigned to `result`.

```python runnable id=part-3-3-parameters-and-return-values-trace-3
def print_double(number):
    print(number * 2)

result = print_double(7)
print(f"Stored value: {result}")
```

Following the statements in execution order produces:

```text
14
Stored value: None
```

Every function call evaluates to a value. If execution reaches the end of a function without an explicit `return`, Python returns the special value `None` implicitly.

Here the function displayed `14`, but the call returned `None` rather than a calculated number. `None` is a real Python value commonly used to represent the absence of another useful result. Writing `return None` explicitly produces the same returned value.

The next exercises ask you to write only a function definition. While working, add temporary calls below the definition and run the program to check different arguments. For a calculation function, put the call inside `print(...)` to see its returned value. Remove the temporary calls before pressing **Check**; the tests make their own calls.

Write a function that uses its parameter in a printed message:

:::exercise be1450bc-1fbe-4b27-a94c-77800469655b

Then write a function that calculates and returns a result from two arguments:

:::exercise 8b520b5d-9ce3-4bcf-9f2d-bf5287e35386

## `return` Ends the Current Call

When Python executes `return`, the current function call ends immediately:

```python
def describe_temperature(temperature):
    if temperature < 0:
        return "freezing"

    if temperature < 15:
        return "cold"

    return "mild or warm"
```

With `-5`, the first `return` ends the call. The later conditions are not evaluated. [Building Functions with Lists](#/part-3/5-building-functions-with-lists?anchor=a-return-ends-the-current-call) applies this rule carefully inside loops.

## Check Your Understanding

1. How does a parameter differ from an argument?
2. How are positional arguments matched to parameters?
3. How can the caller use a function's returned value?
4. What value does a call produce if the function prints a message but has no explicit `return`?
5. What happens to the rest of a function's body when a `return` statement runs?
