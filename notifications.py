from discord_webhook import DiscordWebhook, DiscordEmbed
import date_util


DEFAULT_CARRIER_IMAGE_URL = "https://cdn.vox-cdn.com/thumbor/qDJDN54D-g3XfSttcsdV55wKQD8=/0x0:1200x878/920x613/filters:focal(400x472:592x664):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/65539852/Fleet_Carrier.0.jpg"


class CarrierNotificationDispatcher:


    def __init__(self, **kwargs):
        self.webhook_url = kwargs.get('webhook_url', '')
        self.carrier_name = kwargs.get('carrier_name', '')
        self.carrier_image_url = kwargs.get('carrier_image_url', DEFAULT_CARRIER_IMAGE_URL)


    def send_jump_request_notification(self, cmdr_name, curr_system, dest_system, timestamp):
        webhook = DiscordWebhook(
            url = self.webhook_url,
            username = f"{self.carrier_name} Nav Ops"
        )

        embed = DiscordEmbed(
            title = 'Carrier Jump Request',
            description = f"**CMDR {cmdr_name}** initiated jump sequence for **{self.carrier_name}**",
            color = 16776960
        )
        embed.add_image_url(self.carrier_image_url)
        embed.add_footer('Dates displayed are in-game time (GMT)')
        
        jumped_at_time = date_util.rfc3339_to_datetime(timestamp)
        lockdown_time = date_util.add_time(jumped_at_time, minutes=13, seconds=20)
        embed.add_field('Jumping From', curr_system)
        embed.add_field('Arriving At', dest_system)
        embed.add_field('Estimated Lockdown', date_util.format_date(lockdown_time, date_util.MILITARY_TIME_FORMAT))

        webhook.add_embed(embed)
        webhook.send()


    def send_jump_cancellation_notification(self, cmdr_name, curr_system):
        webhook = DiscordWebhook(
            url = self.webhook_url,
            username = f"{self.carrier_name} Nav Ops"
        )

        embed = DiscordEmbed(
            title = 'Carrier Jump Cancelled',
            description = f"**CMDR {cmdr_name}** cancelled the jump of **{self.carrier_name}**. Carrier will remain at **{curr_system}**",
            color = 10824234
        )
        embed.add_image_url(self.carrier_image_url)
        
        webhook.add_embed(embed)
        webhook.send()


    def send_jump_notification(self, dest_system, timestamp):
        webhook = DiscordWebhook(
            url = self.webhook_url,
            username = f"{self.carrier_name} Nav Ops"
        )

        embed = DiscordEmbed(
            title = 'Carrier Has Arrived!',
            description = f"**{self.carrier_name}** arrived at **{dest_system}**",
            color = 8388352
        )
        embed.add_image_url(self.carrier_image_url)
        embed.add_footer('Dates displayed are in-game time (GMT)')

        arrived_at = date_util.rfc3339_to_datetime(timestamp)
        embed.add_field('Arrival Time', date_util.format_date(arrived_at, date_util.MILITARY_TIME_FORMAT))
        
        webhook.add_embed(embed)
        webhook.send()
