# EDMC-Carrier Plugin
A simple plugin for [EDMarketConnector](https://github.com/EDCD/EDMarketConnector) for sending Fleet Carrier jump notifications to Discord. The plugin watches the following carrier journal log events:

- `CarrierJumpRequest` - When the fleet carrier owner requests a jump to a system
- `CarrierJumpCancelled` - When the fleet carrier owner cancels a pending jump
- `CarrierJump` - When the fleet carrier arrives on a the destination system

`Discord Webhooks` are used to send notifications to a specified channel.

# Installation and Setup

1. Create `Discord Webhook`. See `Webhooks` section of https://support.discord.com/hc/en-us/articles/360045093012-Server-Integrations-Page. Copy and save the URL of the new `Discord Webhook`.

2. (Optional) Upload an image of your carrier to your cloud storage or website (*i.e. Dropbox, Google Drive, Inara, etc.*). Copy and save image URL (must be HTTPS as per Discord's requirement). 

3. Download the `EDMC-Carrier` plugin as zip [here](https://github.com/pudgebrownie/edmc-carrier/archive/master.zip) and extract under the EDMarketConnector `plugins` folder. The default location of the `plugins` is located at: 

    - Windows: `C:\Users\<YOUR_USER>\AppData\Local\EDMarketConnector\plugins`
    - Mac: `~/Library/Application Support/EDMarketConnector/plugins`
    - Linux: `$XDG_DATA_HOME/EDMarketConnector/plugins`

4. Launch `EDMarketConnector` and navigate to `File -> Settings -> EDMC-Carrier` tab

5. Configure the following: 

    - **Discord Webhook URL (Required):** URL of the Discord Webhook generated in step 1
    - **Carrier Name (Required):** Your carrier name / call sign in-game
    - **Carrier Image URL (Optional):** URL of your preferred image of your carrier uploaded in step 2

6. Hit `Ok` and you are done! 
