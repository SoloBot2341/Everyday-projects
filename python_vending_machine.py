import random
import pygame
import tkinter as tk
from tkinter import messagebox
import time
import threading
from plyer import notification
from pygame import mixer_music

pygame.mixer.init()

coins = {
    "pennies": 0.01,
    "nickels": 0.05,
    "dimes": 0.10,
    "quarters": 0.25,
    "singles": 1.00,
    "fives": 5.00,
    "tens": 10.00
} 

coins_available = {
    "pennies": random.randint(0,50),
    "nickels": random.randint(0,50),
    "dimes": random.randint(0,50),
    "quarters": random.randint(0,50),
    "singles": random.randint(0,20),
    "fives": random.randint(0,15),
    "tens": random.randint(0,10)
}


snacks = {
    "lays": [2.50,25],
    "cheetos": [2.75,25],
    "tea": [3.00,25],
    "dorritos": [3.00,25],
    "coffee": [4.00,25],
    "trident": [1.00,25],
    "Pepsi": [2.00,25],
    "haribo": [2.50,25],
    "apple slices":[2.25,25],
    "popcorn": [2.50,25],
    "takis": [2.25,25],
    "sprite": [3.00,25],
    "gummy bears": [3.00,25]

}

from plyer import notification

def get_more(snacks, coins_available):
    notification_sound = pygame.mixer.Sound("C:/Users/James/Downloads/cash-register-purchase-87313.mp3")
    # Get the current time in seconds since the epoch
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(elapsed_time)

        # Check if 15 minutes (or 900 seconds) have passed
        if elapsed_time >= 900:
            print("15 minutes have passed!")
            pygame.mixer.Sound.play(notification_sound)
            for snack, values in snacks.items():
                price = values[0]
                quantity = values[1]
                snacks[snack][1] += 5
            
            for coin, amount in coins_available.items():
                coins_available[coin] += random.randint(0,5)
            
            notification.notify(
                title='Vending Machine',
                message='Snacks and coins have been refilled!',
                timeout=10
            )
            start_time = time.time()  # Reset the start time


class VendingMachine(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.snack_var = tk.StringVar()
        self.payment_var = tk.StringVar()
        self.purchased_sound = pygame.mixer.Sound("C:/Users/James/Downloads/cash-register-purchase-87313.mp3")

        self.snack_quanity = []
        for snack, values in snacks.items():
            price = values[0]
            quantity = values[1]
            self.snack_quanity.append(quantity)

        tk.Label(self, text="Pick a snack: ").grid(row=0, column=0)
        tk.Entry(self, textvariable=self.snack_var, width=50).grid(row=0, column=1)

        tk.Label(self, text="Enter payment: ").grid(row=1, column=0)
        tk.Entry(self, textvariable=self.payment_var, width=50).grid(row=1, column=1)

        tk.Button(self, text="Pay", command=self.pay).grid(row=2, column=0, columnspan=2)

    def pay(self):
        snack = self.snack_var.get().lower()

        if snack not in snacks or snacks[snack][1] <= 0:
            messagebox.showinfo("Error", f"We don't have {snack} as a snack, please select again.")
            return

        try:
            payment = float(self.payment_var.get())
        except ValueError:
            messagebox.showinfo("Error", f"Invalid payment amount.")
            return

        price = snacks[snack][0]
        if payment < price:
            messagebox.showinfo("Error", f"The price of {snack} is ${price}. Please enter a valid amount.")
            return

        if payment > price:
            change = payment - price
            change_dict = self.shortest_amount_of_coins(coins, coins_available, change)
            if change_dict is None:
                messagebox.showinfo("Sorry", f"Oh no, we have no coins available. Here is your money back! ${payment}")
            else:
                pygame.mixer.Sound.play(self.purchased_sound)
                snacks[snack][1] -= 1
                change_info = ', '.join([f'{count} {coin}' for coin, count in change_dict.items() if count > 0])
                messagebox.showinfo("Enjoy", f"Here is your {snack}. Your change is ${change}. You recieved {change_info}. Enjoy! Thanks for using the vending machine.")
        else:
            pygame.mixer.Sound.play(self.purchased_sound)
            messagebox.showinfo("Enjoy", f"Here is your {snack}. Enjoy! Thanks for using the vending machine.")


    def shortest_amount_of_coins(self, coins, coins_available, return_amount):
        sorted_coins = sorted(coins.items(), key=lambda x: x[1], reverse=True)
        result = {}
        for coin, value in sorted_coins:
            count = 0
            while return_amount >= value and coins_available[coin] > 0:
                return_amount -= value
                coins_available[coin] -= 1
                count += 1
            result[coin] = count
            if return_amount == 0:
                break

        if return_amount != 0:
            print("Unable to make exact change with available coins")
            return None
        return result


if __name__ == "__main__":
    vending_machine = VendingMachine()

    # Start a separate thread to refill the snacks and coins every 15 minutes
    refill_thread = threading.Thread(target=get_more, args=(snacks, coins_available))
    refill_thread.start()
    vending_machine.mainloop()