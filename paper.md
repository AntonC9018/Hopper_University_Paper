
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
    - [2.3.5. Code generation](#235-code-generation)
      - [2.3.5.1. Reasons for code generation](#2351-reasons-for-code-generation)
      - [2.3.5.2. Tools in short](#2352-tools-in-short)
      - [2.3.5.3. My workflow](#2353-my-workflow)
    - [2.3.6. Example illustrating why if-statements do not cut it.](#236-example-illustrating-why-if-statements-do-not-cut-it)
- [3. Overview of the system](#3-overview-of-the-system)
  - [3.1. Game mechanics overview](#31-game-mechanics-overview)
    - [3.1.1. Types of actions](#311-types-of-actions)
    - [3.1.2. The goal](#312-the-goal)
    - [3.1.3. The items](#313-the-items)
    - [3.1.4. The enemies](#314-the-enemies)
    - [3.1.5. The time limit](#315-the-time-limit)
    - [3.1.6. More ideas](#316-more-ideas)
  - [3.2. System design overview](#32-system-design-overview)
    - [3.2.1. How NOT to write code](#321-how-not-to-write-code)
    - [3.2.2. Separation and events is the key idea](#322-separation-and-events-is-the-key-idea)
    - [3.2.3. A wrong turn?](#323-a-wrong-turn)
      - [3.2.3.1. The idea of a History](#3231-the-idea-of-a-history)
      - [3.2.3.2. What's the problem though?](#3232-whats-the-problem-though)
      - [3.2.3.3. The Solution](#3233-the-solution)
      - [3.2.3.4. Is it all?](#3234-is-it-all)
    - [ECS (Entity-Component-System)](#ecs-entity-component-system)
      - [Introduction](#introduction)
      - [Why not OOP?](#why-not-oop)
- [4. References](#4-references)

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
It allows exporting on mobile and desktop. See the github repository [here][1].

However, my understanding of how such games actually work was quite poor at the time.

Designing and implementing a simple game is entirely different from what I was faced with.
If you are designing a game that could have thousands of different effects, mechanics and creatures and possibly expanded by mods, you cannot account for every item with a bunch of if-statements, you actually need more involved abstract systems making use of *some* kind of polymorphism.
I did not realize this before this project, but quickly understood it after this initial attempt.
I will expand on this more in a separate chapter.

This initial attempt at coding the game made me understand that complex and scalable games are not a bunch of if statements.
They require creativity and competence.

The initial code was scrapped completely and rewritten in the second version, still on Corona.

### 2.3.2. Corona & Lua: Stage 2

Lua is a really simplistic language: there is no concept of types, modules or classes.
Dynamic method dispatch, however, can be simulated via metatables (prototypical inheritance).
There also are no arrays: both arrays and dictionaries are represented via so-called tables.

The biggest problem with Lua is its lack of types and, consequently, its lack of static analysis.
One has to deal with simplest annoying bugs, like a misspelt variable name, on a regular basis.
Bugs are really hard to track down.

I got pretty far with Lua, having developed a lot of features.

At that time I came up with the idea of using **chains** for implementing events.
In short, chains in my interpretation are responsibility chains which do something with the `context` they are given, kind of like the stack of handler functions on backend which in sequence modify the `request` and `response` objects.
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

I had the concept of *tinkers* and *retouchers* (both made-up terms) which both existed just to help to add (remove) handlers to (from) chains.
The sole difference between them is that retouchers are used for entity *types* (on factories) while tinkers are used for entity *instances*.
They do the same thing, while only being different in the container they target. 
The fact that they do the same thing means code duplication and maintenance issues.
However, since they do the same thing, there is no point in telling them apart.

I did kind of realize this, but I did not know how to fight against this at the time.

The other maintenance issue was *boilerplate* code.

There is really no way around boilerplate code with plain C#.
I know there is reflection, but it is unreliable and error-prone, as well as really slow.
I did use reflection to get rid of boilerplate in some places, like adding together stat objects, which are just structs with a bunch of ints.

Another tool I tried using to get rid of boilerplate were generic interfaces. 
These work to a degree, but make the code too complicated.

All of the problems described above have been remedied only recently, by code generation.

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


### 2.3.5. Code generation

Since april I've worked on code generation for eliminating boilerplate and for making the development process less cumbersome.

#### 2.3.5.1. Reasons for code generation

Code generation is essential, because it encourages experimentation. When I see a pattern that cannot be easily exploited without code generation, I can quickly code a prototype module for my code generator that would exploit that idea. If it turns out to be useful, I just leave this new module in. If it does not turn out great, undoing it is as simple as e.g. skipping a step in code generation. I would not have to go through dozens of files or roll back a git commit.

Code generation prevents repeating this boilerplate code in dozens of files, while also providing any future code with out-of-the-box features. 
It is easier to manage, since all that has to change is the rules of how the code is generated to automatically apply changes to all classes that used the feature.
It is easier to expand on, because it as well takes just a few rule changes in the code generator and does not involve refactoring dozens of files.
It provides automatic documentation. Just imagine keeping similar comments in dozens of files up to date.


#### 2.3.5.2. Tools in short

I have been using `T4`, short for `Text Template Transformation Toolkit` for creating templates, along with `Roslyn` for source code analysis. I would mark classes in my source code with certain user-defined attributes to enable certain code to be generated when the code generator is run.

My approach on code analysis is pretty simplistic. 
It does not monitor the code live, connecting to a language server. 
Instead, when the code generator is run, it deletes all of its previous output, then reads the source files and analyzes them, then just regenerates the code again. 
Yes, it is slow, but it is also way easier to implement. 
The slowest part of the process is reading in and analyzing the source code, so it could definitely be optimized with a language server.


#### 2.3.5.3. My workflow

My process of turning repeating code into generated code is loosely as follows:
1. When writing code, I see a pattern that could be exploited via code generation.
2. If the pattern is not clear enough, I wait until another piece of code encounters a similar problem, until the problem is clear enough in my head to propose a generic solution.
3. I try solving it without code generation, in simplest way possible (hopefully without generic interfaces).
4. If I cannot come up with a simple generic solution, I enable code generation for the given idea.


<!-- Incomplete! -->
### 2.3.6. Example illustrating why if-statements do not cut it. 

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


# 3. Overview of the system

## 3.1. Game mechanics overview

As has been mentioned, the game mechanics are based on those from Necrodancer.

The game takes place in a 2d grid world and it is turn based.
You control a character positioned in one of the cells in the grid.
Every turn, you may take an action, like move in on of the directions to an adjacent cell, attack an enemy on an adjacent cell, dig an obstacle or perform one of the special actions, like casting a spell.
You may also skip your turn, without doing anything.

After you have done your action, all of the enemies are given the chance to take an action, one by one.
Which action is taken is determined by their AI (an algorithm for selecting the next action) and can in fact be anything from plain attack/move to, likewise, casting a spell.

There are a few more things that take place after this, which we'll get into later.


### 3.1.1. Types of actions

An important concept to address is that the player may only select between two types of actions:
1. *Vector actions* (or `directed actions`, governed by directional inputs (arrow keys). These include attacking, moving and digging in a specified direction.
2. *Special actions* (mostly `undirected actions`), like casting a spell or activating some item. 
These actions are executed by pressing one of the designated keys, without requiring a simultaneous directional input (arrow key). 
Those that do need a direction to work properly, like launching a fireball in a certain direction, may use the current orientation of the character, or set the direction by other means.

The important thing to understand is that the player does not have control over what action will be done exactly in case of a vector action. 
More precisely, all possible actions will be tried in order and the first that was able to be executed terminates the action execution process.

For example, if player provided the input `up`, first the character would try to attack in the upward direction, then, if there was no enemy to attack, they would try digging the obstacle in the upward direction, then, if there was no obstacle, they would go ahead and try moving up a tile.

This is opposed to the special actions, which are commonly mapped directly to certain effects or activated items. 
For example, say, the player presses the `S` key, which is mapped to holding up the shield. 
So pressing the `S` key will always execute the exact action it is mapped to (in general, but there are exceptions).

As a result of this paradigm, the player can execute any available action at any given point pressing at most one key.


### 3.1.2. The goal

The player is faced with the problem of completing a randomly generated level.
The levels consists of a few connected rooms, each room containing enemies to fight.
There is one final room with a door (a trapdoor, a staircase or a doorway) to the next level.
Once the player is able to beat a few such levels, they are faced with a boss.
Beating the boss either lets the player procceed to the next level, or results in an overall victory.

The levels get progressively more difficult. In particular, monsters get more health, new and more complicated monster variants appear, the number of floor hazards like spikes or ponds increase, etc.
At the same time, player may get items while clearing the floor, which grant new passive or active abilities, increase stats. So the player gets stronger while progressing as well.


### 3.1.3. The items

The inventory of the player has a few item slots, each either associated a role, like weapon, spell and shovel, or an armor part, like boots or the helmet. 
Those slots which are activated are mapped to a an input, so providing that input would also activate the item in that slot. 

The player may pick up items by stepping on them, thereby they are placed automatically in the slot assigned to them. If there is already an item in that slot, that item is replaced with the one just picked up.

Some items may not have an associated slot. 
Such items as a rule just boost player's stats or slightly change a specific behavior.
For example, there may be an item that does damage to all enemies around the enemy hit by the player.

Assume, for simplicity, there may not be two copies of the same item at the same time equipped by the player.


### 3.1.4. The enemies

Each enemy has a clearly defined behavior. 
They select actions according to a well-understood strategy.

For example, a simple enemy may have the following strategy: skip an action, then attack or move in the direction of player.

The enemies must be predictable for the player to be able to quickly evaluate a given situation and be certain in one's actions.
Ideally, nothing unexpected should ever happen.

Likewise, every enemy must have a way to beat it, some simple pattern of moves for the player to follow to always come up ahead.
The joy of gameplay is in learning the enemy move set, coming up with such patterns and strategies of beating them, and evalualing the situation quickly, coming up with a good action on the fly, in case the enemies come in packs. 


### 3.1.5. The time limit

As has been mentioned, the most intriguing idea is that there is a time limit for every action.
More specifically, the actions must be done to the beat of the music (with some leeway).

This is an essential detail in the design of the game. 
I'd say it is *the* core mechanic borrowed from Necrodancer.
However, this part is relatively independent of other game mechanics, like moving the player within the grid and the item system, and it's not the focus of this work.
This work is mostly focused on my implementation of the other parts of the game: the action system, the item system etc.


### 3.1.6. More ideas

When the engine is done, more ideas would become easy to explore.

I would like to try turning this game in a PVP arena, or a MOBA, keeping the base mechanics and the idea with doing actions to music in place. 
I do not know how viable this would be, but it does seem pretty intriguing.


## 3.2. System design overview

I'm more or less concerned with just the engine, that is, how the logic is going to work, how items, actions, enemy AI are implemented and the tools for e.g. code generation.
I'm also interested in allowing the extension existing content via mods.


### 3.2.1. How NOT to write code

One of the most important topics of game development is how to neatly show what is happening in the game on the screen, with animations, particles and the right sprites being shown.

One way of doing this is to refer to the code that controls the *View*, that is, what you see on the screen, directly in the game logic code. For example, something like this (pseudocode for understanding, not actual code from the game):

```C#
void Move(IntVector2 direction)
{
    if (!Grid.HasBlockAt(this.position + direction))
    {
        SetAnimation(Animation.Hopping);
        TranslateSprite(
            to: this.position + direction, 
            timeInMs: 500, 
            callback: () => SetAnimation(Animation.Idle));
        this.position += direction;
    }
}
```

However, this has some drawbacks:
1. Your game logic code is now tightly coupled with the view. You mix together code that can potentially be separated, thus making it harder to read, understand and maintain.
2. The code you wrote is very unstable. 
Assume for a moment that the player, after having had moved to the new position, have triggered a trap that killed him. That should trigger the kill animation, but, instead, the idle animation set in the callback is playing. Obviously, this is a toy example, but you can already see that setting callbacks like that is no good. You need a more complex system for handling it.
3. What if the player is sliding instead of hopping? Then, a different animation needs to be set, not `Animation.Hopping`, but `Animation.Sliding`. Would you add a check for sliding in the `Move()` function? But what if sliding came from a mod? Then your system would have had no idea of it. Clearly, such simple strategy is not going to work here.

So, to sum up, the drawbacks are:
1. Tight coupling.
2. Maintenance issues.
3. Inflexibility.


### 3.2.2. Separation and events is the key idea

I am going to illustrate how separation of components and events solve all of the issues outlined above.

So, to address tight coupling, just imagine there were two functions, one responsible for moving, while the other for the animations.

```C#
void Move(IntVector2 direction)
{
    if (!Grid.HasBlockAt(this.position + direction))
    {
       this.position += direction; 
    }
}

void AnimateMove(IntVector2 newPosition)
{
    SetAnimation(Animation.Hopping);
    TranslateSprite(
        to: newPosition, 
        timeInMs: 500, 
        callback: () => SetAnimation(Animation.Idle));
}
```

This is still not ideal, implementation-wise (callbacks and so on), but we have a bigger problem here. 
There is currently no way for these functions to communicate. 
Calling `AnimateMove()` in `Move()` does not work, since that would mean that we just refactored the animation code in a function, but they are still tighly coupled. 
Our goal was to separate the game logic from the view. How do we do it?
Events (signals) to the rescue!

The idea is to define a queue of handlers, code in which will be executed when the player moves.
This queue may be static, configurable for particular types of entities.
Still in pseudocode:

```C#
static EventQueue<Handler> moveEvent;

void Move(IntVector2 direction)
{
    if (!Grid.HasBlockAt(this.position + direction))
    {
       moveEvent.Dispatch(this, this.position + direction);
       this.position += direction;
    }
}

void AnimateMove(IntVector2 newPosition)
{
    SetAnimation(Animation.Hopping);
    TranslateSprite(
        to: newPosition, 
        timeInMs: 500, 
        callback: () => SetAnimation(Animation.Idle));
}

void Setup()
{
    moveEvent.AddHandler(AnimateMove);
}
```

Now, the `Move()` function knows nothing about the view. 
It just dispatches an event every time the player moves.

However, this still does not solve the problem with e.g. sliding. 
The player does not slide by default. 
Sliding is an effect applied to them at runtime.
If we wanted to animate sliding correctly, we need a way of changing this queue at runtime.
So, we'll make the event queue a property of a player instance, not just of the player type, so that we could modify it at runtime.

And now, that we have separated them, we can resolve the maintenance issues as well.
Since the view part can be factored in a fully-fledged independent system, this problem too can be solved with a bit more thought.


### 3.2.3. A wrong turn?

So, my initial idea was that the model should be separated from the view, but I did not know how to do it exactly.
I did know of events (signals) and I did use it, but the realization that they can be used for communication between the view and the model has not come to me until lately.
I just thought about this a little differently.
I though about the view and the model as these two completely independent systems, the view being connected to the model with a tiny bridge.
This can work, but it is not very scalable.
Instead, the view should be connected to the model all over the place, via events, while the model knows nothing about the view.

#### 3.2.3.1. The idea of a History

Initially, I imagined model and view being connected via the *history*.
The model would push updates on what events happened in the world throught this history.
For example, when the player is attacked, the `being attacked` update is saved on the history.
The view would update its state and decide what animations to play after all of the events have happened.

So I imagined it this way: there are a bunch of separated state machines in the player view, all responsible for the different events. 
For example, there is a state machine for a dash. A dash means an attack immediately followed by a movement. 
There is also a state machine for moving, which consists of just the moving update. 

So, after a turn in the model has been processed and the history has been filled up, the view would get the history and try running all of the state machines on it. 
So, if a player both attacked and then moved on the same turn, the view will receive the history containing 2 updates: attacking and moving. 
Each of the state machines will then be tried. 
The dash is attacking then moving, so this state machine would succeed. 
The state machine for moving would also succeed, since the moving update is present.
Out of these 2, the view will select the more complex one, that is, the dash, to display animations for.

I even had a more intuitive term for this concept: sieves. 
Each state machine is a sieve that gets clogged when you try to sieve the history through it. 
When the history has been let through all of the sieves, the most complex clogged sieve is selected and the animations associated with that sieve are played.


#### 3.2.3.2. What's the problem though?

The problem comes when you need to pass data along with the updates.

Ok, you *could* pass any data with the updates, but then there is no clear way of seeing which event this is, without casting the passed data to a known type. 
This leads to ugly `if-else` like this, to figure out the correct type.
This is definitely a code smell.

```C#
foreach (object update in history)
{
   if (update is AttackingUpdate attackingUpdate)
   {
       // do something with the data from `attackingUpdate`
       // ...
   }
   else if (update is MovingEvent movingEvent)
   {
       // you get the idea
   }
}
```

Since the hole you are trying to push these updates through from model to view is so narrow, you must convert updates to an analog of the `object` type, losing the actual type of the update in the process.
This is known as type erasure.

But wait, can't you use polymorphism instead of `if-else`'s to call the functions you need to process the data? 

Well, since the model does not know anything about your view logic associated with the updates, but it does jsut know the data in the updates, no, this is not possible. 
You cannot give the model a type with that data to instantiate (so that it has your polymorphic functions). 
That is, you *could*, it's just not very convenient and there are simpler ways of achieving the same result.

You *could* try maintaining a dictionary of handlers mapped to by the type of the update, like below.
This is a stinky code smell and maintaining such code is extremely annoying.

```C#
void HandleAttack(object update)
{
    // First cast to the needed type
    var attackingUpdate = (AttackingUpdate) update;
    // Do something with the data ...
}

void HandleMove(object update)
{
    // First cast to the needed type
    var movingUpdate = (MovingUpdate) update;
    // Do something with the data ...
}

// Type is the type info of the given class.
// Action<T> is a void function that takes in T as an argument.
Dictionary<Type, Action<object>> typeErasedHandlers
{
    { typeof(AttackingUpdate), HandleAttack },
    { typeof(MovingUpdate),    HandleMove   }
};

void SieveThroughHistory(History history)
{
    foreach (object update in history)
    {
        typeErasedHandlers[typeof(update)](update);
    }
}
```

#### 3.2.3.3. The Solution

Fortunately, there is a better way of dealing with this.

The idea is to allow multiple points of contact between the view and the model.
This way, the history stage can be bypassed completely.
The model does not have to *push* any "updates" to the history. 
All it does is it dispatches the corresponding event with all of the data that it is currently dealing with, stored in a context.
As a toy example (again, not real code):

```C#
class AttackingContext
{
    Player player;
    Enemy attackedEnemy;
    IntVector2 direction;
}

class Player
{
    // ...

    EventQueue<AttackingContext> attackEventQueue;

    void Attack(IntVector2 direction)
    {
        var enemy = Grid.GetEnemyAt(this.position + direction);
       
        if (enemy != null)
        {
            var context = new AttackingContext(
                player        : this,
                attackedEnemy : enemy,
                direction     : direction);
            
            attackEventQueue.Dispatch(context);

            enemy.TakeDamage(this.damage);
        }
    }
}

class PlayerView
{
    // ...

    void AttackHandler(AttackingContext context)
    {
        // Do something with:
        // context.player
        // context.attackedEnemy 
        // context.direction     
    } 

    void Setup(Player playerInstance)
    {
        playerInstance.attackEventQueue.AddHandler(AttackHandler);
    }
}

```

This idea may be obvious now that I have illustrated it, but it has not been obvious to me until recently.
I had to go through all the misery of history explained above to come to this revelation.

So, with this design we have been able to separate the model and the view, while being able to pass data from the model to the view without involving type erasure and even without the model knowing anything about the view.

#### 3.2.3.4. Is it all?

There are still a few problems with this design.

One of them mostly has to do with the inconvenience of certain things that come with using this design.
I have been able to address these with code generation.

Another problem is with ordering of handlers. 
I was able to solve that problem by introducing priorities.

I will be discussing both of these later in the work.


### ECS (Entity-Component-System)

A lot has been said about ECS's.
However, I strongly believe that you cannot understand them completely unless you rediscover them yourself.
The moment when you see an actual problem and attempt to solve it with different methods, including ECS, that's when the actual understanding is born.

#### Introduction

ECS is a way of viewing the space of your program in a different way. 

ECS states that there is a world and any object in that world is an *entity*.
All entities start off as just an empty object with an identifier.
It is a skeleton, to which you apply *components* to enable certain behavior or property.
Components usually just contain data.

All the game mechanics are just interactions between objects in the world.
These are conceptualized as *systems*.
They operate on individual *components* of entities, thereby enabling certain behavior.

The idea behind ECS's is, essentially, flexible, dynamic entities.


#### Why not OOP?

If you ever tried using OOP for representing types of entities in a dynamic environment, you know it is *not* going to work.
1. One cannot apply inheritance and hierarchies properly.
2. Static types are too rigid.

So, imagine for a second that you have a `Player` class. 
A player can do many things, including moving, attacking and digging.

Now, you create another class, `Enemy`. 
You notice that the enemy can move and attack, but it has a different control scheme: the player is controlled by user input, while the enemy by an AI.

So you might be tempted to factor out the common things, namely, attacking and moving, in a base class.
The `Player` class will then inherit from this base class, adding the ability to dig, as well as their own input scheme, and so will the `Enemy`, adding their AI algorithm.

But then a new type of `Enemy` comes along: it can attack, move and dig, while also having an AI.
Where in your hierarchy will you put this new class? 
Should it inherit from `Enemy`? 
But then it will have to add the digging, which is already implemented in the `Player` class. 
Should you factor the digging in another base class, like `DiggingMovingAttackingBase`? 
No, because then you cannot inherit the AI from the `Enemy` class. 
Should you instead inherit the `Enemy` class from this new base class? 
Again, no, because `Enemy` cannot dig by design. 

So, with even this simple example, the typical OOP inheritance idea breaks down.
Now, imagine the same scenario but amplified 100 times: there are hundreds of properties and behaviors any entity could have.
This is impossile to model with a hierarchy.

Se second point is that the entites, if they are modeled as instances of static types, cannot alter their behavior at runtime.
In a real game, the player may start of not having the ability to dig, but once thay acquire a pickaxe, they may learn this new ability.
However, you cannot dynamically modify the `Player` type to become able to dig.
Making it able to dig off the start likewise does not make sense, because it learned to do it *eventually*.

Another example: you have a two stage monster, say, an angry butterfly that initially start as an innocent caterpillar, so it cannot even attack, but then it transforms into an actual buttefly, gaining the ability to fly and attack the player.

With OOP there is essentially just one way to model this.
You would have two classes, one modeling the caterpillar state, and another class, modeling the butterfly state.
To transform the caterpillar into a butterfly, you would destroy the caterpillar and spawn a new butterfly.

With dynamic types you have 2 possibilities.
You may either do as above: destroy the caterpillar and spawn a butterfly, or you may morph the caterpillar into a butterfly by giving it the `Flying` and the `Attacking` behaviors.
In this sense, the latter is more flexible.



# 4. References

[1]: https://github.com/AntonC9018/Dungeon-Hopper "Dungeon-Hopper github page"
[2]: https://antonc9018.github.io/Dungeon-Hopper-Docs/ "Dungeon-Hopper documentation"
[3]: https://github.com/AntonC9018/hopper.cs "hopper.cs github page"
[4]: https://github.com/AntonC9018/hopper-unity "Hopper: Unity demo github page"
[5]: https://github.com/AntonC9018/hopper-godot "Hopper: Godot demo github page"
[6]: <citation_needed> "Colleague's work"