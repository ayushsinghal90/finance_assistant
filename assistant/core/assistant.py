import logging
from langchain_openai import ChatOpenAI

from ..exceptions.AssistantError import AssistantError

logger = logging.getLogger('myapp')

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
structured_llm = model.with_structured_output(method="json_mode")


class Assistant:

    def extract_finance_info(self, content):
        try:
            logger.info("Calling LLM model for finance info")
            return structured_llm.invoke(
                """Please extract financial information in Json format from the following text and categorize it into
                three specific categories: assets, expenditures, income and summary.

                    Definitions: 1. **assets**: Items of value owned by an individual or entity, such as cash or emergency fund,
                    property, investments, equipment and others. 2. **expenditures**: Expenses or costs incurred
                    by an individual or entity, including bills, purchases, salaries, and other spending. 3. **income**:
                    Money received by an individual or entity, such as salaries, sales revenue, interest, and dividends.
                    4. **summary**: Client financially summary including future goals and steps needed to be taken. 

                    Text:
                """ + f"{content}")
        except Exception as e:
            raise AssistantError("Failed to get response from ai model", e)
