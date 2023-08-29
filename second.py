import random
import tkinter as tk
import math




class DiceGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")


        self.size = 0

        self.new_state = 0
        self.new_score = 0

        self.current_state = 0
        self.current_score = 0




        self.player_score = 0  # Initialize player's score
        self.player_sum = 0  # Initialize player's sum of dice rolls

        self.house_score = 0   # Initialize house's score
        self.house_sum = 0  # Initialize player's sum of dice rolls


        self.score_label = tk.Label(self.root, text="Player's Score: 0")
        self.score_label.pack()

        self.score2_label = tk.Label(self.root, text="House's Score: 0")
        self.score2_label.pack()

        self.dice_label = tk.Label(self.root, text="Dice Rolls: ")
        self.dice_label.pack()

        self.wins = 0
        self.losses = 0
        self.ties = 0

        self.simulation_results = None


        self.stats_label = tk.Label(self.root, text="Wins: 0, Losses: 0, Ties: 0")
        self.stats_label.pack()  # Add the label to the GUI

        self.change_label = tk.Label(self.root, text="")  # Initialize the change label
        self.change_label.pack()  # Add the label to the GUI

         # Create a button to roll the dice
        self.roll_button = tk.Button(self.root, text="Play Round", command=self.play_round)
        self.roll_button.pack()

        self.change_button = None  # Initialize the button reference

        
        self.container_01 = []
        print("here is your List"+str(self.container_01))

        self.container_house = []  # Initialize container for house's rolls

        self.simulate_button = tk.Button(self.root, text="Simulate Rounds", command=lambda: self.simulate_rounds(100))
        self.simulate_button.pack()

         # Create a button to start simulated annealing
        self.simulate_annealing_button = tk.Button(self.root, text="Simulate Annealing", command=lambda: self.start_simulated_annealing(100))
        self.simulate_annealing_button.pack()


        self.initial_temperature = 1.0  # Initialize the initial temperature
        self.cooling_rate = 0.95  # Define the cooling rate
        self.min_temperature = 0.01  # Define the minimum temperature
        



    def roll_dice(self):
        print("You are Inside roll_dice")

        return [random.randint(1, 6) for _ in range(2)]
    
    
    def play_round(self):
            
            self.size = 5
       
            self.container_01 = self.roll_dice()
            self.update_dice_label()

            self.player_sum = sum(self.container_01)
            self.score_label.config(text=f"Player's Score: {self.player_sum}")


            self.container_house = self.roll_dice()  # House's rolls
            self.house_sum = sum(self.container_house)
            self.score2_label.config(text=f"House's Score: {self.house_sum}")

            
            if self.player_sum < self.size:  # Implement a basic strategy for Simulated Annealing
                print("Player's score is less than 5. Changing a die.")
                print(f"Before die change: {self.container_01}")
                self.change_label.config(text="Change a Die")
                if self.change_button is None:  # Check if the button doesn't already exist

                    self.change_button = tk.Button(self.root, text="Change a Die", command=self.change_die)
                    self.change_button.pack()
                    self.change_die()  # Automatically change a die

                    print(f"After die change: {self.container_01}")
   
            else:
                self.change_label.config(text="Keep Both")

            self.determine_winner()  # Determine the winner at the end of each round



    

     


    def keep_both(self):
        player_score = sum(self.container_01)  # Calculate the player score
        self.score_label.config(text=f"Player's Score: {player_score}")

        self.change_label.config(text="")

    
    def change_die(self):
        min_value = min(self.container_01)
        min_indices = [i for i, value in enumerate(self.container_01) if value == min_value]
        
        lowest_index = min_indices[0]  # Choose the first index with the minimum value
        new_roll = random.randint(1, 6)  # Generate a new random roll
        self.container_01[lowest_index] = new_roll
        self.update_dice_label()

        player_score = sum(self.container_01)  # Calculate the new player score
        self.score_label.config(text=f"Player's Score: {player_score}")

        self.change_label.config(text="")
    

    def update_dice_label(self):
        self.dice_label.config(text=f"Dice Rolls: {self.container_01}")

    def determine_winner(self):
        player_sum = sum(self.container_01)
        house_sum = sum(self.container_house)

        if player_sum > house_sum:
            self.change_label.config(text="Player wins!")
        elif player_sum < house_sum:
            self.change_label.config(text="House wins!")
        else:
            self.change_label.config(text="It's a tie!")

        self.roll_button.config(state=tk.DISABLED)  # Disab

    def simulate_rounds(self, num_rounds):
        self.wins = 0
        self.losses = 0
        self.ties = 0

        for _ in range(num_rounds):
            self.play_round()
            player_score = sum(self.container_01)
            house_score = sum(self.container_house)

            if player_score > house_score:
                self.wins += 1
            elif player_score < house_score:
                self.losses += 1
            else:
                self.ties += 1

        self.update_stats_label()

        # Store the results in the simulation_results variable
        self.simulation_results = {
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties
        }

        print(f"Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}")

        if self.change_button:
            self.change_button.config(state="disabled")  # Disable the button
            

      

    def update_stats_label(self):
        self.stats_label.config(text=f"Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}")

    def get_current_state(self):
        return self.size   


    def calculate_score_state(self):

        return self.wins
    
    def generate_neighboring_state(self, current_state):
    # Generate a new size value by slightly modifying the current size
        new_size = current_state + random.randint(-1, 1)  # You can adjust the range of change

        # Ensure the new size is within a valid range (e.g., between 2 and 10)
        new_size = max(2, min(10, new_size))

        return new_size

    def acceptance_probability(self, current_score, new_score, temperature):
        if new_score > current_score:
            return 1.0  # Accept the new state if it's better
        else:
            # Calculate the probability of accepting a worse state
            delta_score = new_score - current_score
            probability = math.exp(delta_score / temperature)
            return probability


    def start_simulated_annealing(self, num_rounds):


        if self.simulation_results is None:
            print("Please run the simulation rounds first.")
            
            self.change_label.config(text="Please run the 'Simulation Rounds' first.")
            return
            


        self.current_state = self.size
        self.current_score = self.calculate_score_state()

        temperature = self.initial_temperature

        while temperature > self.min_temperature:
            self.new_state = self.generate_neighboring_state(self.current_state)
            self.new_score = self.calculate_score_state()

            if self.new_score > self.current_score or random.random() < self.acceptance_probability(self.current_score, self.new_score, temperature):
                self.current_state = self.new_state
                self.current_score = self.new_score

            temperature *= self.cooling_rate

        print("Simulated Annealing Results:")
        print(f"Best State: {self.current_state}")
        print(f"Best Score: {self.current_score}")

 
if __name__ == "__main__":
    root = tk.Tk()
    game = DiceGame(root)
    root.mainloop()       
