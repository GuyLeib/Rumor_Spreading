# Rumor_Spreading

This program is a GUI implemenation of Game of Life - Rumor spreading variation.
In this variation there is 100*100 grid which simulate a human population. 

The colored cells represent the humans, and the four colors represent 4 doubt levels:

S1 - believe every rumor they hear. (colored in purple)

S2 - will believe a rumor in a probability of 1/3. (colored in light-blue)

S3 - will believe a rumor in a probability of 2/3. (colored in green)

S4 - don't believe to any rumor. (colored in yellow)


# Using The Program:
1. Run the "rumor_spreading.py" file or just double click on the rumor_spreading.exe file.
2. A welcome screen will appear:
On the screen you can see the current game configuration, which you can either change using the change configuration button or start play with the current configurations.
<img width="400" alt="image" src="https://user-images.githubusercontent.com/92683819/235300137-98280aef-dc78-4511-99b1-b66a290882cc.png">
3. In order to start playing press the "Strat Game" button and the next screen will apear:
<img width="400" alt="image" src="https://user-images.githubusercontent.com/92683819/235300408-23b46b0c-951b-4eae-a74e-b0c26df0da19.png">

4.To start spreading the rumor you need to assign the first person who knows the rumor, this will be done using the start button. <img align = "center" img width="29" alt="image" src="https://user-images.githubusercontent.com/92683819/235300486-c4697dea-e735-45b0-91e6-bfd5fc0c6cd3.png">

The first spreader will be marked in black as follows: <img align = "center" img width="68" alt="image" src="https://user-images.githubusercontent.com/92683819/235300549-bb0a2ca8-ce83-4b12-aa09-f788e4586f5f.png">

 
Then, you can either spread the rumor one generation at a time using the Next Generation button <img align = "center" img width="71" alt="image" src="https://user-images.githubusercontent.com/92683819/235300581-ed52aa4b-4213-45eb-8cfe-189969360b31.png"> or you can skip 30 Generations forward using the 30 Generations Forward button <img align = "center" img width="102" alt="image" src="https://user-images.githubusercontent.com/92683819/235300637-2fd2387d-1f82-4fc8-9ce8-4d3dda6f9915.png">
As the rumor starts to spread, a section appears at the bottom of the board, showing the current generation,the number of people who have heard it and the corresponding percentage:
<img align = "center" img width="420" alt="image" src="https://user-images.githubusercontent.com/92683819/235434883-26962350-264c-43b8-a258-e5f74d145b2d.png">

All the cells  which heard rumor will be colored in black for the rest of the simulation.
# Changing Configuraion:
1. In order to change configuration run the program and press on "change configuraion" in the opening screen.
2. The next screen will appear:
<img width="299" alt="image" src="https://user-images.githubusercontent.com/92683819/235301148-ee623b1c-49a2-4927-8c70-13c1bf7ac8c2.png">

The "game strategy" parameter determines how the individuals with varying doubt levels are organized on the board.
For instance, in the "fast" configuration, the cells are arranged in such a way that those with a lot of neighbors are assigned to the s1 doubtness level.

3. The valid values for each parmeter is written in the parentheses. You can also change just some of the parameters and the rest of them will remain as the default values. After inserting the parametes you want to change press on "submit". 
4. In case that the inserted parmeters that are invalid a warning messegae will appear (after pressing on "submit") and the configuration will remain in the default parameters:  <img align = "center" width="206" alt="image" src="https://user-images.githubusercontent.com/92683819/235301298-d94d8b48-7fd5-43a2-afe4-9c2c9dc730e3.png">

# Additional Files:
1. "statistics.py"-The "statistics.py" file is designed to analyze and gain insights into the dynamics of rumor spreading.
This file contains several functions that can run simulations with different sets of parameters and plot various graphs to visualize the impact of each parameter on the rate of rumor spreading.
2. "data.csv"- During the different simulations, a "data.csv" file was created in order to facilitate the organization of data and the creation of various plots.  

