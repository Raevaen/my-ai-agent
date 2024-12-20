from termcolor import colored
from ollamamodel import OllamaModel
from toolbox import ToolBox

agent_system_prompt_template = """
You are an agent with access to a toolbox. Given a user query, 
you will determine which tool is best suited to answer the query if none is found then it's ok. 
You will generate the following JSON response:

"tool_choice": "name_of_the_tool",
"tool_input": "inputs_to_the_tool"

tool_choice: The name of the tool you want to use. It must be a tool from your toolbox or "no tool" if you do not use a tool to solve the task.
tool_input: The specific inputs required for the selected tool. If no tool, just provide a response to the query.
Here is a list of your tools along with their descriptions:
{tool_descriptions}

Make a decision based on the provided user query, the available tools and suggest which tool could be used if "no tool" is found.
Verify that the response is a valid JSON object.
"""

class Agent:
    def __init__(self, tools, model_service, model_name, stop=None):
        """
        Initializes the agent with a list of tools and a model.

        Parameters:
        tools (list): List of tool functions.
        model_service (class): The model service class with a generate_text method.
        model_name (str): The name of the model to use.
        """
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop

    def prepare_tools(self):
        """
        Stores the tools in the toolbox and returns their descriptions.

        Returns:
        str: Descriptions of the tools stored in the toolbox.
        """
        toolbox = ToolBox()
        toolbox.store(self.tools)
        tool_descriptions = toolbox.tools()
        return tool_descriptions

    def think(self, prompt):
        """
        Runs the generate_text method on the model using the system prompt template and tool descriptions.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        dict: The response from the model as a dictionary.
        """
        tool_descriptions = self.prepare_tools()
        agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=tool_descriptions)

        # Create an instance of the model service with the system prompt

        if self.model_service == OllamaModel:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0.1,
                stop=self.stop
            )
        else:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0
            )

        # Generate and return the response dictionary
        try:
            agent_response_dict = model_instance.generate_text(prompt)
            if 'error' in agent_response_dict:
                print(colored(agent_response_dict['error'], 'red'))
                return {"tool_choice": "no tool", "tool_input": agent_response_dict['error']}
            return agent_response_dict
        except Exception as e:
            print(colored(str(e), 'red'))
            return {"tool_choice": "no tool", "tool_input": str(e)}

    def work(self, prompt):
        """
        Parses the dictionary returned from think and executes the appropriate tool.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        The response from executing the appropriate tool or the tool_input if no matching tool is found.
        """
        agent_response_dict = self.think(prompt)
        tool_choice = agent_response_dict.get("tool_choice")
        tool_input = agent_response_dict.get("tool_input")

        for tool in self.tools:
            if tool.__name__ == tool_choice:
                response = tool(tool_input)

                print(colored(response, 'cyan'))
                return
                # return tool(tool_input)

        print(colored(tool_input, 'cyan'))

        return