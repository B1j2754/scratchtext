<img src="static/title.png" alt="ScratchText" width="600">

A text-based interface for Scratch programming

# About

This is a work in progress for HGSE's T217 Spring 2020.

↳ Forked to continue development

# Currently implemented blocks:

### Motion
move(steps) - moves sprite in its current direction<br/>
turn(degrees) - turns the sprite (clockwise)<br/>
goto(x, y) - moves sprite to specified location<br/>
glide(secs, x, y) - glides sprite to specified location over a certain amount of time<br/>
setx(x) - sets the x value of sprite to a certain value<br/>
sety(y) - sets the y value of sprite to a certain value<br/>
edge_bounce() - "bounces" sprite, changing its angle if its touching a wall

### Looks
think(text) - makes sprite think specified text<br/>
say(text) - makes sprite say specified text<br/>
show() - makes sprite show<br/>
hide() - makes sprite hide<br/>

### Events
when_flag_clicked() {  - hat block, event that triggers when code starts

}<br/>
when_space_pressed() {  - hat block, event that triggers when space key pressed

}<br/>
when_clicked() {  - hat block, event that triggers when the sprite is clicked

}<br/>

### Control
forever() {  - repeat following code indefinitely

}<br/>
repeat(iteration) {  - repeat following code specified amount of times

}<br/>

wait(time) - wait specified time (in seconds)

### Variables
variable = value - set a variable to a value