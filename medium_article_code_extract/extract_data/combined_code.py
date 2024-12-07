# Code Block 4
# pyright: reportCallIssue=false
from crewai import Agent, Task, LLM, Crew
import os
from crewai.tools import tool

# from crewai_tools import tool

from crewai_tools import PDFSearchTool

from langchain_community.tools.tavily_search import TavilySearchResults

################################################################################
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama3-8b-8192",
    temperature=0,
    max_tokens=1000,
)

# Code Block 5
################################################################################

rag_tool = PDFSearchTool(
    pdf="/content/17.pdf",
    config=dict(
        llm=dict(
            provider="groq",  # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama3-8b-8192",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="huggingface",  # or openai, ollama, ...
            config=dict(
                model="BAAI/bge-small-en-v1.5",
                # task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    ),
)
# Code Block 6
################################################################################
rag_tool.run("How does exercise price determine for ESOP?")
##########################Response#########################Relevant Content:options or shares. The employees are only able to obtain these shares once the ESOP vesting term has completed. Exercise period: It means the time period which starts after the completion of vesting period within which an employee can exercise his/her right to apply for shares against the vested options in pursuance of the scheme of ESOP approved by the shareholders in general meeting by way of Special Resolution. Exercise price: Means the price payable by an employee for exercising the options granted in pursuance of the scheme of ESOP. ARTICLE JANUARY 2024 | 107 CHARTERED SECRETARYESOP? A. Companies are free to decide the exercise price, which may be issued at a discount or premium but the exercise price determined by the Company shall not be less than the par value of the shares. Q. Does it mandatory for the Company to issue and allot only fresh shares under ESOP scheme? A. No, it is not mandatory for the company to issue and allot only fresh shares under ESOP scheme, but it may choose either option: 1. If Company is willing to issue fresh shares, it should adopt direct route to issue and allot shares under the scheme of ESOP. 2. If the Company is willing to channelize its existing share only, in such case Company should adopt Trust route to issue and allot shares under the scheme of ESOP. Q. How are ESOP taxed in India? A. ESOPs have dual tax effects: 1. When an employee exercises their rights and purchases company’s stock. 2. When the employee sells the stock after exercising the option. TAX TREATMENT AT THE TIME OF BUYING THE SHARES Employees can exerciseFAQs Q. What is an ESOP? A. Thus, we can say that ‘ESOP’ stands for ‘Employee Stock Option Plan’ which is a kind of employee benefit plan that gives employees the right to purchase shares of their employer company at a pre-determined price after a certain time period. Q. Does the ESOP supplement the salary of an employee? A. From the point view of monetary benefits, we can say that ESOPs are often used to supplement the salaries of employees. Instead of paying high salary, employees may be offered ESOPs, which may generate more wealth for employees if the Company is growing and generating good amount of earnings which is over and above break-even point. Q. Is ESOP risky and having any possibility of monetary loss? A. It may be risky, if an employee accepts ESOPs instead of a higher salary, and the organization where they are employed is not growing as per the market standards or in comparison to its competitors, ESOP may result in monetary loss. Q. How does exercise price determine for


# Code Block 7
################################################################################
# Need to include TavilyKey

web_search_tool = TavilySearchResults(k=3)

# Code Block 8
################################################################################
web_search_tool.run("How does exercise price determine for ESOP?")


# Code Block 9
################################################################################


@tool
def router_tool(question):
    """Router Function"""
    if "ESOP" in question:
        return "vectorstore"
    else:
        return "web_search"


# Code Block 10
################################################################################
Router_Agent = Agent(
    role="Router",
    goal="Route user question to a vectorstore or web search",
    backstory=(
        "You are an expert at routing a user question to a vectorstore or web search."
        "Use the vectorstore for questions on concepta related to Retrieval-Augmented Generation."
        "You do not need to be stringent with the keywords in the question related to these topics. Otherwise, use web-search."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


# Code Block 11
################################################################################
Retriever_Agent = Agent(
    role="Retriever",
    goal="Use the information retrieved from the vectorstore to answer the question",
    backstory=(
        "You are an assistant for question-answering tasks."
        "Use the information present in the retrieved context to answer the question."
        "You have to provide a clear concise answer."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


# Code Block 12
################################################################################
Grader_agent = Agent(
    role="Answer Grader",
    goal="Filter out erroneous retrievals",
    backstory=(
        "You are a grader assessing relevance of a retrieved document to a user question."
        "If the document contains keywords related to the user question, grade it as relevant."
        "It does not need to be a stringent test.You have to make sure that the answer is relevant to the question."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


# Code Block 13
################################################################################
hallucination_grader = Agent(
    role="Hallucination Grader",
    goal="Filter out hallucination",
    backstory=(
        "You are a hallucination grader assessing whether an answer is grounded in / supported by a set of facts."
        "Make sure you meticulously review the answer and check if the response provided is in alignmnet with the question asked"
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


# Code Block 14
################################################################################
answer_grader = Agent(
    role="Answer Grader",
    goal="Filter out hallucination from the answer.",
    backstory=(
        "You are a grader assessing whether an answer is useful to resolve a question."
        "Make sure you meticulously review the answer and check if it makes sense for the question asked"
        "If the answer is relevant generate a clear and concise response."
        "If the answer gnerated is not relevant then perform a websearch using 'web_search_tool'"
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm,
)


# Code Block 15
################################################################################
router_task = Task(
    description=(
        "Analyse the keywords in the question {question}"
        "Based on the keywords decide whether it is eligible for a vectorstore search or a web search."
        "Return a single word 'vectorstore' if it is eligible for vectorstore search."
        "Return a single word 'websearch' if it is eligible for web search."
        "Do not provide any other premable or explaination."
    ),
    expected_output=(
        "Give a binary choice 'websearch' or 'vectorstore' based on the question"
        "Do not provide any other premable or explaination."
    ),
    agent=Router_Agent,
    tools=[router_tool],
)


# Code Block 16
################################################################################
retriever_task = Task(
    description=(
        "Based on the response from the router task extract information for the question {question} with the help of the respective tool."
        "Use the web_serach_tool to retrieve information from the web in case the router task output is 'websearch'."
        "Use the rag_tool to retrieve information from the vectorstore in case the router task output is 'vectorstore'."
    ),
    expected_output=(
        "You should analyse the output of the 'router_task'"
        "If the response is 'websearch' then use the web_search_tool to retrieve information from the web."
        "If the response is 'vectorstore' then use the rag_tool to retrieve information from the vectorstore."
        "Return a claer and consise text as response."
    ),
    agent=Retriever_Agent,
    context=[router_task],
    # tools=[retriever_tool],
)

# Code Block 17
################################################################################
grader_task = Task(
    description=(
        "Based on the response from the retriever task for the quetion {question} evaluate whether the retrieved content is relevant to the question."
    ),
    expected_output=(
        "Binary score 'yes' or 'no' score to indicate whether the document is relevant to the question"
        "You must answer 'yes' if the response from the 'retriever_task' is in alignment with the question asked."
        "You must answer 'no' if the response from the 'retriever_task' is not in alignment with the question asked."
        "Do not provide any preamble or explanations except for 'yes' or 'no'."
    ),
    agent=Grader_agent,
    context=[retriever_task],
)


# Code Block 18
################################################################################
hallucination_task = Task(
    description=(
        "Based on the response from the grader task for the quetion {question} evaluate whether the answer is grounded in / supported by a set of facts."
    ),
    expected_output=(
        "Binary score 'yes' or 'no' score to indicate whether the answer is sync with the question asked"
        "Respond 'yes' if the answer is in useful and contains fact about the question asked."
        "Respond 'no' if the answer is not useful and does not contains fact about the question asked."
        "Do not provide any preamble or explanations except for 'yes' or 'no'."
    ),
    agent=hallucination_grader,
    context=[grader_task],
)


# Code Block 19
################################################################################
answer_task = Task(
    description=(
        "Based on the response from the hallucination task for the quetion {question} evaluate whether the answer is useful to resolve the question."
        "If the answer is 'yes' return a clear and concise answer."
        "If the answer is 'no' then perform a 'websearch' and return the response"
    ),
    expected_output=(
        "Return a clear and concise response if the response from 'hallucination_task' is 'yes'."
        "Perform a web search using 'web_search_tool' and return ta clear and concise response only if the response from 'hallucination_task' is 'no'."
        "Otherwise respond as 'Sorry! unable to find a valid response'."
    ),
    context=[hallucination_task],
    agent=answer_grader,
    # tools=[answer_grader_tool],
)
# Code Block 20
################################################################################
rag_crew = Crew(
    agents=[
        Router_Agent,
        Retriever_Agent,
        Grader_agent,
        hallucination_grader,
        answer_grader,
    ],
    tasks=[router_task, retriever_task, grader_task, hallucination_task, answer_task],
    verbose=True,
)


# Code Block 21
################################################################################
inputs = {"question": "Does the ESOP supplement the salary of an employee?"}

rag_crew.kickoff(inputs=inputs)
