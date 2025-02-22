import configparser
import requests

class HKBU_ChatGPT():
    def  init (self,config_='./config.ini'): 
        if type(config_) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_)
        elif type(config_) == configparser.ConfigParser: 
            self.config = config_

    def submit(self,message):
        conversation = [{"role": "user", "content": message}]

        url = (self.config['CHATGPT']['BASICURL']) + "/deployments/" + (self.config['CHATGPT']['MODELNAME']) + "/chat/completions/?api-version=" + (self.config['CHATGPT']['APIVERSION'])

        headers = { 'Content-Type': 'application/json','api-key': (self.config['CHATGPT']['ACCESS_TOKEN']) } 
        payload = { 'messages': conversation }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200: 
            data = response.json()
            return data['choices'][0]['message']['content'] 
        else:
            return 'Error:', response
    def equiped_chatgpt(update, context):
        global chatgpt
        reply_message = chatgpt.submit(update.message.text) 
        logging.info("Update: " + str(update)) 
        logging.info("context: " + str(context))
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


if __name__ == ' main ':
	ChatGPT_test = HKBU_ChatGPT()
	while True:
        	user_input = input("Typing anything to ChatGPT:\t") 
        	response = ChatGPT_test.submit(user_input) 
        	print(response)
        # register a dispatcher to handle message: here we register an echo dispatcher # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        # dispatcher.add_handler(echo_handler)

        # dispatcher for chatgpt global chatgpt
        chatgpt = HKBU_ChatGPT(config)
        chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
        dispatcher.add_handler(chatgpt_handler)
