###Syntax	One-line explanation
#information	   A Python variable that stores the actual data (Albert Einstein's biography).
#{information}	   A placeholder in the prompt template that will be replaced with the variable's value.
#"information"	   A dictionary key (string) used by LangChain to match the placeholder {information}.
###

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

def main():
    print("Hello from langchain-course!")
    information = """ Albert Einstein[a] (14 March 1879 – 18 April 1955) was a German-born theoretical physicist best known for developing the known theory of relativity. Einstein also made important contributions to quantum theory.[1][5] His mass–energy equivalence formula E = mc2, which arises from special relativity, has been called "the world's most famous equation".[6] He received the 1921 Nobel Prize in Physics for "his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect".[7]"""

#{Information} here is blank needs to be filled from above. It is a place holder
    summary_template = """ 
    given the information {information} about a person I want you to create  
    1. A short summary
    2. two interesting facts about them
    """

#PromptTemplate tells LangChain what blanks exist, "information" is blank's name

    summary_prompt_template = PromptTemplate (
        input_variables=["information"],
        template=summary_template
    )

#Left side information is name given for the blank, right side is actual value

    #llm = ChatOpenAI(temperature=0, model="gpt-5")
    llm = ChatOllama(temperature=0, model="gpt-oss:20b")
    chain = summary_prompt_template | llm
    response = chain.invoke(
        input={"information": information}  #it must match - Dictinoary key : python variable
    )
    print(response.content)

if __name__ == "__main__":
    main()



