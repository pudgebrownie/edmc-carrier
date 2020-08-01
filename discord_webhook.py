
import json
import requests

class DiscordWebhook: 


    def __init__(self, url, **kwargs):
        self.url = url
        self.username = kwargs.get('username')
        self.content = kwargs.get('content', '')
        self.embeds = kwargs.get('embeds', [])


    def add_embed(self, embed):
        if not isinstance(embed, DiscordEmbed):
            raise TypeError(f"Invalid argument {embed}. It should be of type DiscordEmbed")
        self.embeds.append(embed.__dict__)


    def to_req_payload(self):
        data = dict()
        for key, value in self.__dict__.items():
            if key != 'url':
                data[key] = value
        return data


    def send(self):
        response = requests.post(self.url, json=self.to_req_payload())
      

class DiscordEmbed:


    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.image = kwargs.get('image', {})
        self.footer = kwargs.get('footer', {})
        self.fields = kwargs.get('fields', [])
        self.color = kwargs.get('color', 0)


    def add_field(self, name, value, is_inline = True):
        self.fields.append(
            {
                'name': name,
                'value': value,
                'inline': is_inline
            }
        )


    def add_image_url(self, url):
        self.image = {
            'url': url
        }


    def add_footer(self, footer):
        self.footer = {
            'text': footer
        }
        