import os
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.llms import HuggingFaceHub

huggingfacehub_api_token=os.getenv('HUGGINGFACEHUB_API_TOKEN')


def openai_chain():
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="gpt2-medium", model_kwargs={"temperature":0.1, "max_new_tokens":150})

    # llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5", model_kwargs = {"temperature": 0.1, "max_length": 700})
    # llm = HuggingFaceHub(repo_id="teknium/OpenHermes-2.5-Mistral-7B", model_kwargs = {"temperature": 0.1, "max_length": 700})

    prmpt_template = """ System: You are a mental health chatbot who chats with people and give them comforts. You are very sweet, compassionate to the user and easy-to-talk and never use bad words to them. Whether user is feeling overwhelmed, anxious, or just need someone to listen, you are there for them. You are there to provide a listening ear, offer comfort, and help user navigate through whatever they're going through.

    Conversation context:
    {history}   

    <|prompter|> {input}
    <|assistant|> """

    # prmpt_template = """ <|prompter|>{history} {input}
    # <|assistant|> """

    PROMPT = PromptTemplate(input_variables= ["history", "input"], template=prmpt_template)

    memory = ConversationBufferMemory(human_prefix="Human", ai_prefix= "Assistant")

    conversation = ConversationChain(
        prompt = PROMPT,
        llm = llm,
        verbose = True,
        memory = memory
    )
    print("Conversation ====>", conversation)
    return conversation

def run_chain(chain, prompt):
    num_tokens = chain.llm.get_num_tokens(prompt)
    print("Prompt ======>", prompt)
    output = chain.invoke({"input": prompt})
    print("output =========>")
    return output, num_tokens

def clear_memory(chain):
    return chain.memory.clear()
