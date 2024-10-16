# By @itzAsuraa 
#Distribute and edit it as your wish but please don't remove credit
#By stealing Credit of Developer you will not become pro so try to give full credit to Developer


from pyrogram import Client, filters
import requests
from ERAVIBES import app

# Store user state to track if they are awaiting a query for the draw command
user_states = {}

# Define the handler for /draw Command.
@app.on_message(filters.command("draw"))
async def ask_for_query(client, message):
    # Check if a query is provided directly with the /draw command
    if len(message.command) == 1:  # If no query is provided
        # Set the user state to 'awaiting query'
        user_states[message.from_user.id] = 'awaiting_query'
        await message.reply("**Please provide a query to generate an image.**")
    else:
        # If the query is provided, process it directly
        query = " ".join(message.command[1:])
        await generate_image(client, message, query)


# Function to generate image based on the query
async def generate_image(client, message, query):
    # Make a request to the text2img API
    url = f"https://text2img.codesearch.workers.dev/prompt={query}"
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        image_url = data.get("image")
        if image_url:
            # Send the image with a caption mentioning the user
            caption = f"**Image generated by {message.from_user.mention}**"
            await message.reply_photo(photo=image_url, caption=caption)
        else:
            await message.reply("**Sorry, I couldn't generate an image for your query.**")
    else:
        await message.reply("**Error in generating image. Please try again later.**")