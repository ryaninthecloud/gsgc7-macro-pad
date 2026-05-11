    
<center>
<h1>GSGC7 Macro Pad Project</h1>
</center>

### Introduction
Scrolling Vinted is a hobby for many and I am no exception. One such session resulted in me coming across a listing for the Glensound GSGC7 ISDN controller. This meant 0 to me, it was listed for something like £10 and I got a notification a few days later to say it was now £1. I bought it without really thinking about what I'd do with it.

Some brief research helped me to understand that the GSGC7 is used to dial and facilitate calls through another device (for example, the GSGC6) over ISDN. Principally used in broadcasting studios.

### Objective
Turn the GSGC7 into a macro-pad; I type a number into the board and have a Python script interpret that number to run a predefined automation.

### Before I read on, does it work?
![Rick and Morty, Jerry's boss saying yes](https://media3.giphy.com/media/v1.Y2lkPTZjMDliOTUyejM3N2xnZ3poM3YwcnY5M3N1MG0xM2JyYTVza2pycjIydHV3ajBtbyZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/l4FGAhdLqp6jea2Ag/200.gif)
<br><hr>



### The device

<img src="https://github.com/ryaninthecloud/gsgc7-macro-pad/blob/main/docs/MyGSGC7.png?raw=true" alt="drawing" width="200"/>

The device arrived and its faceplate immediately fell off, so after reattaching with some archivist's glue, I found that the device has a 9 pin (DB9) connector port on the back.

Opening it up, I was greeted by a **SAB 80C535** single chip microcontroller. My intention was to use the GSGC7 in as much of its factory state as possible, so I didn't immediately start poking around for an instruction set. However, this was really useful in understanding a bit more about the function of the device itself.

Beside the SAB chip, there isn't really much of note inside, the most interesting thing - and my main point of focus - is the DB9 port.

### Boy Do I Miss Documentation (BDIMD - be-dimmed)
Research online immediately revealed to me that I was looking at a device from the late 90's, produced by the company Glensound. The device, as I mentioned, was primarily used in broadcast studios to connect to ISDN lines - I am being deliberately vague here as I don't understand much about this and have mainly been obsessing over other aspects of the device.

I was not shocked to find that Googling "GSGC7 Glensound" yields a meagre 2 pages of results, but what was there was useful; the BDMIND refers largely to the paucity and less the veracity/utility of what does exist.

It would be remiss of me to say that I immediately and studiously consumed all of the documentation, painstakingly researching all of the elements I did not understand. It just is not true. I did the classic CTRL+F on the documents I could find and immediately started to realise there was a lot to this project that I didn't understand.

The main documents that I have based my understanding and approach on are the two linked below:

 1. https://www.glensound.co.uk/assets/library/528b37ba8ebe6-AP72-06.pdf
 2. https://glensound.co.uk/assets/library/528b31db12a39-gsgc6hb.pdf


> It is worth noting that I didn't ask any LLM about this project, for
> me, these projects are about learning and solving the puzzle.

Document 1 is interesting, it gives a handy user's guide to the GSGC7 but Document 2 is where the really interesting stuff is. Document 2 covers the interaction between the board and its intended controller, a GSGC6. The document contains in it information about the language [Heyes AT Modem commands] the devices use to communicate with each other as well as the installation (wiring) instructions.

### More volts please
Being impatient and not really getting the answers I wanted at the convenience I deemed suitable, I decided to JFTI (T=Try) and ordered an RS232 module to attach to my Arduino that would facilitate Serial communication between the board and my laptop.

As I said before, patience not being my thing, I had ignored much of the documentation at this point and was just playing around. I was disappointed to find that hooking up a 3.3v-5v RS232 module to my Arduino and then plugging in the GSGC7 yielded nothing - the board would not power on.

Sat in a waiting room, I revisited Document 2 and spotted a very clear wiring guide under 'Installation Guide'. This diagram showed that the board was expecting 12v, not the measly 5v I was offering up.

A quick trip to the PiHut and I ordered a voltage step-up regulator that could turn 5v into 12v.

My wiring got slightly more complicated than I had originally intended or hoped, but nonetheless, as displayed below, the GSGC7 lives under this carefully constructed ecosystem of connectivity.

![A complicated wiring diagram](https://github.com/ryaninthecloud/gsgc7-macro-pad/blob/main/docs/GSGC7-wiring.png?raw=true)

### It lives!
After carefully stringing together my cache of embedded components, the device breathed. I was able to confirm its method of communication was - as documented - outputting a series of (Heyes) AT commands.

### I can write some software now...

The Approach:
1) Arduino sits between the GSGC7 and my laptop
2) The Arduino receives raw AT commands over Serial (through the RS232 module) and then broadcasts them to the PC over the Arduino <-> PC serial connection
3) A Python script runs as a background service and interprets the dialled commands from the GSGC7, it then looks up the dialled number and performs the automation defined against it
4) The Python script also sends responses to the GSGC7 providing the user (me) with some feedback on whether the automation was a success or not

### What does what?


