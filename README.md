# ScratchText
![ScratchText](static/title.png)

A text-based interface for Scratch programming

## About

This is a work in progress for HGSE's T217 Spring 2020.

↳ Forked to continue development for community -- adding more functionality and block coverage

## Currently implemented blocks:

### Motion
- `move(steps)` : Moves sprite in its current direction
- `turn(degrees)` : Turns the sprite (clockwise)
- `goto(x, y)` : Moves sprite to specified location
- `glide(secs, x, y)` : Glides sprite to specified location over a certain amount of time
- `setx(x)` : Sets the x value of sprite to a certain value
- `sety(y)` : Sets the y value of sprite to a certain value
- `edge_bounce()` : "Bounces" sprite, changing its angle if it's touching a wall

### Looks
- `think(text)` : Makes sprite think specified text
- `say(text)` : Makes sprite say specified text
- `show()` : Makes sprite show
- `hide()` : Makes sprite hide

### Events
- `when_flag_clicked() { }` : Hat block, event that triggers when code starts
- `when_space_pressed() { }` : Hat block, event that triggers when space key pressed
- `when_clicked() { }` : Hat block, event that triggers when the sprite is clicked

### Control
- `forever() { }` : Repeat following code indefinitely
- `repeat(iteration) { }` : Repeat following code specified amount of time
- `wait(time)` : Wait specified time (in seconds)

### Operators
- `value + value` : Adds two values together
- `value - value` : Subtracts one value from another
- `value / value` : Divides one value by another
- `value * value` : Multiplies two values by each other
- `value % value` : Applies a modulo function to one value by another

#### Expressions
Works with operators, ex.: 
- `$forb + 12`
- `13 / 15`

### Variables
- `$variable = value`: Set a variable to a value
- `$variable`: References a variable's value

### Pen Blocks
- `penUp()`: Makes sprite put its "pen" into the "up" position
- `penDown()`: Makes sprite put its "pen" into the "down" position
- `penClear()`: Makes the sprite clear all current drawings on screen

### Comments
Semi-added, currently editor just ignores them<br/>
Single line comments and multi line comments are currently written the same -- Ex.:<br/>
- `/# This is a single-line comment #/`
-
- `/# This is a`
- `multi-line comment #/`