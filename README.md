## Written by Reactor02

## For NASCAR Racing 2003 Season

Unless you can't (like me) just use NRatings
NRatings is better (has a GUI) and can do more easier, but is a ClickOnce application and requires .NET, which is a pain to get working on Linux (I can't tell you about MacOS but ClickOnce and .NET are designed for exlusively Windows)

## How to Use

Make sure Python is installed (the program was made with Python 3.12)
Copy the .car files of the cars you want to modify into the imports folder along with the .lst (roster file located in the same directory as the .car files) containing all the car files you want to modify
After running the program, the modified .car files will be in exports where you can copy them back to their original folder (the original umodified files will still be in imports)
For y/n input, valid inputs are y, Y, n, and N
For the input that selects different rating types, you can select multiple types by entering multiple characters (1E2 selects ratings labeled. 1, E, and 2)
For all other inputs, it is just a number
**DISCLAIMER!!!** I did **NOT** add precautions to every input, so if you enter an invalid input, it may crash 

## How to Run

Open a terminal and navigate to the CLI-NR2003-Car-Ratings-Editor-main folder (you may need to extract it from its archive)
run `python3 main.py`
This 100% works on Linux, should work the same on MacOS, you might have to run `python main.py` or `py main.py` on Windows
Alternatively you could run it through something else like Visual Studio Code

## How to Navigate Directories in the Terminal

In case you aren't familar with the terminal or shell

To access the terminal on Windows, press Windows+R and type cmd in the run dialoge (I have never used PowerShell, but you probably don't need this if you do use it and it should be the same)
On Linux and MacOS the terminal is the same and should be in Start Menu or list of applications

To navigate directories type
`cd xyz`
and replace `xyz` with your directory or folder
examples:
`cd Downloads/CLI-NR2003-Car-Ratings-Editor-main`
or
`cd Downloads`
`cd CLI-NR2003-Car-Ratings-Editor-main`

To clear the terminal (for a cleaner and less crowded look)
`clear` (`cls`on Windows)

If you get lost
`ls` (`dir` on Windows)
lists your current directory and
`cd ..`
goes back a folder
