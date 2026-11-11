---
id: part-1/2-programs-and-the-programming-workflow
part: 1
order: 2
title: Programs and the Programming Workflow
---

## Learning Objectives

- You can describe programming as giving precise instructions to a computer.
- You can break a small task into smaller steps before writing code.
- You can run a short Python program and distinguish source code, output, and error messages.
- You can use an edit-run-observe-revise cycle when developing a program.
- You understand why reading and explaining code are part of programming, not separate from it.

This chapter is about what programming is and how you will work throughout the course. You do not need to know Python yet. The important idea is that programming is a process of turning an intention into a sequence of precise instructions, then checking whether those instructions actually produce the behavior you wanted.

## Programming Is Precise Problem Solving

Programming is the activity of describing a process so precisely that a computer can carry it out.

A computer does not understand goals in the same way a person does. If you tell another person, "make me some tea," they fill in a great deal of missing information from experience. They know that water needs to be heated, that the mug should probably not be placed upside down, and that the kettle should eventually be switched off.

A Python program does not fill in those gaps. It follows the instructions that are actually present. Thus, programming requires precision. A program can be almost what you intended and still do the wrong thing.

> Generative AI does not remove this need for precision. An AI assistant may guess what you intended when your request is vague, but now the guesswork has simply moved somewhere else. If the guess is wrong, the generated program may still look polished and plausible.

A programmer therefore needs two related skills:

- describing the intended behavior clearly;
- checking that the resulting program really has that behavior.

You will practise both across the course.

## From Goals to Smaller Pieces

Consider another task:

> Ask the user how many minutes they studied and tell them how many hours that is.

The task can be broken down as follows:

1. Ask the user for the number of minutes.
2. Store the answer.
3. Turn the answer into a number.
4. Divide that number by 60.
5. Store or otherwise use the result.
6. Print the result for the user.

This is **problem decomposition**: breaking a larger task into smaller responsibilities.

The same habit works whether you write the code yourself or ask an AI assistant for help. "Build a study app" is vague. "Ask for a number of minutes, convert it to hours, and print the result" is much easier to reason about.

Later in the course, decomposition becomes more formal when you learn functions, modules, and classes. For now, it is simply a way of thinking before typing.

## From Thinking to Code

Those smaller steps are already close to a program. Programming is the work of turning them into instructions a computer can follow.

## Source Code, Output, and Program State

When you write Python, the text you write is called **source code**. Here is a complete Python program:

```python
print("Hello, Python!")
```

When Python runs this program, it produces output:

```text
Hello, Python!
```

The source code and the output are different things. The source code is the instruction. The output is one visible consequence of executing that instruction.

Soon, your programs will also have values stored in variables. Those values form part of the program's **state**: the information the program currently remembers while it is running. Much of debugging consists of comparing the state you *expected* with the state the program *actually* has.

Decide whether each item is Python source code or program output.

:::exercise 45696958-a59c-4479-8188-f7fb9ac70e67

:::exercise 00e59f79-6a30-44a5-b2ce-381432150163

## Running Python

In the course environment, you will have an editor where you can type Python and a way to run the program. Running the program means that Python reads the source code, executes the instructions, and produces output. You will see the output below the editor.

You can run the program by clicking the **Run** button. Try the following program:

```python runnable id=part-1-2-programs-and-the-programming-workflow-example-1
print("Hello!")
print("This is my first Python program.")
```

Compare the output with the source code and then change the second line to something of your own and run the program again.

For now, treat `print(...)` as the instruction that displays a line. The next chapter explains the text values passed to `print(...)` and how to construct your own output. Here the focus is the workflow around the program.

This cycle is the basic development workflow:

1. **Edit** the program.
2. **Run** the program.
3. **Observe** what happened.
4. **Revise** the program.

You will use this cycle constantly. Professional programming adds more tools around it, but the basic rhythm remains recognizable.

## Errors Are Information

Try running this program exactly as written:

```python runnable id=part-1-2-programs-and-the-programming-workflow-example-2
print("Hello, Python!"
```

Python cannot understand it because a closing parenthesis is missing. You should see a **syntax error**.

A syntax error means that the source code does not follow the grammar of Python. The program cannot start executing normally because Python cannot parse the instructions.

Fix the missing parenthesis and run the program again.

This is an important early habit: when Python reports an error, **read the message before changing random things**. The message provides information about what Python could not understand or what went wrong while the program was running.

You will encounter many errors in this course. Everyone who programs does.

**A Useful Attitude Toward Errors**

The goal is not to reach a point where you never make mistakes. The goal is to become better at locating and correcting them.

When something fails, try to identify one specific fact first: what line failed, what Python says about it, or what value was different from what you expected. Fixing one concrete problem is much easier than treating the whole program as "broken."

Read each error, make a focused correction, and run the program again.

:::exercise 7edbc312-2dd5-4f95-9b63-ee4158920d51

:::exercise 3724c9ed-ab2c-4ba8-b247-d67f27066fed

## Order Matters

Python normally executes top-level statements from top to bottom.

Compare:

```python runnable id=part-1-2-programs-and-the-programming-workflow-example-3
print("First")
print("Second")
```

with:

```python runnable id=part-1-2-programs-and-the-programming-workflow-example-4
print("Second")
print("First")
```

Both programs are valid. They do different things because the order of the instructions changed.

When you are confused by a program, returning to the question "what happens first, what happens next?" often helps.

## Reading Is Part of Programming

You will write and read code in this course.

Most programmers spend a large part of their working time reading existing code: their own code from last week, code written by teammates, library examples, documentation, code from the internet, and increasingly code suggested by AI assistants.

A useful question throughout the course is: **Can I explain what this program does without relying on the person or tool that wrote it?**

## Check Your Understanding

1. What is problem decomposition?
2. What is the difference between source code and program output?
3. What does a syntax error mean?
4. Why is the edit-run-observe-revise cycle useful?
5. Why is it important to read and explain code, not just write it?
