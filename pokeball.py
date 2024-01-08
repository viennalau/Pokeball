import time
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
current = time.time()
servo_opened = False

class RGB_LED():
    def __init__(self, GPIO_red, GPIO_green, GPIO_blue):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_red, GPIO.OUT)
        GPIO.setup(GPIO_green, GPIO.OUT)
        GPIO.setup(GPIO_blue, GPIO.OUT)
        self.red = GPIO.PWM(GPIO_red, 75)
        self.green = GPIO.PWM(GPIO_green, 75)
        self.blue = GPIO.PWM(GPIO_blue, 75)
        self.GPIO_red = GPIO_red
        self.GPIO_green = GPIO_green
        self.GPIO_blue = GPIO_blue
        self.red.start(0)
        self.green.start(0)
        self.blue.start(0)

    def turn_off(self):
        self.red.ChangeDutyCycle(0)
        self.green.ChangeDutyCycle(0)
        self.blue.ChangeDutyCycle(0)
    
    def turn_on(self):
        self.red.ChangeDutyCycle(100)
        self.green.ChangeDutyCycle(100)
        self.blue.ChangeDutyCycle(100)

    def set_red(self):
        self.red.ChangeDutyCycle(100)
        self.green.ChangeDutyCycle(0)
        self.blue.ChangeDutyCycle(0)

    def set_green(self):
         self.red.ChangeDutyCycle(0)
         self.green.ChangeDutyCycle(100)
         self.blue.ChangeDutyCycle(0)

class Servo():
    def __init__(self, GPIO_pin):
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(GPIO_pin, GPIO.OUT)
       self.pin = GPIO_pin
       self.servo = GPIO.PWM(4, 50)
       self.servo.start(0)
    
    def open(self):
        for i in range(0,5):
            self.servo.ChangeDutyCycle(i)

    def close(self):
        for i in range(5, 0, -1):
            self.servo.ChangeDutyCycle(i)

    def capture_success(self):
        global light1
        for i in range(10):
            light1.set_red()
            time.sleep(.2)
            light1.turn_off()
            time.sleep(.2)
        time.sleep(2)
        light1.set_green()
        time.sleep(3)
        light1.turn_off()
        # flash red rapidly, wait 2 seconds, solid green for 3 then turn off and stay closed
    
    def capture_fail(self):
        global light1
        for i in range(10):
            light1.set_red()
            time.sleep(.2)
            light1.turn_off()
            time.sleep(.2)
        time.sleep(2)
        light1.set_red()
        time.sleep(3)
        light1.turn_off()
        servoHinge.open()

light1 = RGB_LED(23,24,12)
servoHinge = Servo(4)

def button_response(channel):
    global current
    global servoHinge
    global servo_opened
    if time.time() - current > 0.5:
        if servo_opened:
            servoHinge.close()
            servo_opened = False
        else:
            servoHinge.open()
            servo_opened = True
        current = time.time()

GPIO.add_event_detect(26, GPIO.RISING, callback=button_response)

Pokemon = [
    "Pikachu", "Eevee", "Weedle", "Vaporeon", "Dialga", "Lobunny",
    "Jigglypuff", "Budew", "Quagsire", "Slurpuff", "Butterfree", "Dewgong",
    "Gallade", "Diglett", "Gyrados", "Raichu"
]
enemy_pokemon = " "
basic_pokemon = ["Charmander", "Squirtle", "Bulbasaur"]
starter_pokemon = ""
pokemon_inventory = []
fight_choice = ""

def pokemon_game():
    print("Oh look, you have come across", enemy_pokemon)
    fight_choice = input("Do you want to fight and capture it? Type Y/N: ")
    if fight_choice.upper() == "Y":
        print("Your starter Pokemon is", starter_pokemon)
        print("Let's fight")
        time.sleep(1)
        print("Ouch....")
        print("")
        time.sleep(1.5)
        print("Why did you choose", starter_pokemon, "....??")
        time.sleep(4)
        if random.randrange(0, 101) < 90:
            print("Huzzah! Your", starter_pokemon, "has won")
            servoHinge.close()
            if random.randrange(0, 101) < 99:
                servoHinge.capture_success()
                pokemon_inventory.append(enemy_pokemon)
                print("Congrats! You captured the", enemy_pokemon+"!")
            elif random.randrange(0, 101) > 99:
                servoHinge.capture_fail()
                servoHinge.open()
                print("Nooo! The",enemy_pokemon,"has escaped! :(")
        else:
            print("Yikes....")
            time.sleep(1.5)
            print("Your", starter_pokemon, "has lost, sorry.")

start = input("Welcome to the Pokeball. Type start to play: ")

while start == "start":
    print("Let's catch Pokemon, together!")
    returning = input("Are you a returning user? Y/N: ")
    if returning.upper() == "N":
        pokemon_inventory = []
        starter_pokemon = input("Enter the pokemon you want as your starter. No spaces. \n\
            You can choose from the following: " + str(basic_pokemon) + " : ").capitalize()
        enemy_pokemon = random.choice(Pokemon)
        print("Nice! You have chosen", starter_pokemon)
        pokemon_game()
    elif returning.upper() == "Y":
        print("Welcome back!")
        enemy_pokemon = random.choice(Pokemon)
        pokemon_game()
