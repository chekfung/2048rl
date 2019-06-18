# 2048 Reinforcement Learning Project
##### Date: 06/18/19 (Initially created: 01/26/19)
##### Authors: Jason Ho, Jeremy Chen, Steven Cheung, Hwai-Liang Tung
------

## Project Overview
**Note**: This project was a collaboration between four people initially and then continued by Jason Ho in the middle of June of 2019.

The 2048 rl project initially began after a failed attempt at another project beforehand which meant that we had a late start to the hackathon. Rather thancontinue that project, our group elected to start a new project using reinforcement learning. One of the easier games to code in our opinions was 2048, meaning that we could focus on learning the simple_rl module that was created by the Brown University HRCI Robotics lab. It was small enough of a project that we were confident that we could get the basics of our code working within the small time frame that we had left.

### This project contains a few files:
 - 2048.py : This file contains the Board class which represents the entire 
                game as itself and all the methods required for the game to 
                work correctly.
                
- rl.py   : This file contains all of the framework including the tfeSTATE
                and tfeMDP class declarations such that the 2048 class is able 
                to work correctly. It basically bridges the disconnect between 
                the 2048 game and the reinforcement learning agent that is 
                capable of playing the game.
                
- TODO: Finish this part of the README


## How to Use

* Note: In order to be able to run the repository correctly, it requires the 
        simple_rl and pygame libraries to be downloaded.

- TODO: Finish the how to use part of the README 


 ## Bugs and Fixes
- tfeMDP reward function seems to be broken because it keeps trying the same
  moves, which promotes it to get a linear score overtime rather than make more 
  informed scores as it plays more games.

- TODO: Finish documenting all of the bugs and fixes that could be done


 ## Todo List
1. Fix implementation with the tfeMDP to make sure that it works correctly and
   check whether or not the reward function is broken.
        - It seems that since the reward is calculated at each move, it just
          tries moves that it realizes will give it similar scores, but we 
          want to try and make it such that the graph is exponential.

2. Implement the 2048 game in a text based way in the console such that we can 
   try and see whether or not the 2048 game is working correctly as intended.

3. Use pygame in order to make an implementation of the 2048 game that has a
   GUI. Afterwards, try and use this GUI in order to display the moves that the
   reinforcement learning agent makes in order to get a visual of exactly what
   is occuring at every step of the way.

4. Finish documentation and make sure that everything is working as intended.


 ##  Change Log
__*01/26/19: Version 1.0*__
- Hack @ Brown first day where the initial 2048 game was created and then 
      the architecture of rthe tfeMDP were initialized where we were able to get 
      basic functionality of the game and basic functionality of the MDP

__*01/27/19: Version 1.1*__
- Hack @ Brown second day where changed game to run underneath with numpy
      arrays, getting rid of most of the bad runtime code that was written 
      beforehand.
- tfeMDP fixed such that it actually produced graphs rather than a blank
      graph without any information on it.

__*01/28/19: Version 1.2*__
- Worked to fix the tfeMDP reward function because it seems as if the rl
      agent was performing only linearly better than the random agent in
      choosing the correct moves to maximize its score.
- To make sure that the game worked by itself, tried to implement a text 
      version of the game that could be played on the console.

__*06/18/19: Version 1.3*__
- Formally documented in PEP-8 and files separated such that it represents 
      a repository rather than one singular file. README was started
- Beginning to work on a pygame GUI for the 2048 game in order to get a 
      grasp of the front end of the game.