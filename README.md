This is “MyProgramMaker,” a musical program generator for the classical music branch of Harvard’s radio station, WHRB 95.3 FM.

Background: As a classical music announcer in WHRB, one has to make musical programs within certain guidelines; for example, the music program must last a specified amount of time (e.g. 3 hours total), and, when changing between pieces, one must change to a piece close in time period to the previous piece (i.e. I wouldn’t want to play a piece of music written in 2022 right after something written in the 500s; I want to “ease” my listener in). MyProgramMaker generates a program within such guidelines. Once the program is generated, you can make modifications to the generated program; if, for instance, the program gave you Beethoven’s 5th Symphony as one of its pieces, but you would prefer not to include it, you can remove it from your program.

How to get to the program: MyProgramMaker is a flask web application, so, in order to get to the website itself, one must first run flask in codespaces. To do so, first go into the finalproject folder as so: $ cd finalproject

Once you are in the finalproject folder, you then can run flask, as below: finalproject/ $ flask run

This command should print out the following: * Debug mode: off INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead. * Running on https://thomas-juhasz-opulent-space-eureka-r9vpgpv95pvhwp5-5000.preview.app.github.dev INFO: Press CTRL+C to quit INFO: * Restarting with stat

Use the link that the program generated, which should bring you to the website itself.

The program: Login Once you reach the website, you will be directed to the login page. If you have already made an account, proceed to enter your username and password, and click “Log In.” Otherwise, click on “Register” in the top right corner to make an account for yourself.

Register
    If you are entering the webpage for the first time, you will want to click on “Register” in the upper right hand corner.  You will be asked to enter a username, a password, and a confirmation of your password; for your password, the program will require you to enter at least 8 characters and at least one capital and one lowercase letter in order to accept your password. If you try to register while failing to meet these criteria or to fill out all of the text boxes, you will receive an error message.  Once you have correctly entered your username and password, the website will then direct you to the homepage.

“MyProgramMaker” homepage
    Upon reaching the homepage, which greets you with an image of several violins, you have several choices; you can either click on “Generate Program” to create a musical program, you can click on “History” to see the most recent two programs you have generated, or you can logout.
Generate Program
    When you click on “Generate Program,” you will be asked to enter the desired duration of your program, in total number of minutes.  The program will then generate a musical program for you within two minutes of the duration that you entered.  For instance, if you want to make a program that lasts 30 minutes, you might get back a musical program that is 31.2 minutes.  In addition to the duration, you will receive important information about the piece of music itself: the composer of the piece, the title of the piece, the performers, and the time period of the piece.  The time periods fall between 0 and 6, with 0 being before or during the time of the Middle Ages, and 6 being essentially present time.  The program ensures that consecutive pieces in the musical program will be within 2 time periods apart.  For instance, if my first piece is of period 3, it can be followed by a piece of period 1, 2, 3, 4, or 5, but not by those of periods 0 or 6.  Similarly, if I have a piece that is of period 1, it can be followed by a piece of period 1, 2, or 3, but not 4, 5, or 6.
    You will also see that there are columns labeled “Label,” “Format,” and “Number.”  “Label” refers to the company that released the recording (e.g. Sony, DG, RCA), “Format” refers to the medium in which the recording is played (e.g. CD, record/LP, or via a streaming service), and “Number” refers to the actual ID of the recording, since each piece of music is a real recording that was released.  These three columns are important since, as a radio announcer, I must know the specific recording to play (there are many different recordings of Beethoven 5, for instance, so it is important to know which recording to play).

History
    Upon clicking on “History,” you will be directed to the most recent programs that you have generated: the current program, and your program immediately before.  It displays the same information about each piece of the program as did the “Generate Program” page.

Log Out
    Once you are done using the program, you can click on “Log Out,” which will log you out and bring you back to the “Log In” page.
I hope you enjoy our CS50 final project, MyProgramMaker!# finalproject
This is my CS50 final project. 
