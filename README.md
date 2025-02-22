# The_Watcher
![alt text](The_Watcher.jpg)

## A cheeky little Letterboxd - Discord Bot
For some unknown reason Letterboxd hasn't allowed collaboration on lists! This little discord bot fixes that.
Made using [Discord.py](https://github.com/Rapptz/discord.py)

Letterboxd *please* give me API access

## Features
1. *Add Movie*  : Allows anyone in your discord to add a movie to your Letterboxd list.
2. *Delete Move* : For when someone adds a terrible pick.
3. *Get a Random Movie* : You can pick off your list, or add some extra lists y'all use and get a random value.

## Requirements
1. Python 3.11
2. ChromeDriver (boo) in your PATH with some type of adblocker (yay!) extension in the main folder.
3. venv with requirements.txt
4. Discord Dev Account
4. A .env in the main folder with the following:
    1. BOT_TOKEN = Generated from Discord Dev page
    2. LB_USERNAME = Your Letterboxed username
    5. LB_PASSWORD = Letterboxed pass
    6. DISC_ID = Your discord ID
    7. LB_LIST_NAME = Your Letterboxd list - Your Kinosphere!

## Running
Run "Bot_Soul.py" in your venv. Make sure to run:

`!sync`

At the start to add your commands to your discord.
