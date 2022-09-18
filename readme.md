<h1 align="center">Kagameshi</h1>


<h3>Kagameshi is a discord bot written in python that allows
you to crowdsource caption-image pairs from Danbooru on discord.<h3>

## How does it work

Kagameshi downloads images from the danbooru front page and displays them on discord.
Replying to that message will add a caption-image pair to the database.

---
### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/sALTaccount/kagameshi.git
   ```

2. Configure your `config.toml`

    Change `token` to your discord bot token

---
## Usage

Reply to the image sent by the bot with your caption, and it will be added to the database


![img1](https://camo.githubusercontent.com/08af2a8a215e872d6af524483acafd1c63ba6316b1da73e6e0d4545f3aaf4b96/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313032303135373933333431393530333639362f313032303532393035383037343836393835302f756e6b6e6f776e2e706e67)
![img2](https://camo.githubusercontent.com/c2daa28333891e4fc4741819c9f423ef7b089b89d871183cf3700c3e62bb277c/68747470733a2f2f63646e2e646973636f72646170702e636f6d2f6174746163686d656e74732f313032303135373933333431393530333639362f313032303532393731303130383739303934342f756e6b6e6f776e2e706e67)

The bot will react with a check mark if your response is properly recorded.

## Responses
The responses are stored in a file called `responses.json`, created in the directory where the program was run.
In the JSON file, the key is the Danbooru post ID, and the value is the prompt that the user typed.