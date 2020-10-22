import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
        Initialize game board.
        Each game board has
            - `piles`: a list of how many elements remain in each pile
            - `player`: 0 or 1 to indicate which player's turn
            - `winner`: None, 0, or 1 to indicate who the winner is
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Returns the Q-value for a combination of `state` and `action`.
        If no Q-value exists in `self.q`, returns 0.
        """
        for q_value in self.q:
            if q_value == (tuple(state),action): 
                return self.q[q_value]
        
        return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Updates the Q-value for a combination of `state` and `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.
        """

        # Calculate new Q-value
        new_q = old_q + self.alpha * (reward + future_rewards - old_q)

        # Add state, action and Q value to dictionary if they don't exist
        if (tuple(state),action) not in self.q:
            self.q.setdefault((tuple(state),action), new_q)
        
        # Update Q value for existing state/action pairs
        else:
            self.q[(tuple(state),action)] = new_q     

    def best_future_reward(self, state):
        """
        Given a `state`, considers all possible `(state, action)`
        pairs and returns the highest of their corresponding Q-values.

        If a `(state, action)` pair has no Q-value in `self.q` uses 0 as the Q-value.
        If there are no available actions in `state`, returns 0.
        """
        
        # Obtain a set of all possible actions for state
        possible_actions = Nim.available_actions(state) 

        # If no actions are available
        if len(possible_actions) == 0:
            return 0

        # Initiate maximum reward value
        best_reward = float('-inf') 

        # Update maximum reward value        
        for action in possible_actions:
            if (tuple(state), action) in self.q:
                best_reward = max(best_reward, self.q[tuple(state), action])
            else: 
                best_reward = max(best_reward, 0)

        return best_reward

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, returns an action `(i, j)` to take.

        If a greedy algorith is used (i.e., `epsilon` is `False`), 
        then returns the best action available for the `state`.

        If an epsilon-greedy algorith is used (i.e. `epsilon` is `True`), 
        then with probability `self.epsilon` choose a random available action,
        otherwise choose the best action available.
        """

        # Obtain a set of all possible actions for state
        possible_actions = Nim.available_actions(state) 

        # Create a set of best actions
        best_actions = set()
        best_reward = self.best_future_reward(state)

        for action in possible_actions:
            
            # If state/action pair has a Q-value, compares Q-value to the best reward for the state
            # to identify the best actions
            if (tuple(state), action) in self.q: 
                if self.q[tuple(state), action] == best_reward: 
                    best_actions.add(action)
            
            # If state/action pair does not have a Q-value, uses a Q-value of 0 
            # and, if the best reward for the state is also 0, assigns action to the set of best actions
            else: 
                if best_reward == 0:
                    best_actions.add(action)

        # Greedy algorithm
        if epsilon == False: 
            random_best_action = random.choice(list(best_actions))
            return random_best_action 
        
        # Epsilon-greedy algorithm 
        epsilon_actions = dict()
        epsilon_weight = self.epsilon/len(possible_actions)
        greedy_weight = (1-self.epsilon)/len(best_actions) 

        if epsilon == True: 
            for action in possible_actions:
                epsilon_actions.setdefault(action, epsilon_weight)
            for action in best_actions:
                epsilon_actions[action] += greedy_weight      
    
            population = list(epsilon_actions.keys())
            weights = list(epsilon_actions.values())
            random_epsilon_action = random.choices(population, weights)[0]

            return random_epsilon_action   
        
def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return
