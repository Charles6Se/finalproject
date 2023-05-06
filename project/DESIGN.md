# Design Document

## Technical Decisions
### In this section, share and justify the technical decisions you made.
You don't need to respond to all questions, but you might find some of the following helpful:
* What design challenge(s) did you run into while completing your project? How did you choose to address them and why?
* Was there a feature in your project you could have implemented in multiple ways? Which way did you choose, and why?
* If you used a new technology, what did you learn about this new technology? Did this technology prove to be the right tool?

The biggest challenge was stopping a value error we were only getting sometimes. It turns out that the csv from 95.3 we were using has a few empty values for the the time which gave us the value error. We had to use a try except to get around this, so anytime it happened we would not take the entry. Also it took time to get the first period entry to be randomized. To do this we made a variable that was only true at first and then made false. The delete feauture I origionally implemented in JS, but I realized that that way it would be harder to get the History to update. I decided it would be easier to implement it in python.



## Ethical Decisions
### What motivated you to complete this project? What features did you want to create and why?
Thomas works for WHRB 95.3, so we decided to program a website that auto generates his program using the websites csv. We made it randomizedm, and he could choose any time he wants. One additional feature was that the period can't jump too much. Also we put a history feature in so you can see your program if you accidentally change the page.



### Who are the intended users of your project? What do they want, need, or value?
You should consider your project's users to be those who interact _directly_ with your project, as well as those who might interact with it _indirectly_, through others' use of your project.

The main users is anyone who wants to generate a classical music program, but particularly radio announcers. The indirect users would be any person who listens to the radio program. They could also be the musicians and publishers of the music. The announcers want a effective program, and the listeners want to hear good music. The musicians and publishers want to receive credit which the announcers should recognize before they play the music.


### How does your project's impact on users change as the project scales up?
You might choose one of the following questions to reflect on:
* How could one of your project's features be misused?
* Are there any types of users who might have difficulty using your project?
* If your project becomes widely adopted, are there social concerns you might anticipate?

At first we were planning on making a website that choose 1 piece and played it based on what the user inputted. As we countinued, we decided to change it to a radio program generated since we realized that this would give us actual utility. Visually impared people will not be able to use it since we have no audio component. I do not believe there are any concerns to it becoming widely adopted. 


