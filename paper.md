
Table of contents
<!-- TOC -->
- [1. Abstract](#1-abstract)
- [2. Introduction](#2-introduction)
  - [2.1. Motivation](#21-motivation)
    - [2.1.1. My part in the job](#211-my-part-in-the-job)
  - [2.2. Game mechanics design](#22-game-mechanics-design)
  - [2.3. A short history of development](#23-a-short-history-of-development)
    - [2.3.1. Initial attempts](#231-initial-attempts)
    - [2.3.2. Corona & Lua: Stage 2](#232-corona--lua-stage-2)
    - [2.3.3. C# rework](#233-c-rework)
    - [2.3.4. Unity and Godot](#234-unity-and-godot)
    - [Code generation](#code-generation)
      - [Reasons for code generation](#reasons-for-code-generation)
      - [Tools in short](#tools-in-short)
    - [2.3.5. Example illustrating why if-statements do not cut it.](#235-example-illustrating-why-if-statements-do-not-cut-it)
- [3. References](#3-references)

<!-- /TOC -->

# 1. Abstract 

Together with my colleague, we have created a Roguelike game, **Hopper**, based on the mechanics of *Crypt of the Necrodancer*.
In the first section I explain why I initiated this project and what development path I took. The next few sections are more technical. There, I motivate and illustrate with concrete examples my design decisions of the system, explain how the game works internally. I present how I managed to escape boilerplate and code duplication via code generation with *Roslyn* and *T4*. Finally, I show how the same code generation tools can be used for integrating the project with the *Godot* game engine.

# 2. Introduction

## 2.1. Motivation

The game idea is highly inspired by the game **Crypt of the Necrodancer** (henceforth refered to as simply *Necrodancer*), which I adore.

The project has always been planned to be an open-source game based on the same mechanics.

I never plan this project to make profit. It is designed for personal sake as well as, perhaps, for the community that is going to hopefully pick it up eventually.

The **problems with Necrodancer** that made me want to make a similar game are the following:
1. Modding is virtually impossible. Here, mods can only change visuals. No new mechanics or new types of mobs can be added into the game.
2. There is no Android support. I initially really wanted to play this on mobile.
3. The code is not publicly available.

So, **my goals for the project** became:
1. Make a game with mechanics like in Necrodancer.
2. Design a well-scalable system with many features and a slick API, to make developing mods easy.
3. Keep the code open to the public with a permissive license and invite modders when the API is mature enough.
4. Make it run on Android.

**Along the way**:
1. Get experience in game development.
2. Get experience in the domain of maintenance of complex systems.
3. Get experience in working and communicating with the community, artists and other developers.
4. Add yet another project into the list of personal projects. 


### 2.1.1. My part in the job

Now, I'd say I'm a nerd, I'm not an artist or a designer. 

I like programming complex systems and tools, but I cannot really *design* games, nor do I want to do it.
So my goal with this project is to build up a base, the *Core* of the game, its base library, off of which others could sprout their ideas. 
With this project, I do not strive to make a *complete* game, nor do I want to work on the graphics (drawing the sprites, creating animations, lighting, UI, etc.).
I want to make it very clear that I'm here to make a base for that, an interface for creating these animations and interacting with the world and the characters, tools for creating new objects and enemies etc.

For demonstration purposes, a minimal version of the game will be created.


## 2.2. Game mechanics design

The game that I aimed to make borrows its base mechanics from **Crypt of the Necrodancer**.

Necrodancer is a *Dungeon Crawler*, *Roguelike*. 
You get to explore a randomly generated dungeon, fighting enemies and bosses along the way. 
It is turn-based, that is, both you and your enemies can do an action (move, attack, cast a magic spell, open a chest, etc.) only once each turn.

I like the concept of Roguelikes in general — the fact that you grow stronger whilst descending into the depths of the dungeon. I also do like playing other Roguelikes. To be noted **The Binding of Isaac**, **Into the Breach**, **The Darkest Dungeon**, **Slay the Spire** and **One Step From Eden** are the ones that I enjoyed most.

What makes Necrodancer really stand out is its clever twist on the mechanic, namely, you can only act to the beat of the music, which is why it is classified as a *Roguelike Rhythm* game. 

The fact that you have limited time to act really does differentiate it from other Roguelikes.
While technically being turn-based, it succeeds to be fast-paced, thanks to this mechanic.
While you have *some* time to consider your next action, you cannot carefully calculate everything, like you would in chess.

Also, it is important to see the consequences of your actions and plan ahead a few turns to be safe, but given the fact that the time you are given to think in between beats is so limited, reaction plays a big role too.
This game teaches you to be able to draw the line at some point and take a decent action, which is not going to necessarily be the best one overall.
This is in a way similar to timed chess, where your time is a resource you have to manage and the clock ticking might make you nervous.
The short spacing between beats likewise feels stressful at times, but it feels good to sometimes clutch out such intense moments, where you are able to ward off a horde of enemies e.g. with a well-casted magic spell or a deft weapon swing.


## 2.3. A short history of development

I started working on this project about 2 years ago. 
Over these 2 years, it has been scrapped and rewritten, completely or partially from scratch, about 5 times.

Now it is hard to know what to do at the start, I would even dare say impossible.
With complex systems and without completely defined requirements, you rarely get things right the first time.
Code gets rewritten, ideas become more clear in your mind, new areas and possibilities get explored and abandoned.
Writing a game is, likewise, not a linear path.

Even though I knew the general idea I wanted to pursue with this project, as well as I had the base mechanics figured out, I did not know how to structure it correctly, in terms of code and system design.
So, I had to try many different things to reach the more exciting stuff I have got today.

### 2.3.1. Initial attempts

Initially, I tried to code the game in *Corona* game engine, in *Lua* programming language.
It allows exporting on mobile and desktop.

However, my understanding of how such games actually work was quite poor at the time.

Designing and implementing a simple game is entirely different from what I was going for.
If you are designing a game that could have thousands of different effects, mechanics and creatures and possibly expanded by mods, you cannot account for every item with a bunch of if-statements, you actually need more involved abstract systems making use of *some* kind of polymorphism.
I did not realize this before this project, but quickly understood it after this initial attempt.[Dungeon-Hopper][1]
I will expand on this more in a separate chapter.

This initial attempt at coding the game made me understand that complex and scalable games are not a bunch of if statements.
They require creativity and competence.

The initial code was scrapped completely and rewritten in the second version, still on Corona.

### 2.3.2. Corona & Lua: Stage 2

Lua is a really simplistic language: there is no concept of types, modules or classes.
Dynamic method dispatch, however, can be simulated via metatables (prototypical inheritance).
There also are no arrays: both arrays and dictionaries are represented by the concept of tables.

The biggest problem with Lua is its lack of types and, consequently, its lack of static analysis.
One has to deal with simplest annoying bugs, like a misspelt variable name, on a regular basis.
Bugs are really hard to track down.

I got pretty far with Lua, having developed a lot of features.

At that time I came up with the idea of using **chains** for implementing events.
In short, chains in my interpretation are responsibility chains that do something with the `context` they are given, kind of like the stack of handler functions on backend that in sequence modify the `request` and `response` objects.
At any point the propagation of the `context` may be stopped by a handler, to avoid the execution of the handlers down the line.
Also, each of the handlers has an associated priotity, by which they stay sorted in the underlying data structure. 
See more on chains, including implementation details in future sections.

This idea proved essential to the way I ended up handling movement, attacking, taking damage etc.

During this time, I also realised that, in order for the system to be really robust, I must use dynamic components. 
More on this, likewise, in future chapters.

This stage of the project is pretty well-documented, which is essential when you don't even have types in your language.
I wrote a couple of articles explaining some of the mechanics and API's of the system, which you may find [here][2].
Some of the ideas documented there translated almost intact into the new version of the code.


### 2.3.3. C# rework

Finally, I got sick of Lua not having types. 
I decided to go ahead and rewrite the entirety of the project for C#.
Why C#? 
I did not care what game engine I will end up using, I was just focused on the logic part, i.e. the development of the system.
I knew there are *Unity* and *Godot*, which both support C# as their scripting language.
So the idea was to write the core code independent of the graphics.
This concept is commonly called *MVC (Model-View-Controller)* or *MVVM (Model-View-ViewModel)*. 
With this, it will be possible to create "visualizer scripts" for any game engine that supports C#.

This idea is nothing new and it's actually what I was thinking of initially.
However, before this project evolved into using C#, the idea of how the communication between the view and the model should be organized had been pretty vague to me.
Before the transition from the Lua version, I had not even tried to code a robust enough system to handle that.
I kind of slapped together a good enough for testing purposes prototype, and let it slide.

So, the C# version was initially done solely in console.
At the time, I did not even know how to write automated tests or rather had not bothered to learn how to do it.
The tests were manual and based on inspection. 
I had a script that would print out a bunch of information of how objects interacted in the game and I would skim throught that to see if a feature worked as expected.

For this starter C# version I basically recoded all of the Lua code in C# and also enhanced some of the ideas.
The code became more robust, but not robust enough.

There were a lot of maintenance issues that I had that slowed down programming and made it annoying.
In short, I used factories to build out my entity types as well as builder classes for their initial chains.
Thing is, with factories, you have this tight coupling of the factory and the class it builds.
So when I changed the entity, I had to go back and change the factory too.
When I changed how the chain functions, I had to go back and see if the builder works right.

I had the concept of *tinkers* and *retouchers* (both made up terms) which both existed just to help to add (remove) handlers to (from) chains.
The sole difference between them is that retouchers are used for entity *types* (on factories) while tinkers are used for entity *instances*.
They do the same thing, while only being different in the container they target. 
The fact that they do the same thing means code duplication and maintenance issues.
However, since they do the same thing, there is no point in telling them apart.

I did kind of realise this, but I did not know how to fight against this at the time.
It has been remedied only by code generation, lately.

The other maintenance issue was *boilerplate* code.

There is really no way around boilerplate code with plain C#.
I know there is reflection, but it is unreliable and error-prone, as well as really slow.
I did use reflection to get rid of boilerplate in some places, like adding together stat objects, which are just structs with a bunch of ints.

Another tool I tried using to get rid of boilerplate were generic interfaces. 
These work to a degree, but make the code too complicated.

### 2.3.4. Unity and Godot

A couple of months after switching to C#, the codebase got mature enough to try to make a view on Unity or Godot.

Initially, I made a small demo for [Unity][4]. 
It featured a generic controller, which worked with interfaces and so was later reused for the [demo Godot version][5] (not the current version).
This time I designed a prototype for the controller that was a little more robust, but still lacked a lot of features and was too annoying to enjoy working with. 
Its deficiencies were addressed in the new version, developed mainly by my colleague, who describes it at length [in his work][6]. 
<!-- This is not yet true!! --> 
The former hairiness was salvaged by means of code generation.

Game engine features, as mentioned above, do not affect my work in a significant way, which is why the description of those will be omitted.
My colleague, however, had to work more closely with the engine, so I encourage you to go see [his work][6] for more information on game engine details.
My part of this job was to derive the essential to the game API, which was done independently of any game engine.
For me, a game engine simply provided a sort of a visualisation of my code.
This way of visualizing what the code does can sometimes be helpful to identify certain bugs. 
The point is that humans understand visual input more intutively than console logs or the call stack and so sometimes the problem is more apparent when you see it pop up in action.


### Code generation

Since april I've worked on code generation for eliminating boilerplate and for making the development process less cumbersome.

#### Reasons for code generation

Code generation is essential, because it encourages experimentation. When I see a pattern that cannot be easily exploited without code generation, I can quickly code a prototype module for my code generator that would exploit that idea. If it turns out to be useful, I just leave this new module in. If it does not turn out great, undoing it is as simple as, e.g. skipping a step in code generation. I would not have to go through dozens of files or roll back a git commit.

Code generation prevents repeating this boilerplate code in dozens of files, while also providing any future code with out-of-the-box features. 
It is easier to manage, since all that has to change is the rules of how the code is generated to automatically apply changes to all classes that used the feature.
It is easier to expand on, because it as well takes just a few rule changes in the code generator and does not involve refactoring dozens of files.
It provides automatic documentation. Just imagine keeping similar comments in dozens of files up to date.

#### Tools in short

I have been using `T4`, short for `Text Template Transformation Toolkit` for creating templates, along with `Roslyn` for source code analysis. I would mark classes in my source code with certain user-defined attributes to enable certain code to be generated when the code generator is run.

My approach on code analysis is pretty simplistic. 
It does not monitor the code live, connecting to a language server. 
Instead, when the code generator is run, it deletes all of its previous output, then reads the source files and analyzes them, then just regenerates the code again. 
Yes, it is slow, but it is also way easier to implement. 
The slowest part of the process is reading in and analyzing the source code, so it could definitely be optimized with a language server.



### 2.3.5. Example illustrating why if-statements do not cut it. 

Say you wanted to program a simple *Snake* game. 
It has a well-defined limited set of features and mechanics that you do not plan to expand.
Then it can be coded quickly with a bunch of if statements:

```C++
// change direction
if (direction == LEFT || direction == RIGHT)
{
    if (pressed_down) direction = DOWN;
    else if (pressed_up) direction = UP;
}
else
{
    if (pressed_left) direction = LEFT;
    else if (pressed_right) direction = RIGHT;
}

// move
position += direction;

// update state
if (is_off_screen(position) || is_snake_at_position(position)) 
{
    game_over();
} 
else if (is_apple_at_position(position))
{
    score++;
    destroy_apple();
    create_apple(); // cannot be at `position` or either position of the snake
}
else
{
    delete_first_snake_position();
    add_snake_position(position);
}
```



# 3. References

[1]: https://github.com/AntonC9018/Dungeon-Hopper "Dungeon-Hopper github page"
[2]: https://antonc9018.github.io/Dungeon-Hopper-Docs/ "Dungeon-Hopper documentation"
[3]: https://github.com/AntonC9018/hopper.cs "hopper.cs github page"
[4]: https://github.com/AntonC9018/hopper-unity "Hopper: Unity demo github page"
[5]: https://github.com/AntonC9018/hopper-godot "Hopper: Godot demo github page"
[6]: <citation_needed> "Colleague's work"