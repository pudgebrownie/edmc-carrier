
import sys
import tkinter as tk
import myNotebook as nb
from config import config
from notifications import CarrierNotificationDispatcher

# config constants
WEBHOOK_URL_CONFIG_KEY = 'edmc-carrier.webhook_url'
CARRIER_NAME_CONFIG_KEY = 'edmc-carrier.carrier_name'
CARRIER_IMAGE_URL_CONFIG_KEY = 'edmc-carrier.carrier_image_url'
USE_BODY_INFO_CONFIG_KEY = 'edmc-carrier.use_body_info'

this = sys.modules[__name__]
carrier_notification_dispatcher = CarrierNotificationDispatcher()


def plugin_start3(plugin_dir):
    print("Loading EDMC-Carrier {}. Setting preferences...".format(plugin_dir))

    webhook_url = __load_config(WEBHOOK_URL_CONFIG_KEY)
    carrier_name = __load_config(CARRIER_NAME_CONFIG_KEY)
    carrier_image_url = __load_config(CARRIER_IMAGE_URL_CONFIG_KEY)
    this.use_body_info = __load_config(USE_BODY_INFO_CONFIG_KEY)

    carrier_notification_dispatcher.__setattr__('webhook_url', webhook_url)
    carrier_notification_dispatcher.__setattr__('carrier_name', carrier_name)
    carrier_notification_dispatcher.__setattr__('carrier_image_url', carrier_image_url)
    carrier_notification_dispatcher.__setattr__('use_body_info', this.use_body_info)
   
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

    if not __load_config(USE_BODY_INFO_CONFIG_KEY):
        this.use_body_info = tk.IntVar(value = 0)
    else:
        this.use_body_info = tk.IntVar(value = 1)

    this.prefs_use_body_info_button = nb.Checkbutton(
            frame,
            text = "Include Body Name",
            variable = this.use_body_info
        )
    this.prefs_use_body_info_button.grid(row=4, padx=10, pady=2, sticky=tk.W)

    return frame

def prefs_changed(cmdr, is_beta):
    new_webhook_url = this.prefs_webhook_url.get().strip()
    new_carrier_name = this.prefs_carrier_name.get().strip()
    new_carrier_image_url = this.prefs_carrier_image_url.get().strip()
    new_use_body_info = this.use_body_info.get()

    carrier_notification_dispatcher.__setattr__('webhook_url', new_webhook_url)
    carrier_notification_dispatcher.__setattr__('carrier_name', new_carrier_name)
    carrier_notification_dispatcher.__setattr__('carrier_image_url', new_carrier_image_url)
    carrier_notification_dispatcher.__setattr__('use_body_info', new_use_body_info)

    config.set(WEBHOOK_URL_CONFIG_KEY, new_webhook_url)
    config.set(CARRIER_NAME_CONFIG_KEY, new_carrier_name)
    config.set(CARRIER_IMAGE_URL_CONFIG_KEY, new_carrier_image_url)
    config.set(USE_BODY_INFO_CONFIG_KEY, new_use_body_info)


def journal_entry(cmdr, is_beta, system, station, entry, state):
    event_name = entry.get("event")

    if this.use_body_info:
        destination = entry.get('Body')
    else:
        destination = entry.get('SystemName')
    
    if event_name == 'CarrierJumpRequest':
        timestamp = entry.get('timestamp')
        carrier_notification_dispatcher.send_jump_request_notification(cmdr, destination, timestamp)


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

