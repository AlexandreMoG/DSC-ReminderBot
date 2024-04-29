# DSC-ReminderBot
This project features a docker image to build a discord application that remind users after a choosen interval of time.

It was made for the Pursuit of Gilia discord server.  

## REQUIREMENTS

To run the application you'll need the following :
* **Docker** : This project requires docker to build the image
*  **docker-compose** : This project requires docker-compose to build the image and deploy the application
  
To run the standalone test and extra scripts, you'll need the following :
* **Python 3.11** and the following packages:  
  * **nextcord** : Nextcord is a modern, easy-to-use, feature-rich, and async-ready API wrapper for Discord, forked from discord.py.
  * **python-dotenv** : Python-dotenv reads key-value pairs from a .env file and can set them as environment variables.

## SETUP 

**Clone the Repository**:
```sh
git clone https://github.com/AlexandreMoG/ReminderBot-discord.git
cd ReminderBot-discord
```

**Modify the configuration file credentials.env with the GUILD_ID, the API_TOKEN and the ROLE_ID, check the CONFIGURATION section for more information.**

**Build the docker image and deploy the application**:
```sh
docker-compose up -d
```

## CONFIGURATION 

You do not have to modify the `docker-compose.yml`.  

You should modify the file named `credentials.env` containing :
```
GUILD_ID=<The ID of the server>
API_TOKEN=<Bot token>
ROLE_ID=<The ID of the group to ping>
```
