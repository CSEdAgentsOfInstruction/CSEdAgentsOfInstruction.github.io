---
id: part-3/2-defining-and-calling-functions
part: 3
order: 2
title: Defining and Calling Functions
---

## Learning Objectives

- You can define a function using `def` and call it.
- You can trace a program, distinguishing a function definition from the execution of its body.
- You can place function definitions and the main program in a clear order.
- You can identify repeated code or a distinct task that could be given a function name.

You have called functions since your first Python program:

```python
print("Hello")
length = len("hello")
```

A **function call** asks Python to run behavior that has been defined somewhere. Until now, almost all of those definitions came from Python itself.

You can define your own functions too.

## Your First Function

```python runnable id=part-3-2-defining-and-calling-functions-example-1
def greet():
    print("Hello!")
    print("Welcome to the program.")

greet()
```

The output is:

```text
Hello!
Welcome to the program.
```

The definition begins with `def`:

```python
def greet():
```

The colon starts an indented block, just as it does with `if`, `for`, and `while`. The indented lines form the **function body**.

The function body does not run merely because Python reads the definition. It runs when the function is **called**:

```python
greet()
```

Read that line as:

> Run the function named `greet`.

The parentheses are part of the call. They will become more important in the next chapter, when functions begin receiving information.

## Defining Is Not Calling

Before running this program, predict whether `inside greet` appears before or after `after definition`:

```python runnable id=part-3-2-defining-and-calling-functions-example-2
print("before definition")

def greet():
    print("inside greet")

print("after definition")
greet()
print("after call")
```

The output is:

```text
before definition
after definition
inside greet
after call
```

When Python reaches:

```python
def greet():
```

it creates the function definition and continues past the body. The body is saved for later. Only the call `greet()` makes Python enter the function and execute its lines.

A useful trace is:

1. print `before definition`;
2. define `greet`;
3. print `after definition`;
4. call `greet`;
5. execute the body and print `inside greet`;
6. return to the line after the call;
7. print `after call`.

Function definitions often appear near the top of a program, but their bodies run only when called.

Now define and call one small function yourself:

:::exercise 86726e7b-152c-420c-a037-126659d5b573

## Calling a Function More Than Once

Once behavior has a name, it can be reused:

```python
def print_separator():
    print("--------------------")

print("First section")
print_separator()
print("Second section")
print_separator()
print("Third section")
```

The two calls execute the same body at different points in the program.

This is one reason functions help with duplicated code. If the separator later changes, there is one definition to edit instead of several copied lines.

But avoiding duplication is not the only reason to use a function. A function name can also make the structure of a program easier to see.

Compare:

```python
print("--------------------")
print("SUMMARY")
print("--------------------")
```

with:

```python
print_separator()
print("SUMMARY")
print_separator()
```

The second version tells a reader what the repeated lines are _for_.

Use repeated calls to keep one visual detail in one place:

:::exercise a04d56ee-1180-4e3c-aaa6-e32f0eb995a8

## Functions as Named Pieces of Work

The measurement program in the [overview](#/part-3/1-overview) had four jobs: read input, select usable values, calculate a summary, and present the result. A function can give one of these jobs a name.

For example, a program that collects values and displays the usable ones might later look like this:

```python
values = read_values()
usable = select_usable(values)
print(usable)
```

This is a **design sketch**, not a complete runnable program: `read_values` and `select_usable` have not been defined here. The next chapter explains how functions return values. For now, notice that the names let you follow the program's tasks without reading all the code for each one.

**A Function Should Have a Reason to Exist**

Do not create a function merely because a block contains several lines.

A useful function usually represents a meaningful piece of work: calculate a total, classify a value, read one item, format one part of a report, or display one kind of message.

## A Definition Must Run Before Its Function Is Called

When Python executes a call, the function name must already refer to a function. At the top level of a program, this normally means Python must execute the function's `def` statement before it reaches the call.

This does not work:

```python
greet()

def greet():
    print("Hello")
```

When the first line runs, Python does not yet know what `greet` refers to.

A common structure is therefore:

```python
def greet():
    print("Hello")

def print_separator():
    print("----------")

print_separator()
greet()
print_separator()
```

Function definitions appear first. The main program comes afterwards. This is a useful program structure, not a rule that every function body must appear earlier than every call written anywhere in the file. What matters is whether the definition has executed by the time Python executes the call.

## Common Mistakes

### Forgetting the parentheses when calling

This:

```python
greet
```

does not run the body. `greet` refers to the function itself. `greet()` calls it.

### Forgetting the colon

```python
def greet()
    print("Hello")
```

is invalid syntax. The definition line ends in a colon.

### Incorrect indentation

```python
def greet():
print("Hello")
```

The body must be indented.

### Defining but never calling

This program produces no output:

```python
def greet():
    print("Hello")
```

The function exists, but nothing asks it to run.

Repair each of these mistakes in a complete program:

Each small starter has a different problem in its function definition or use. Make the smallest repair that produces the requested display.

:::exercise 98aada39-7cfd-483b-8271-94a9f938e444

:::exercise 5ae8f985-128c-4205-89f6-c7f2f757b1d6

:::exercise 0c367bd1-22fc-4668-9792-960185d1de7f

## Check Your Understanding

1. What is the difference between defining a function and calling it?
2. How do the colon and indentation identify a function's body?
3. Where does execution continue after a function call finishes?
4. What must have happened before Python can call a function by its name?
5. When would it be useful to give a piece of work its own function name?
