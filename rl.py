'''
Title: 2048 Hackathon Project using Reinforcement Learning
Author: Jason Ho, Jeremy Chen, Steven Cheung, Hwai-Liang Tung
Date: January 26th - 27th 2019
'''

# Imports from other files in repo
from 2048 import Board

# Imports from simple_rl library
from simple_rl.mdp.MDPClass import MDP
from simple_rl.mdp.StateClass import State
from simple_rl.run_experiments import run_agents_on_mdp
from simple_rl.agents import QLearningAgent, RandomAgent, RMaxAgent


class TFEState(State):
    '''
    TFEState is the definition of the state that is used for the reinforcement
    learning agent to know what state the board is in and what it should do 
    in order to advance itself in the next move.
    '''

    def __init__(self, board):
        '''
        init is just the initialiser method that takes in the board of the 
        2048 game.

        Parameters 
        ----------
        board : nparray
            the board represents the 2048 numpy array.
        '''
        State.__init__(self, data=board.flatten().tolist())
        self.board = board


class tfeMDP(MDP):
    '''
    tfeMDP is the specific implementation and modification of the MDP class
    that takes in all of the details needed for an rl agent to be able to play
    2048 by itself.

    Parameters
    ----------
    MDP : MDP
        Represents the Markov Desicion Process class created by the Brown
        University HRCI lab.
    '''
    # Definitions of all of the actions possible for the rl agent
    ACTIONS = ["Up", "Down", "Left", "Right"]

    def __init__(self, init_board=Board(False, 0), name="2048"):
        '''
        Initializer method that creates the MDP and assigns the other fields
        according to the 2048 game.
        '''
        self.step_cost = 0.0
        self.gamma = 0.99
        self.name = name
        self.current_state = TFEState((init_board.addTile()).addTile().board)

        # Initializing the actual Markov Decision Process:
        MDP.__init__(tfeMDP.ACTIONS, self._transition_func, self._reward_func,
                     init_state=TFEState(
                         (init_board.addTile()).addTile().board),
                     gamma=gamma)

    def get_parameters(self):
        '''
        get_parameters is a method that takes all of the parameters and fields
        defined beforehand and adds them into a dictionary that can be processed
        by the MDP funciton.
        '''
        param_dict = defaultdict(int)
        param_dict["current_state"] = self.current_state
        param_dict["step_cost"] = self.step_cost
        param_dict["gamma"] = self.gamma
        param_dict["name"] = self.name

    def _transition_func(self, state, action):
        '''
        transition_func is a method that essentially alows the rl agent to make
        a move, which creates the new state where the board is moved after the
        agent inputs a move.

        Parameters
        ----------
        state : state
            Represents the old state of the board state

        action : str
            Represents the move that the rl agent makes in order to go to the
            next state.

        Returns
        ----------
        state : state
            Represents the new state after the action beforehand is taken.
        '''
        b = Board(np.asarray(state.data).reshape((4, 4)))
        return State(self, b.moveAndUpdateBoard(action).board.flatten().tolist())

    def _reward_func(self, state, action):
        '''
        reward_func is a method that does a similar action as the transition
        function, but instead of finding what the next state is, it returns 
        the reward that a rl agent would get for doing good moves.

        TODO: This is not that optimized and can be fixed to make the rl agent
        a lot better.

        Parameters
        ----------
        state : state
            Represents the state of the board in 2048 at the current moment

        action : str
            Represents the move that the rl agent inputted in order to get
            to the next state. 
        '''
        b = Board(np.asarray(state.data).reshape((4, 4)))
        currentScore = sum(state.data)
        newScore = sum(b.moveAndUpdateBoard(action).board.flatten().tolist())
        return newScore - currentScore

    def __str__(self):
        '''
        str is a getter that just returns the name of the game that the
        rl agent is playing.
        '''
        return self.name

# ============================================================================ #

# Run Experiment


def main():
    # create mdp using own definition
    mdp = tfeMDP()

    # Three different agents to compare how each do against each other
    rand_agent = RandomAgent(actions=mdp.get_actions())
    rmax_agent = RMaxAgent(actions=mdp.get_actions())
    agent = QLearningAgent(actions=mdp.get_actions())

    # Function that actually runs everything and generates the appropriate
    # graphs and statistics defining how each agent did
    run_agents_on_mdp([agent, rmax_agent, rand_agent], mdp,
                      instances=200, episodes=100, steps=1000)


main()
