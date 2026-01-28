from shlex import join
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from src.api.models.generate.goal import GoalDetail, GoalInput
from src.api.models.generate.formula import FormulaDetail, FormulaInput
from src.api.models.generate.eval_template import EvalTemplate, EvalTemplateInput, get_eval_template_model
from langchain_openai import ChatOpenAI
from src.config import settings
from src.prompt import CREATE_GOAL_PROMPT, CREATE_FORMULA_PROMPT, CREATE_EVAL_TEMPLATE_PROMPT
from langfuse.langchain import CallbackHandler
from src.core.tools.builtin_tool.http_request_runner import do_async_http_request
from src.utils.read_file import load_file_to_text
import json
from pydantic import Field

class GenerateService:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.LLM_CONFIG["openai"]["model"],
            temperature=settings.LLM_CONFIG["openai"]["temperature"],
            api_key=settings.LLM_CONFIG["openai"]["api_key"],
            base_url=settings.LLM_CONFIG["openai"]["base_url"],
            max_tokens=2000,
            # reasoning_effort="minimal"
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

    async def create_eval_template(self, input: EvalTemplateInput):

        # extra_fields = {}
        # for column in input.columns:
        #     extra_fields[column] = (str, Field(description=column))

        # EvalTemplate = get_eval_template_model(extra_fields=extra_fields)

        parser = JsonOutputParser(pydantic_object=EvalTemplate)

        text_documents = load_file_to_text(input.attachment_url)

        if input.is_use_system_data:
            async_result = await do_async_http_request(
                url=settings.MULTI_AGENT_CONFIG[input.project_code]["settings"].get("url_endpoint")+"proxy/shared/api/v1/Dynamic/GetDataSourceByDynamicStore",
                method="POST",
                query_params={
                    "StoreName": "sp_get_cat_criteria",
                    "dataSourceRequestString": "page=1&pageSize=20&group=GroupName-asc",
                    "DataFormSearch": {
                        "Type": "E_COMPETENCY"
                    }
                },
                auth_params = {
                    "token": settings.API_TOKEN,
                    "url_endpoint": settings.MULTI_AGENT_CONFIG["settings"].get("url_endpoint", ""),
                    "username": settings.MULTI_AGENT_CONFIG["settings"].get("username", ""),
                    "password": settings.MULTI_AGENT_CONFIG["settings"].get("password", ""),
                    "token_url": settings.MULTI_AGENT_CONFIG["settings"].get("token_url", ""),
                    "client_id": settings.MULTI_AGENT_CONFIG["settings"].get("client_id", ""),
                    "client_secret": settings.MULTI_AGENT_CONFIG["settings"].get("client_secret", ""),
                },
                auth_method="oauth2"
            )
            competency = json.dumps(async_result.data['Data']['Data'])
        else:
            competency = "empty"

        messages = [SystemMessagePromptTemplate.from_template(CREATE_EVAL_TEMPLATE_PROMPT)]

        if input.chat_history is not None:
            for chat in input.chat_history:
                if chat.human is not None:
                    messages.append(HumanMessage(content=chat.human))
                if chat.bot is not None:
                    messages.append(AIMessage(content=chat.bot))

        prompt = ChatPromptTemplate(
            messages=messages,
            partial_variables={
                "format_instructions": parser.get_format_instructions(),
                "prompt": input.prompt,
                "documents": text_documents,
                "competency": competency,
                "template_name": input.template_name ,
                "template_type": input.template_type,
                "departments": ','.join(input.departments),
                "positions": ','.join(input.positions)
            },
        )

        return self.handle_response(input.prompt, prompt, parser)

    def handle_response(self,question: str, prompt: PromptTemplate, parser: JsonOutputParser):
        
        chain = prompt | self.model | parser

        response = chain.invoke({"question": question}, config={"callbacks":[self.langfuse_handler]})

        result = {}
        if "properties" in response:
            result["response"] = response["properties"]
        elif "data" in response:
            result["response"] = response["data"]
        elif isinstance(response, dict):
            result["response"] = [response]
        else:
            result["response"] = response

        return result