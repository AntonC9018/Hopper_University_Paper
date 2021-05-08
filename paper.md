<!-- TOC -->

- [1. Abstract](#1-abstract)
- [2. Introduction](#2-introduction)
    - [2.1. Motivation](#21-motivation)
        - [2.1.1. My part in the job](#211-my-part-in-the-job)
    - [2.2. Game mechanics design](#22-game-mechanics-design)
    - [2.3. A short history of development](#23-a-short-history-of-development)
        - [2.3.1. Initial attempts](#231-initial-attempts)
        - [2.3.2. Example illustrating why if-statements do not cut it.](#232-example-illustrating-why-if-statements-do-not-cut-it)

<!-- /TOC -->

# 1. Abstract

Together with my colleague, we have created a Roguelike game, **Hopper**, based on the mechanics of *Crypt of the Necrodancer*.
In the first section I explain why I initiated this project and what development path I took. The next few sections are more technical. There, I motivate and illustrate with concrete examples my design decisions of the system, explain how the game works internally. I present how I managed to escape boilerplate and code duplication via code generation with *Roslyn* and *T4*. Finally, I show how the same code generation tools can be used for integrating the project with the *Godot* game engine.

# 2. Introduction

## 2.1. Motivation

The game idea is highly inspired by the game **Crypt of the Necrodancer** (henceforth refered to as simply *Necrodancer*), which I adore.

The project has always been planned to be an open-source game based on the same mechanics.

I never plan this project to make profit. It is designed for personal sake as well as, perhaps, for the community that is going to hopefully pick it up eventually.

The problems with Necrodancer that made me want to make a similar game are the following:
1. Modding is virtually impossible. Here, mods can only change visuals. No new mechanics or new types of mobs can be added into the game.
2. There is no Android support. I initially really wanted to play this on mobile.
3. The code is not publicly available.

So, my goals for the project became:
1. Make a game with mechanics like in Necrodancer.
2. Design a well-scalable system with many features and a slick API, to make developing mods easy.
3. Keep the code open to the public with a permissive license and invite modders when the API is mature enough.
4. Make it run on Android.

Along the way:
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
Writing a game is, likewise not a linear path.

Even though I knew the general idea I wanted to pursue with this project, as well as I had the base mechanics figured out, I did not know how to structure it correctly, in terms of code and system design.
So, I had to try many different things to reach the more exciting stuff I have got today.

### 2.3.1. Initial attempts

Initially, I tried to code the game in *Corona* game engine, in *Lua* programming language.
It allows exporting on mobile and desktop.

However, my understanding of how such games actually work was quite poor at the time.

Designing and implementing a simple game is entirely different from what I was going for.
If you are designing a game that could have thousands of different effects, mechanics and creatures and possibly expanded by mods, you cannot account for every item with a bunch of if-statements, you actually need more involved abstract systems making use of *some* kind of polymorphism.
I did not realize this before this project, but quickly understood it after this initial attempt.

I will expand on this more in a separate chapter

### 2.3.2. Example illustrating why if-statements do not cut it. 

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

