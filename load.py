
import sys
import tkinter as tk
import myNotebook as nb
from config import config
from notifications import CarrierNotificationDispatcher

# config constants
WEBHOOK_URL_CONFIG_KEY = 'edmc-carrier.webhook_url'
CARRIER_NAME_CONFIG_KEY = 'edmc-carrier.carrier_name'
CARRIER_IMAGE_URL_CONFIG_KEY = 'edmc-carrier.carrier_image_url'

this = sys.modules[__name__]
carrier_notification_dispatcher = CarrierNotificationDispatcher()


def plugin_start3(plugin_dir):
    print("Loading EDMC-Carrier {}. Setting preferences...".format(plugin_dir))

    webhook_url = __load_config(WEBHOOK_URL_CONFIG_KEY)
    carrier_name = __load_config(CARRIER_NAME_CONFIG_KEY)
    carrier_image_url = __load_config(CARRIER_IMAGE_URL_CONFIG_KEY)

    carrier_notification_dispatcher.__setattr__('webhook_url', webhook_url)
    carrier_notification_dispatcher.__setattr__('carrier_name', carrier_name)
    carrier_notification_dispatcher.__setattr__('carrier_image_url', carrier_image_url)
   
    return "EDMC-Carrier"


def plugin_stop():
    print("Stopping EDMC-Carrier plugin")


def plugin_prefs(parent, cmd, is_beta):
    webhook_url = __load_config(WEBHOOK_URL_CONFIG_KEY)
    carrier_name = __load_config(CARRIER_NAME_CONFIG_KEY)
    carrier_image_url = __load_config(CARRIER_IMAGE_URL_CONFIG_KEY)

    frame = nb.Frame(parent)
    nb.Label(frame, text='Discord Webhook URL').grid(row=1, padx=10, pady=2, sticky=tk.W)
    this.prefs_webhook_url = nb.Entry(frame)
    this.prefs_webhook_url.insert(tk.END, webhook_url)
    this.prefs_webhook_url.grid(row=1, column=1, padx=10, pady=2, sticky=tk.EW)

    nb.Label(frame, text="Carrier Name").grid(row=2, padx=10, pady=2, sticky=tk.W)
    this.prefs_carrier_name = nb.Entry(frame)
    this.prefs_carrier_name.insert(tk.END, carrier_name)
    this.prefs_carrier_name.grid(row=2, column=1, padx=10, pady=2, sticky=tk.EW)

    nb.Label(frame, text="Carrier Image URL").grid(row=3, padx = 10, pady=2, sticky=tk.W)
    this.prefs_carrier_image_url= nb.Entry(frame)
    this.prefs_carrier_image_url.insert(tk.END, carrier_image_url)
    this.prefs_carrier_image_url.grid(row=3, column=1, padx=10, pady=2, sticky=tk.EW)

    return frame


def prefs_changed(cmdr, is_beta):
    new_webhook_url = this.prefs_webhook_url.get().strip()
    new_carrier_name = this.prefs_carrier_name.get().strip()
    new_carrier_image_url = this.prefs_carrier_image_url.get().strip()

    carrier_notification_dispatcher.__setattr__('webhook_url', new_webhook_url)
    carrier_notification_dispatcher.__setattr__('carrier_name', new_carrier_name)
    carrier_notification_dispatcher.__setattr__('carrier_image_url', new_carrier_image_url)

    config.set(WEBHOOK_URL_CONFIG_KEY, new_webhook_url)
    config.set(CARRIER_NAME_CONFIG_KEY, new_carrier_name)
    config.set(CARRIER_IMAGE_URL_CONFIG_KEY, new_carrier_image_url)


def journal_entry(cmdr, is_beta, system, station, entry, state):
    event_name = entry.get("event")
    
    if event_name == 'CarrierJumpRequest':
        curr_system = system
        dest_system = entry.get('SystemName')
        timestamp = entry.get('timestamp')
        carrier_notification_dispatcher.send_jump_request_notification(cmdr, curr_system, dest_system, timestamp)


    if event_name == "CarrierJumpCancelled":
        carrier_notification_dispatcher.send_jump_cancellation_notification(cmdr, system)


    if event_name == "CarrierJump":
        timestamp = entry.get('timestamp')
        carrier_notification_dispatcher.send_jump_notification(system, timestamp)


def __load_config(key):
    value = config.get(key)
    if not value: 
        value = ''
    return value

