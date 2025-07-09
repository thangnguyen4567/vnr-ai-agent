from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from src.api.models.generate.goal import GoalDetail, GoalInput
from src.api.models.generate.formula import FormulaDetail, FormulaInput
from langchain_openai import ChatOpenAI
from src.config import settings
from src.prompt import CREATE_GOAL_PROMPT, CREATE_FORMULA_PROMPT
from langfuse.langchain import CallbackHandler

class GenerateService:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.LLM_CONFIG["openai"]["model"],
            temperature=settings.LLM_CONFIG["openai"]["temperature"],
            api_key=settings.LLM_CONFIG["openai"]["api_key"],
            max_tokens=2000,
        )
        self.langfuse_handler = CallbackHandler()

    def create_goal(self, input: GoalInput):

        parser = JsonOutputParser(pydantic_object=GoalDetail)

        prompt = PromptTemplate(
            template=CREATE_GOAL_PROMPT,
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
                "question": input.question,
            },
        )

        return self.handle_response(input.question, prompt, parser)

    def create_formula(self, input: FormulaInput):

        parser = JsonOutputParser(pydantic_object=FormulaDetail)

        message = [SystemMessagePromptTemplate.from_template(CREATE_FORMULA_PROMPT)]

        if input.chat_history is not None:
            for chat in input.chat_history:
                if "human" in chat:
                    message.append(HumanMessage(content=chat["human"]))
                if "bot" in chat and chat["bot"] != None:
                    message.append(AIMessage(content=chat["bot"]))
            message.append(HumanMessagePromptTemplate.from_template("{question}"))

        prompt = ChatPromptTemplate(
            messages=message,
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
                "enum": input.enum,
                "prompt": input.prompt,
                "question": input.question,
            },
        )
        return self.handle_response(input.question, prompt, parser)


    def handle_response(self,question: str, prompt: PromptTemplate, parser: JsonOutputParser):
        
        chain = prompt | self.model | parser

        response = chain.invoke({"question": question}, config={"callbacks":[self.langfuse_handler]})

        result = {}
        if "properties" in response:
            result["response"] = response["properties"]
        else:
            result["response"] = response

        return result