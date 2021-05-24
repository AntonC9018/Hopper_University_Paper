
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
    - [3.2.4. ECS (Entity-Component-System)](#324-ecs-entity-component-system)
      - [3.2.4.1. Introduction](#3241-introduction)
      - [3.2.4.2. Why not OOP?](#3242-why-not-oop)
      - [3.2.4.3. Compression](#3243-compression)
      - [3.2.4.4. My ECS](#3244-my-ecs)
- [4. Technical topics](#4-technical-topics)
  - [4.1. The grid](#41-the-grid)
    - [4.1.1. Cells](#411-cells)
    - [4.1.2. Components having to do with position and movement](#412-components-having-to-do-with-position-and-movement)
      - [4.1.2.1. Transform](#4121-transform)
      - [4.1.2.2. Displaceable](#4122-displaceable)
      - [4.1.2.3. Moving](#4123-moving)
      - [4.1.2.4. Pushable](#4124-pushable)
    - [4.1.3. Block](#413-block)
      - [4.1.3.1. Directed entities](#4131-directed-entities)
    - [4.1.4. Enter and Leave events](#414-enter-and-leave-events)
  - [4.2. Chains](#42-chains)
    - [4.2.1. Responsibility chains](#421-responsibility-chains)
    - [4.2.2. Priority](#422-priority)
      - [4.2.2.1. How is the priority assigned?](#4221-how-is-the-priority-assigned)
    - [4.2.3. Types of chains](#423-types-of-chains)
  - [4.3. Entities and Components](#43-entities-and-components)
    - [4.3.1. Structure of Entities](#431-structure-of-entities)
    - [4.3.2. What do components need to function?](#432-what-do-components-need-to-function)
    - [4.3.3. Entity types](#433-entity-types)
      - [4.3.3.1. The 3-step procedure](#4331-the-3-step-procedure)
      - [4.3.3.2. Problems](#4332-problems)
    - [4.3.4. Component copying](#434-component-copying)
      - [4.3.4.1. Why even copy components?](#4341-why-even-copy-components)
      - [4.3.4.2. Implementation](#4342-implementation)
    - [4.3.5. Entity factory](#435-entity-factory)
    - [4.3.6. Entity wrappers](#436-entity-wrappers)
    - [4.3.7. Loading entity types from JSON at runtime](#437-loading-entity-types-from-json-at-runtime)
  - [4.4. Acting and the Game Loop](#44-acting-and-the-game-loop)
  - [4.5. Targeting?](#45-targeting)
  - [4.6. Items?](#46-items)
  - [4.7. Pools and Loot tables?](#47-pools-and-loot-tables)
  - [4.8. World generation](#48-world-generation)
  - [4.9. Code generation](#49-code-generation)
- [5. References](#5-references)

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

For example, if the player provided the input `up`, first the character would try to attack in the upward direction, then, if there was no enemy to attack, they would try digging the obstacle in the upward direction, then, if there was no obstacle, they would go ahead and try moving up a tile.

This is opposed to the special actions, which are commonly mapped directly to certain effects or activated items. 
For example, say, the player presses the `S` key, which is mapped to holding up the shield. 
So pressing the `S` key will always execute the exact action it is mapped to (in general, but there are exceptions).

As a result of this paradigm, the player can execute any available action at any given point pressing at most one key.


### 3.1.2. The goal

The player is faced with the problem of completing a randomly generated level.
The levels consist of a few connected rooms, each room containing enemies to fight.
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
I'm also interested in allowing the extension of existing content via mods.


### 3.2.1. How NOT to write code

One of the most important topics of game development is how to neatly show what is happening in the game on the screen, with animations, particles and the right sprites being shown.

One way of doing this is to refer to the code that controls the *View*, that is, what you see on the screen, directly in the game logic code (the *Model*). For example, something like this (pseudocode for understanding, not actual code from the game):

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
I did know of events (signals) and I did use them, but the realization that they can be used for communication between the view and the model has not come to me until lately.
I just thought about this a little differently.
I though about the view and the model as these two completely independent systems, the view being connected to the model with a tiny bridge.
This can work, but it is not very scalable.
Instead, the view should be connected to the model at a multitude of points of contact, via events, with the model knowing nothing about the view.

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

Well, since the model does not know anything about your view logic associated with the updates, but it does just know the data in the updates, no, this is not possible. 
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


### 3.2.4. ECS (Entity-Component-System)

A lot has been said about ECS's.
However, I strongly believe that you cannot understand them completely unless you rediscover them yourself.
The moment when you see an actual problem and attempt to solve it with different methods, including ECS, that's when the actual understanding is born.

#### 3.2.4.1. Introduction

ECS is a way of viewing the space of your program in a different way. 

ECS states that there is a world and any object in that world is an *entity*.
All entities start off as just an empty object with an identifier.
It is a skeleton, to which you apply *components* to enable certain behavior or property.
Components usually just contain data.

All the game mechanics are just interactions between objects in the world.
These are conceptualized as *systems*.
They operate on individual *components* of entities, thereby enabling certain behavior.

The idea behind ECS's is, essentially, flexible, dynamic entities.


#### 3.2.4.2. Why not OOP?

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


#### 3.2.4.3. Compression

Another idea is to give every entity the entire range of possible properties and abilities and just not let them use most of them. 
This way, it is easy to enable some of the abilities later: you just have to e.g. set some flag that indicates whether you entity can use that ability.

There are two problems with this:
1. The more components or properties you have in your game, the more bloated your entities become, the more space they take. Not just one entity, but all of them at once.
2. It cannot be extended by mods, which is a no-no in my case. One of my project goals is to allow modding.

So, storing components in contrast to every entity having every property naturally leads to more *sparse* entities, in other words, to the idea of *compression*.


#### 3.2.4.4. My ECS

I have a little bit of a special perspective on ECS, currently.
- The notion of a *system* is pretty vague in my code.
- There is a distinction between *data components* (or simply *components*) and *behaviors*.
- In my code, behaviors are the ones defining *events* (*chains* are used, more on them later). 
So, behaviors in this case are a fusion of a component and a system.
As has been described above, events prove essential in binding together the view and the model.
- There is a concept of a type. 
A type is essentially a template by which the entities are constructed on instantiation.
Types are currently modeled with another entity (a *subject*), which is cloned on instantiation to create a new instance of that type.
The instance then becomes independent of the subject and may change at runtime in any way, without affecting the subject.
Types therefore can be augmented with components at type construction time, just like entities at runtime. 

I'm a little bit worried about the performance of my ECS. 
The thing is, it is what's called a "fake" ECS.
ECS's generally put a lot of focus on storing the different components in some central linear place in memory to be able to feed those components into systems sequentially (sequential iteration is way faster).
Manual memory management also improves performance, saving a lot of work for the GC (garbage collector).

I am doing it the "I don't care" way, that is, just allocate all components on the heap with the `new` operator.
This is, in fact, both the expected and the easy way of doing this in C#, but it's not performant at all.

Doing an ECS in the right way in C# is a very hard feat to accomplish.
Structs and arrays of structs are the only way of storing data directly in memory and not somewhere on the heap.
C# lacks tools of doing manual memory management, like the ones found in C++, because you're just not assumed to care about memory management when doing C#.
I even once considered migrating the project into C++, but C++ has its own faults, e.g. the fact that modding is going to be a lot more challenging to implement, so in the end I settled with a fake ECS instead.



# 4. Technical topics

In this section, I present some of the elements of the game. 
In particular, I explain their motivation and the way they have been implemented, with concrete code examples from the source.


## 4.1. The grid

As has already been mentioned, the world is represented as a 2d grid with entities.
Now, since the query operations of finding an entity at a specific cell, seeing if there is a block at a specific cell are so common, it is beneficial to store the entites (more explicitly, their *transforms*) by their current coordinates, in a literal 2d array. This is, in fact, the way I decided to model it ([see e.g. the constructor][7]. 


### 4.1.1. Cells

Every cell is assumed to have different layers, where entities on each layer have slightly different properties. 
For example, generally, a spiked trap, which damages the player when they step on it, cannot be attacked by players, but can be exploded by bombs. 
This is because the layer in the cell that the trap is located at is the `trap` layer, while the player or enemies can only target the `real` layer with their normal attacks.
Anyway, this is how I decided to model this idea.

Before the rework, I used to have a slot for each of the layers in each cell, but that was not good, at least because most of the layers were empty most of the time, since there was nothing at those positions.
See, for example, [the former Cell class, in lua][8].

This had another drawback: there can only be one entity in that layer at a time. 
This makes entities that can go through other entities of the same layer either impossible to implement, or just difficult to think about.

I since realized I could store the entities in a list, and then retrieve the entity from a needed layer by iterating through that list. 
Linear search is in fact acceptable in this case, because a cell usually won't have more than 1-2 entities.
Cases when there are more entities are rare and can be basically neglected.

Another small benefit of this approach is that an entity can change its layer at runtime without needing to update where it is stored in the cell.

The current implementation of a cell involves inheriting from `List<Transform>`. 
See [the current implementation][9].
I personally see nothing bad in this approach, although [a lot of bad things has been set about this][10].
People often bring up *composition over inheritance*, how composition is more flexible, but this isn't really a case of that. 
This is more about avoiding boilerplate by not writing out the implementation of `IList<Transform>`, forwarding all calls to a private member of type `List<Transform>`.
This, at the same time, makes the code more erroneous, I know, by allowing people to cast a cell to `List<Transform>` and then using the add member of that, instead of the one shadowing the `Add()` method inherited from list, which also does some debug asserts.
This way, I allow other code to do more with the cell, maybe even something they are not supposed to do.

I, personally, do not really care what people say. 
I'm going to use whatever feels OK to me.
Implementing an interface by writing out forwarding methods to a member list does not feel good.
At the same time, I have not yet fully developed my style of coding in C#, and I do not personally agree with some of the suggestions people make.
Perhaps when I grow professionally, I will understand more.

Also, a quick and simple test indicated that inheriting from `List` actually makes the code about 1.5 times faster than keeping the list a member field.

To be noted though, that static tiles are not even considered entities and are therefore not stored in the grid. 
The same applies to particle effects, which have no inflence on game mechanics.
The model is only responsible for things that have to do with game logic.


### 4.1.2. Components having to do with position and movement

Obviously, being able to occupy a certain position in the world and being able to change one's position at runtime are essential for the game. 

These abilities are modeled via the following specialized components: 
- `Transform`, providing a *position in the world*,
- `Displaceable`, providing the ability *to change one's position in the world*,
- `Moving`, providing the ability to *move voluntarily*,
- `Pushable`, providing the ability to *be moved involuntarily*.


#### 4.1.2.1. Transform

Entities that can be positioned in the world must have the [`Transform` component][11]. 
It contains information about the current position in the world, the current orientation (where the character is looking) and what layer the given entity is part of.
Every transform also stores a reference to the entity, so that one could get it by querying the grid.

Currently, there is a concept of being `directed`, which will be covered later.
It is modeled with an optional `tag` (a component without data), however, it could be beneficial to store it as a flag in the `Transform` component. 
This way, new flags could be introduced, like `sized`, an entity that takes up more that one cell at once.
Currently, any entity takes up just one position at a time.

The `Transform` is a component containing some helper methods for interacting with the grid.
This component is tightly coupled with the grid.
The methods are defined as instance methods of the transform simply for convenience sake.
They may as well have been defined as extension methods, or as methods on `Grid` (most of them have their analogues on the `Grid`).

The `Transform` currently works with the global grid, that is, it assumes that there is *just one world existing at once*.
This was done primarily for convenience: before the latest rework, the transforms used to have a reference to the world they are currently in.
However, I have changed this mostly because almost every function requires a reference to the world and so it was very annoying having to pass it around in the program.

When I add the possibility of multiple worlds existing at once, I will have to patch it somehow.
However, the change should not be too hard, given the fact that the logic code is single-threaded, which means I could change the global world instance when the world currently being processed changes.

If you look at the code closer, you might notice how some of the fields have been decorated with attributes.
This has to do with the code generator.
In short, the `Inject` attribute is used to generate a constructor and a copy constructor for this component, which would require to pass them a value for this field as a parameter.

You may also notice the methods `Grid.TriggerLeave()` and `Grid.TriggerEnter()` being called.
How these work exactly will be pointed out later.


#### 4.1.2.2. Displaceable

Changing one's position in a certain direction, either voluntarily or involuntarily, is conceptualized as *displacing*. 
Teleporting *to* a different position is *not* considered displacing.

This behavior allows displacement unless the place the entity is trying to move into is blocked.
Which layer is to be considered a blocking layer is stored as an injected field on this behavior and so may be changed at runtime for a particular entity if needed.

`Displaceable` is a *behavior*, which can be added to an entity to make it able to displace. [Source code][12].
In this class you can approximately see the way most behaviors are implemented.

[Here][13], we define a few chains (basically events).
The code generator picks up on them, initializing them in the autogenerated constructor as well as copying them in the autogenerated copy constructor.

If external code wanted to add handlers to these chains on an entity instance (or type, since it is implemented via a "subject" instance), they would use the `Export` attribute. 
Applying it would autogenerate the code to allocate a unique priority number to that handler function and, optionally, to generate a wrapper that may be used to make the process of getting the necessary chain from the entity and hooking up the handler easier. 

[Here][14] is an example of such attribute being applied to expose a handler function to the code generator.

The different chains defined in the `Displaceable` behavior are executed at different times in the process of displacing:
- `Check` is done before the movement, checking whether it should be done at all. 
  If the check chain has been passed through without stop, the action of displacing is considered successful, even though the entity may actually not move in the process. This is by design. 
- `BeforeRemove` is the second check to see if the displacement should be applied. 
  The difference between `BeforeRemove` and `Check` is that, even if `BeforeRemove` fails, that is, a handler stops the propagation of the context to other handlers, the move is to be considered successfull, even though it will not be executed.
  This difference is needed mainly for the acting system, explained later.
  But the key idea is that the `Check` chains are primarly used for checking *whether another action should be tried*.
  See, if the displacement fails at `Check`, e.g. *attacking will be tried*, but if it fails later at `BeforeRemove`, the action of moving will succeed and *no subsequent action will be tried*.
- `BeforeReset` is passed after the entity has been removed from the grid, but before it has been brought back (*reset*) in the grid. 
  As you may notice, it is passed directly, without propagation checking, so all handlers in that chain are guaranteed to be executed once `_BeforeResetChain.Pass(ctx);` is run.
- `After` is passed after the entity has been reset in the grid.

This many chains are needed to be able to alter the behavior of displacing in a very precise way.
For example, the particular function by [the link][14] makes it so that when the entity is about to displace, its orientation will be changed to that direction. 
But you may imagine there being crazy complex ideas implemented with the help of chains.
For example, [*sliding* uses the `After` chain][15] to stop sliding when the entity hits a wall or gets off a slippery surface.

I call the idea of applying some little detail to the algorithm of e.g. displacement, *retouching*, just like adding effects and details in Photoshop.


#### 4.1.2.3. Moving

`Moving` is the behavior responsible for voluntary displacement.

`Moving` behavior is a *directed activateable behavior*, which means it has an `Activate()` function that takes in a direction and returns a boolean, indicating whether the activation succeeded.
Such behaviors can be activated by the *action system*.
`Moving` uses the `Displaceable` behavior to actually do the displacement.

`Moving` is an example of a behavior making use of *autoactivation*.
*Autoactivation* is a feature provided by the code generator that lets it automatically generate the `Activate()` function, along with 2 chains: `Check` and `Do`. 
The purpose of `Check` chain is to *check* whether to *do* (traverse) the `Do` chain. 
The `Do` chain then will contain handlers that do whatever moving in this case is assumed to do.
Here we also see the use of the `DefaultPreset()` function that would set up these chains initially by applying the necessary handlers.

This is a common pattern in behaviors, but it's most useful for *prototyping*.
The `Check` and `Do` strategy works well for most behaviors in the beggining, but eventually you often realize you need more control, e.g. a chain like `Before` or `After`.
Then you would define all you need for your particular behavior, leaving autoactivation behind.

As an example, the `Displaceable` behavior started off as an autoactivated behavior.

[See the source code.][16]


#### 4.1.2.4. Pushable

`Pushable` is likewise an *autoactivated* behavior, but it's *not directed activateable*, because it cannot be done voluntarily.

`Pushable` is currently not a very mature piece of code, so I can't explain much here.

[See the source code.][17]



### 4.1.3. Block

The idea of an entity not being able to move into a cell is conceptualized as that cell being *blocked* by another entity.
Typically, this entity would be either from the *real* layer (enemies and the player) or from the *wall* layer.

As noted, blocking the movement is implemented in the `Displaceable`.
Blocks also have an impact on the *targeting system*, explained later.

#### 4.1.3.1. Directed entities

An entity being directed means they occupy just a part of the cell they are in. 
Such directed entities serving as directed blocks are often called *barriers*.

This idea has been inspired by such barrier blocks from **Cadence of Hyrule**.
[One of the tests][18] explains the idea of directed blocks with ASCII art more clearly than any text would.

This introduces more complexity in the process of detecting whether a particular cell is blocked.

Normally, for non-directed blocks, you just need to check one cell to know whether it is blocked or not.
If the cell contains an entity from your block layer, it is, if it does not, it isn't.
With directed blocks it's a bit more subtle.

If the entity from the block layer happens to be directed, you must check if it is on the correct side of the cell (which side it is on is indicated by its orientation).
The correct side of the cell being the side your character is going to enter it from.
If the potential blocking entity is on any other side of the cell, it should not block the movement.

But it's not all! You must also check whether the cell that the character starts their movement from contains a directional block on the side of the cell from which the character is going to leave it. 

I have implemented all of this as the [`HasBlock()` function][19] in the `Grid`. 
Since we need to know the side the character is going to leave from, it takes as input the direction alongside the actual coordinates of the cell of interest. 


### 4.1.4. Enter and Leave events

The grid also [defines 4 utility structures][20]:
- the `Enter` and `Leave` normal `TriggerGrids`;
- the `Enter` and `Leave` filtering `TriggerGrids`.

These have not been battle-tested yet, but they have been given a try in the implementation of the *sliding, bouncing, pinning* effects and in *projectiles*.

Basically, these grids lets you subscribe a handler function that will be executed upon any entity entering (or leaving) that cell.
The difference between normal `TriggerGrid` and the filtering one is that in the normal grid, your handler function *will be removed at the end of the current turn*, which essentially means your handler will persist only until all of the current entities have done their moves.
In contrast, handlers added to the filtering grid decide whether to keep or to remove themselves by returning true or false.
For an example, see e.g. [the `Leave` handler of bouncing][21].

Note that this API is not complete and might change in the future. 
I just explored an idea that seemed useful.

For example, [this handler][21] captures the entity as the first argument.
Capturing should ideally be replaced with a lookup based on id of the entity to allow the entities to be garbage collected immediately. 
However, doing that manually each time would be annoying.
Again, I may use the code generator for this purpose in the future.




## 4.2. Chains

In the previous sections the idea of *chain* has been touched on slighly. 
This section provides a more detailed description of what they are.


### 4.2.1. Responsibility chains

The *chains* in my code stem from the idea of a **responsibility chain**.

A responsibility chain is a list of handler functions operating on some data.
The data may be simple, like a number, but it may be more complex, in which case it is commonly called a *context*.

The meaning of calling these handlers is to either get some result or apply some effect.
Once one of the handlers has managed to apply its effect or has been able to calculate the output, the propagation stops, i.e. no further handler gets executed.

In case of chains *in my code*, the idea of *"managing to apply its effect"* is more general.
Whether to stop the propagation is figured out by checking the `Propagate` property of the object, which may either encapsulate a bool field or return true or false depending on other values of the context.
Also, a chain may be *passed without propagation checking*, so it is passed through regardless of the value of `Propagate`.

See [tests for chains][24].


### 4.2.2. Priority

It may be beneficial for the handlers to have priority and be sorted by that priority.
This would make fixing bugs related to the ordering of handlers easier, and give more flexibility to the chains.

Now the question is, what data structure to use for these?
We want a fast insertion, deletion and lookup, while being able to iterate through the collection in order of priority.

An idea would be to use a list, and sort that list before every iteration. 
This is a solution for sure, but the problem is that removing handlers is generally slow, and lookup involved scanning the entire list.

Another idea, which I have actually used, is to use linked lists and sort them before iterating, but, for first, sorting linked lists is messy and, for second, a second list had to be stored to keep the handlers added in between iterations, which would then be added into the main list.

Currently, I have settled on a balanced binary tree, represented by a `SortedSet` in C#. 
Removal, insertion and lookup are logarithmic, and the collection is kept sorted at all times.
I have also made it so that priorities are unique between the handlers in the program, so that any handler could be uniquely identified by its priority.


#### 4.2.2.1. How is the priority assigned?

The priority is assigned in the autogenerated init function, by using the registry to generate a priority number.

I have made a special class for this, the [priority assigner][25], which maps *priority ranks* to *priority numbers*.
[Priority ranks][26] are the following: lowest, low, medium, high and highest and are enumerated by an enum. I may add more ranks in the future, but it is sufficient for the current needs.

When you map a handler for export, you can specify a priority rank. 
The handler will get a unique priority number for that rank on initialization.


### 4.2.3. Types of chains

The introduction of priorities made all chains priority chains, which is an excessive complication in some cases.
So I have added the `LinearChain`, which is a chain, but without priorities, individual elements from which should not be removed, as it is modeled with a `List`.
I have also defined a `SelfFilteringChain`, which uses a double buffer (double list) to filter itself on traversal by inserting the elements that should be kept in the secondary buffer, and then swapping the buffers after the traversal.
We have already seen an instance of them being used in code: the `TriggerGrids`.

See [implementation of the `DoubleList`][22].
See [implementation of the different types of chains][23].


## 4.3. Entities and Components

Entities are objects that **affect the game logic**.
Examples of entities: *player*, *enemy*, *environmental objects*, *traps*, *special floor tiles*.

Things that don't affect the game logic, like *particles* or *simple floor tiles*, are *not* considered entities. 
These things *are not managed by the model*. 


### 4.3.1. Structure of Entities

An entity is just an object with an id and a dictionary of components.
So it would be fair to call entities simply *containers for components*.

Aditionally, I have entity instances store their *type id*, in order to simplify the interaction with the view.
This type id is also used in the item system.

[See the source code][27].

As you can see, the `Entity` class is `sealed`, which means it cannot be subclassed.
As has been discussed in the [system overview](#324-ecs-entity-component-system), the only mechanism for achieving different properties and behavior of entities is *component usage*.
Thanks to this, an entities' behavior or properties can be augmented by applying new components or by removing already existing ones.


### 4.3.2. What do components need to function?

Every component has 2 types of fields:
1. *Injected fields*. 
The values for these are passed through the constructor, set, and, most of the time, never changed.
Copying the initial form of a component would mean copying all of the injected fields' values over.
For example, the layer of the entity is an injected field on the `Transform` component.
2. *Other fields*. 
These fields are needed to capture the *runtime state* of a component. 
For example, flags on the `Acting` behavior, indicating whether the entity has acted this turn;
current position and orientation on the `Transform` component.

So, as has been established, in order to function properly, components must be given values for all their injected fields on component instantiation.

Behaviors provide one more type of field, namely, *chains*.
Chains essentially represent the mechanism used to achieve *polymorphism*.

The second important point is that behaviors may change an entities' behavior in some way.
This implies adding handlers to chains of their own or to the chains of other behaviors, already on the entity.

For example, the `Acting` component needs to reset its flags at the end of turn.
To achieve this, it adds a *reset handler* to the do chain of the `Ticking` behavior.
So, handlers may be added by behaviors to the chains of any behavior present on the entity.

The third thing is the *retouchers*. 
Retouchers are handlers that are added to specific chains of a specific behavior separately.
They have already been mentioned when overviewing the system.

These three things, namely, instantiation and the addition of behaviors, initializing behavior handlers and retouching, define the way entity types are constructed.  


### 4.3.3. Entity types

"Types" in this case do not mean "subclasses", because, as has been mentioned, components are used instead of inheritance.
Specific entity types are implemented via other means.

#### 4.3.3.1. The 3-step procedure

So, first let's understand in what way types could be created. The possibilities:
1. Run functions on entities that would add components, retouchers and initialize them in the correct ways.
2. Create some intermediate representation of the types and then instantiate new entities using that. This has failed for me since with this you basically have to create two copies of your logic: one for the actual entity and one for the "factory". With this, you get lots of maintenance issues.
3. A compromise between the two methods: have a factory, that would augment an entity and on instantiation just create copies of that entity. That is, we'll have functions that would set up the factory, adding the appropriate components and hooking up handlers via a respective `Preset()` function. 
This is what I opted for in the current implementation, because it is the simplest of all 3.

If we take into account the aforementioned things needed for components to be initialized correctly, we arrive at the following 3-step intialization procedure:
1. Add all components / behaviors.
2. Run their init functions (possibly more than one init function for a given behavior will be available, since these would be used instead of subclassing to achieve poymorphism).
3. Add more handlers (retouch).

So my idea was to define entity types as static classes with 3 static functions, one function for each step, which would augment the subject of the entity factory in order to initially construct the entity of a given type.

Here is [an example of such a static class][28]. 
This example also illustrates how a sort of type inheritance is achieved: just call these 3 functions of the type you want to inherit at the corresponding steps, before calling your own ones.

Here is an example of the syntax of inheritance. 

```C#
[EntityType(Abstract = true)]
public static class BaseType
{
    public static void AddComponents(Entity subject) {/*something*/}
    public static void InitComponents(Entity subject) {/*something*/}
    public static void Retouch(Entity subject) {/*something*/}
}

[EntityType(Abstract = false)]
public static class DerivedType
{
    public static EntityFactory Factory;

    public static void AddComponents(Entity subject) { 
        Base.AddComponents(subject); 
        /*something else*/ 
    }
    public static void InitComponents(Entity subject) {
        Base.InitComponents(subject); 
        /*something else*/
    }
    public static void Retouch(Entity subject) {
        Base.Retouch(subject); 
        /*something else*/
    }
}
```

#### 4.3.3.2. Problems

These is a couple of problems with this approach:
1. It involves some annoying boilerplate. 
Calling the function of the base type at *each* of steps, providing the signatures for the three static functions correctly, defining a static field of the `EntityFactory` type are the annoying things.
2. For the same reason, it is error prone. 
It is easy to forget to call the init function of one of the behaviors and there is no clear indication of that.

However, I do not worry about these problems, since I plan to eventually be able to *generate this code* from json files with the descriptions of types.
These json files will ideally be modified via a graphical editor or with Intellisense available. 
By Intellisense I mean e.g. suggesting appropriate values for the injected fields.
These values will be gotten by scanning the source code, looking for types or fields marked with corresponding attributes.

For example, the `Transform` component has an injected field of type `Layer`, which can obviously only have values from the `Layer` enum. 
So Intellisense could suggest those.

As another example, consider the `SlotComponent`. 
It needs an injected value of type `Slot`. 
`Slot` is not an enum. 
Although being a known type, the suggestions would have to be instances of that type.
We say that such instances are stored as static fields and are marked with the `[Slot]` attribute.
This way, the code analyzer could get hold of them and suggest them via Intellisense.

However, **a lot** more work has to be done, in order to get this working, so, for now, I decided to keep it simple and define the static classes manually. 
Sure, it is error-prone, but this way I would at least be able to build a working prototype in time.


### 4.3.4. Component copying

By copying components I mean copying the *chains* and the *injected fields*, that is, those parts of the component that are related to the type of the entity, while disregarding the values that would change at runtime.

#### 4.3.4.1. Why even copy components?

Well, this is essential for intializing entites.
As has been mentioned, in order to initialize an entity, the corresponding factory has to clone a stored "subject" entity instance.

Why not run the same set of functions on a fresh entity every time an entity of that type is to be instantiated instead of creating a whole "subject" instance?
The least I can think of that makes this a bad idea is the fact that doing this would negate the possibility of optimizing the chains to be *lazily* copied onto the new instance, having to be reconstructed entirely every time a new instance is needed. 

#### 4.3.4.2. Implementation

In order to copy any object one has a couple of options, some of which have already been mentioned:
1. Copy via reflection (kind of like automatic serialization);
2. Copy via code generation (providing default copy strategy for most components);
3. Copy manually.

Since all of the components are statically known in advance, there is no need for copying via reflection.

My code extensively uses copying via code generation, providing autogenerated copy constructors and copy functions, which, in turn, make use of these constructors.
More on code generation later.

Manual copies are sometimes prefered over automatic code generation, because, for some components, the strategy of creating a copy could be too complex.
So, the code generator will not provide a copy contructor, if it finds one already.

Ok, now let's understand what is actually going to be copied each time:
1. Values of injected fields. 
They are copied directly (by reference, if it is a reference type, or by making a shallow copy, if it's a struct).
2. Chains are always copied. 
Since I allow no closures for handlers, that is, the functions are not allowed to capture e.g. components,the task of copying them is trivial, namely, just copy the underlying data structure. 
It may also be enhanced in the future to an immutable sorted set, so that it is only copied when a change to the handlers of the new object is made.

The fact that the values of the runtime fields do not need to be copied leads to another interesting idea.
Why not construct a sort of *type representation* of components, that is, cut down versions of components, with just the injected fields and the chains.
This is actually a pretty good idea, although the only benefit one would get from this is that the entity factories would take a little bit more space in memory (the components wouldn't have the runtime fields present).
I'm not doing it because it would be hard to implement and it would take a lot of time, with minimal benefit.


### 4.3.5. Entity factory

Entity factories, as has been mentioned, contain a "subject" instance and their purpose it to create copies of this instance on demand. 
See [the implementation][29].

Since factories can be queried by their id (having a factory id it is possible to get the factory with that id), they must be assigned such id's and stored in the registry.
I will present some more theory on the registry and identifiers later.


### 4.3.6. Entity wrappers

Another interesting unimplemented hypothetical idea is to create wrappers around specific entity types.

Currently, the code generator creates extension methods for the `Entity` class for retrieving a specific component from an entity.
So, having any entity, even if it doesn't have the component `X`, you can do `entity.GetX()` or `entity.TryGetX()`.
This is bad when you expect an entity of a certain entity type, because all of the irrelevant methods, that is, methods that retrieve components that would never exist on that entity, would create clutter among the relevant methods.
This makes exploring the API via Intellisense considerably harder and is error prone.

So, consider an entity of type `A` that has the `X` component. 
Other component, that the entity of type `A` is not going to have, are `Y` and `Z`.
If we define a wrapper like this:

```c#
public readonly struct A_EntityWrapper
{
    public readonly Entity entity;

    public A_EntityWrapper(Entity entity) => this.entity = entity;

    public X GetX() => entity.GetX();
}

public void HypotheticalUsage()
{
   var entity = A_EntityType.Factory.Instantiate();

   // probably done automatically by the factory, when returing the entity
   var wrapped = new A_EntityWrapper(entity);

   wrapped.GetX(); // works
   // wrapped.GetY(); // does not work
   wrapped.entity.GetY(); // works if you know for sure it has Y 
}
```

The methods `GetY()` and `GetZ()` will not clutter the view, when we know the entity is of the entity type `A`. 
If we for some reason decided that we want to get the `Y` from the entity, we can just do `wrapped.entity.GetY();`, or even access any other extension methods that were defined for entity.

So it would be a *soft* wrapper, rather than a hard one, like when inheriting a type.

Once we have a way of storing an intermediate representation of the entity type, that is, which components will be present on it after the entity factory has been instantiated, the task of generating these wrapper classes becomes relatively trivial.

However, this intermediate representation is, too, a hypothetical idea at this point.
It requires just too much work to be done in time. 
However, having such representation will be essential for metacompiling json into `EntityType` static classes in C#, as well as for this idea.
So, this is definitely a problem worth solving eventually.


### 4.3.7. Loading entity types from JSON at runtime

As has been mentioned, defining types with JSON files has not been implemented yet, but it is a planned feature.

The code generator is going to metacompile these JSON files with descriptions of entity types into actual C# static classes, which would then produce functional entity factories when run.
But it should also be possible to load entity types directly from JSON at runtime, immediately converting it into a functional entity factory.

In order to not redefine the same logic both in the runtime entity factory generator and in the metacompiler, a shared piece of logic can be used that would parse JSON files and generate an intermediate representation of the entity types. 
Then, this intermediate representation will either be used directly to generate a factory at runtime, or to generate static classes in the code generator.

Runtime entity types can prove useful in prototyping new types while in game.


## 4.4. Acting and the Game Loop




## 4.5. Targeting?

## 4.6. Items?

## 4.7. Pools and Loot tables?

## 4.8. World generation

## 4.9. Code generation


# 5. References

[1]: https://github.com/AntonC9018/Dungeon-Hopper "Dungeon-Hopper github page"
[2]: https://antonc9018.github.io/Dungeon-Hopper-Docs/ "Dungeon-Hopper documentation"
[3]: https://github.com/AntonC9018/hopper.cs "hopper.cs github page"
[4]: https://github.com/AntonC9018/hopper-unity "Hopper: Unity demo github page"
[5]: https://github.com/AntonC9018/hopper-godot "Hopper: Godot demo github page"
[6]: <citation_needed> "Colleague's work"
[7]: https://github.com/AntonC9018/hopper.cs/blob/5b3156f38a03867272357085813409e9076cfc6d/Core/World/Grid/Grid.cs#L30 "GridManager's constructor"
[8]: https://github.com/AntonC9018/Dungeon-Hopper/blob/master/world/cell.lua#L19 "The former Cell class in lua"
[9]: https://github.com/AntonC9018/hopper.cs/blob/5b3156f38a03867272357085813409e9076cfc6d/Core/World/Grid/Cell.cs#L8 "Cell's current implementation"
[10]: https://stackoverflow.com/questions/21692193/why-not-inherit-from-listt "Inheriting from list in C#"
[11]: https://github.com/AntonC9018/hopper.cs/blob/5b3156f38a03867272357085813409e9076cfc6d/Core/World/Grid/TransformComponent.cs#L16 "Transform"
[12]: https://github.com/AntonC9018/hopper.cs/blob/25612ec4438f39f8b590c3a7426c5f0b6a8dea78/Core/Components/Basic/Displaceable.cs "Displaceable"
[13]: https://github.com/AntonC9018/hopper.cs/blob/25612ec4438f39f8b590c3a7426c5f0b6a8dea78/Core/Components/Basic/Displaceable.cs#L59 "Displaceable: chain declarations"
[14]: https://github.com/AntonC9018/hopper.cs/blob/0bcc623cb17d56f765b402860cd0e62e31885ad2/Core/Retouchers/Reorient.cs#L12 "Export attribute example"
[15]: https://github.com/AntonC9018/hopper.cs/blob/0bcc623cb17d56f765b402860cd0e62e31885ad2/TestContent/Modifiers/Sliding/SlidingEntityModifier.cs#L58 "Sliding example"
[16]: https://github.com/AntonC9018/hopper.cs/blob/0bcc623cb17d56f765b402860cd0e62e31885ad2/Core/Components/Basic/Moving.cs "Moving"
[17]: https://github.com/AntonC9018/hopper.cs/blob/0bcc623cb17d56f765b402860cd0e62e31885ad2/Core/Components/Basic/Pushable.cs "Pushable"
[18]: https://github.com/AntonC9018/hopper.cs/blob/25612ec4438f39f8b590c3a7426c5f0b6a8dea78/.Tests/Core_Tests/GridTests.cs#L169-L195 "ASCII art directed block"
[19]: https://github.com/AntonC9018/hopper.cs/blob/25612ec4438f39f8b590c3a7426c5f0b6a8dea78/Core/World/Grid/Grid.cs#L189 "Grid.HasBlock()"
[20]: https://github.com/AntonC9018/hopper.cs/blob/408ae5fb9ec73fa3426648442d122c57f623a6ef/Core/World/Grid/Grid.cs#L16-L19 "Trigger Grids"
[21]: https://github.com/AntonC9018/hopper.cs/blob/408ae5fb9ec73fa3426648442d122c57f623a6ef/TestContent/Mechanics/Bouncing/Bouncing.cs#L52 "Example of a filtering handler"
[22]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/Utils/DoubleList.cs "DoubleList"
[23]: https://github.com/AntonC9018/hopper.cs/tree/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/Utils/Chains "Chains"
[24]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/.Tests/Core_Tests/Chain.cs "Chain Tests"
[25]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/Core/Registry/PriorityAssigner.cs "Priority assigner"
[26]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/Shared/PriorityRank.cs "Priority Ranks"
[27]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/Core/Entity/Entity.cs "Entity class"
[28]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/TestContent/EntityTypes/Skeleton.cs "Skeleton entity type example"
[29]: https://github.com/AntonC9018/hopper.cs/blob/86ca8afdfc40c3de04548f9d66e4738d8b86f9c6/Core/Entity/EntityFactory.cs "EntityFactory implementation"