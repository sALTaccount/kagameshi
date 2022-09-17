import traceback
import pybooru
import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from typing import Optional

import json_interface

embed_color = discord.Colour.from_rgb(215,195,134)
    

class DataCog(commands.Cog, name='Data', description='Used by volunteers to label data.'):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.dbclient = pybooru.Danbooru('danbooru', username='haru1367')
        self.default_tags = 'rating:general'
    
    def get_post(self, tags=None, id=None):
        if id is not None:
            post = self.dbclient.post_show(id)
        else:
            if tags is None:
                tags = self.default_tags
            else:
                tags = tags + ' ' + self.default_tags
            post = self.dbclient.post_list(tags=tags, limit=1)[0]
        return post
    
    async def post_searcher(ctx: discord.AutocompleteContext):
        return list(json_interface.get_responses(None).keys())

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (not self.bot.user.mentioned_in(message)) and (message.reference is None):
            return
        if not message.reference.cached_message.embeds:
            return

        post_id = int(message.reference.cached_message.embeds[0].footer.text)
        print(f'setting {post_id} to -- {message.content}')
        json_interface.insert_response(None, post_id, None, message.content)
        await message.add_reaction('✅')
    
    @commands.slash_command(name='fetch', description='Fetch a labeled image')
    @discord.option('post_id',
        int,
        description = 'Post ID to fetch the label for',
        autocomplete=post_searcher,
        required = True
    )
    async def fetch(self, ctx: discord.ApplicationCommand, post_id: int=None):
        try:
            if post_id is not None: assert isinstance(post_id, int)
            post = self.get_post(None, post_id)
            embed = discord.Embed(color=embed_color)
            embed.set_footer(text=str(post_id))
            embed.set_image(url=post['file_url'])
            if ('tag_string_copyright' in post) and post['tag_string_copyright']:
                embed.add_field(name='Copyright', value=post['tag_string_copyright'])
            if ('tag_string_artist' in post) and post['tag_string_artist']:
                embed.add_field(name = 'Artist', value=post['tag_string_artist'])        
            if ('tag_string_character' in post) and post['tag_string_character']:
                embed.add_field(name = 'Character(s)', value=post['tag_string_character'])
            if ('tag_string_general' in post) and post['tag_string_general']:
                embed.add_field(name = 'General', value=post['tag_string_general'])            
            if ('tag_string_meta' in post) and post['tag_string_meta']:
                embed.add_field(name = 'General', value=post['tag_string_meta'])
            
            post_info = f"Created At: ``{post['created_at']}``\nSize: ``{post['image_width']}``x``{post['image_height']}``\nScore: ``{post['score']}``"

            embed.add_field(name='Post Info', value=post_info, inline=False)
            embed.add_field(name='Added Caption', value=json_interface.get_response(None, post_id), inline=False)

            await ctx.interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Fetching failed.', description=f'An exception has occurred while fetching an image from Danbooru.\nError: {e}\n```{traceback.format_exc()}```', color=embed_color)
            await ctx.send_response(embed=embed, ephemeral=True)
    
    @commands.slash_command(name='label', description='Label an image')
    @discord.option(
        'tags',
        str,
        description = 'Tags to use for fetching an image to label',
        required = False,
    )
    @discord.option(
        'post_id',
        str,
        description = 'A specific Danbooru post_id to fetch for labelling',
        required = False
    )
    async def label(self, ctx: discord.ApplicationContext, tags: Optional[str]=None, post_id: Optional[int]=None):
        try:
            if tags is not None: assert isinstance(tags, str)
            if post_id is not None: assert isinstance(post_id, int)

            while True:
                post = self.get_post(tags, post_id)
                if json_interface.get_response(None, int(post['id'])):
                    continue
                else:
                    break

            embed = discord.Embed(color=embed_color)
            embed.set_footer(text=post['id'])
            embed.set_image(url=post['file_url'])
            if ('tag_string_copyright' in post) and post['tag_string_copyright']:
                embed.add_field(name='Copyright', value=post['tag_string_copyright'])
            if ('tag_string_artist' in post) and post['tag_string_artist']:
                embed.add_field(name = 'Artist', value=post['tag_string_artist'])        
            if ('tag_string_character' in post) and post['tag_string_character']:
                embed.add_field(name = 'Character(s)', value=post['tag_string_character'])
            if ('tag_string_general' in post) and post['tag_string_general']:
                embed.add_field(name = 'General', value=post['tag_string_general'])            
            if ('tag_string_meta' in post) and post['tag_string_meta']:
                embed.add_field(name = 'General', value=post['tag_string_meta'])
            
            post_info = f"Created At: ``{post['created_at']}``\nSize: ``{post['image_width']}``x``{post['image_height']}``\nScore: ``{post['score']}``"

            embed.add_field(name='Post Info', value=post_info, inline=False)

            await ctx.interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='Labeling failed.', description=f'An exception has occurred while fetching an image from Danbooru.\nError: {e}\n```{traceback.format_exc()}```', color=embed_color)
            await ctx.send_response(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(DataCog(bot))
