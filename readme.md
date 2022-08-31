<h1 align="center">Kagameshi</h1>


<h3>Kagameshi is a discord bot written in python that allows
you to crowdsource caption-image pairs on discord.<h3>
---
## How does it work

Kagameshi selects a random image from a specified folder
and uploads it to discord in a specified channel. Users
can then reply to the image in order to create a caption
image pair. Responses are stored in a postgresql database.

---
### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/sALTaccount/kagameshi.git
   ```
2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
   Install a [postgresql server](https://www.postgresql.org/download/) if you don't already have one


3. Put your data a folder named `dataset`

    Don't put your data directly into the folder, 
    put it inside of a "bucket" folder (eg `/dataset/0001/image.jpg`).
    Split larger datasets into multiple buckets.


4. Configure your `config.toml`

    Change `token` to your discord bot token

    Change `bucket` to your dataset bucket ID

    Change `channel` to the discord channel ID you want to use

    Change `host`, `database`, `user`, and `password` to your postgresql credentials

    All of the above are strings


---
## Usage

Reply to the image sent by the bot with your caption and it will be added to the database


![test](https://i.ibb.co/9Wjnyhs/image.png)

If the response is successfully recorded, the bot will react with check mark.
If the response was not recorded, the bot will react with an X.

You MUST reply to the image for the response to be recorded. This is to mitigate
messages that were not intended to be captions from being recorded as such.

Replies to images later than the last image sent will also not be recorded.

Once an image has been shown once, it will not be randomly selected again.
Upon bot restart, Kagameshi queries the postgresql server for all recorded captions,
and will not show any images in which a caption is already recorded.

Responses can be retrieved with an sql shell (such as pSql) with
```
SELECT * FROM kagameshi_responses;
```
---
## Postgresql
Kagameshi uses postgresql to store recorded captions.

Responses are stored in the following format and order:


| name       | type    | description                               |
|------------|---------|-------------------------------------------|
| image_name | VARCHAR | The name of the image the response is for |
| bucket     | VARCHAR | The bucket that the image is stored in    |
| user_id    | VARCHAR | The discord user ID of the submitter      |
| response   | VARCHAR | The caption written by the submitter      |