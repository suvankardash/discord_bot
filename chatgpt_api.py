import openai
API_KEY = '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'
openai.api_key = API_KEY
def chatGPTResponse(conversation):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation
        )
    except openai.error.APIConnectionError:
        return None

def initializeConversation():
    global conversation
    conversation=[]
    conversation.append({'role':'system','content':'How may I help you ? '})
    conversation=chatGPTResponse(conversation)

def getResponse(prompt):
    global conversation
    conversation.append({'role':'user','content':prompt})
    conversation=chatGPTResponse(conversation)
    return conversation[-1]['content'].strip()

if __name__ == "__main__":
    choice=-1
    initializeConversation();
    while(choice!=0):
        prompt=input("enter your prompt message = ")
        response=getResponse(prompt)
        print(response)
        choice=int(input())
