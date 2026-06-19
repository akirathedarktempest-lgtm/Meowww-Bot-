import discordrpc

rpc=discordrpc.RPC(app_id="your application id/go to developer portal, then your bot and then there will be application id, copy it and paste here")

rpc.set_activity(
    large_image="download_11_",#I am not going to apply the texts, because your bot's name will show up already and for now, let's keep this simple
    small_image="sua"#and, these are the names of images, go to your bot in developer's portal/go to rich presence/art assests/add images from your device/and what will be the name there, you will paste that, the name appearing 
)
rpc.run()#and this is a simple rpc of my meowww bot, I will develop it more, add buttons and more on later
