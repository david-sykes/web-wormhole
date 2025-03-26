import openai
import json
import os


class Agent:
    """
    A class representing an AI agent capable of processing messages,
    using tools, and generating responses.
    """

    def __init__(self, client, model, system_message, tools, tool_map, max_steps=10):
        """
        Initialize the Agent with necessary components.

        :param client: OpenAI client for API calls
        :param model: The language model to use
        :param system_message: Initial system message to set context
        :param tools: List of available tools
        :param tool_map: Dictionary mapping tool names to functions
        """
        self.client = client
        self.model = model
        self.system_message = system_message
        self.messages = [{"role": "system", "content": self.system_message}]
        self.tools = tools
        self.tool_map = tool_map
        if self.tools:
            self.tool_choice = "auto"
        else:
            self.tool_choice = None  # Let the LLM choose the appropriate tool
        self.max_steps = max_steps

    def call_local_tool(self, tool_call) -> str:
        """
        Execute a local tool based on the tool call from the LLM.

        :param tool_call: Object containing tool name and arguments
        :return: Result of the tool execution as a string
        """
        tool_name = tool_call.function.name
        if tool_name not in self.tool_map:
            raise ValueError(f"Tool '{tool_name}' not found in local tool map.")

        try:
            arguments = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError as e:
            raise ValueError("Error decoding tool call arguments.") from e

        # Execute the tool function with parsed arguments
        result = self.tool_map[tool_name](**arguments)
        return str(result)

    def __call__(self, message=""):
        """
        Process a message, interact with the LLM, and handle tool calls.

        :param message: Input message (optional)
        :return: Tuple of (output, response_type)
                 response_type can be 'message' or 'tool_call'
        """
        if message:
            self.messages.append({"role": "user", "content": message})

        # Get completion from the LLM
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice=self.tool_choice
        )
        # If the model decides it wants to do tool calls it will include these in the response
        # There can be multiple tool calls in one response, so handle them all
        if completion.choices[0].message.tool_calls:
            # Handle tool calls
            self.messages.append(completion.choices[0].message) # Append the message once
            tool_calls = completion.choices[0].message.tool_calls
            tool_outputs = []
            for tool_call in tool_calls:
                output = self.call_local_tool(tool_call) #Calculate output from function call
                # Append each function call outcome to the messages
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": output
                })
                tool_outputs.append(output)
            
            # Return the last tool output and mark as tool call
            return tool_outputs, 'tool_call', tool_calls
        else:
            # Handle regular message response
            output = completion.choices[0].message.content # TODO: Should we look into checknig the finish reason here instead? https://platform.openai.com/docs/guides/structured-outputs#json-mode
            self.messages.append({"role": "assistant", "content": output})
            return completion.choices[0], 'message', message

# TODO: this is not quite right as inheriting classes have multiple args so need to fix
    def build_first_prompt(self, question, *args): 
        """
        Build the initial prompt for the agent. This function can be used to build more complex prompts based
        on the user input. It may also call other functions to pre-populate the prompt with data

        :param question: The initial question to process
        :return: The initial prompt
        """
        return question
    
    def run_agent_loop(self, question, *args):
        """
        Run a loop to process a question until an answer is found.

        :param question: The initial question to process
        :return: The final answer
        """
        self.initial_prompt = self.build_first_prompt(question, *args)
        completion, response_type, _ = self.__call__(message=self.initial_prompt)
        print(completion)
        steps = 0
        while steps < self.max_steps:
            if response_type == "tool_call":
                completion, response_type, _ = self.__call__()
            elif response_type == "message":
                if completion.finish_reason == "stop":
                    return completion.message.content
                else:
                    completion, response_type, _ = self.__call__()
            steps += 1
        return "No answer found."

    def run_agent_loop_debug(self, question):
        """
        Run a loop to process a question in debug mode, allowing manual input at each step.

        :param question: The initial question to process
        :return: The final answer
        """
        print("🐞 Entering Agent Debug Mode 🐞")
        print("At each step, you can:")
        print("1. Enter a message to continue the agent's reasoning")
        print("2. Type 'quit' to exit")
        print("-------------------------------------------")

        self.initial_prompt = self.build_first_prompt(question)
        print(f"\n[Initial Prompt]:\n{self.initial_prompt}\n")
        current_output, current_type, current_input = self.__call__(message=self.initial_prompt)
        print(f"\n\nInput (Type: {current_type}):\n\n{current_input}\n\n[Agent Output (Type: {current_type})]:\n\n{current_output}\n\n")

        steps = 0
        while steps < self.max_steps:
            user_input = input("Enter your next message (or 'quit'): ").strip()
            
            if user_input.lower() == 'quit':
                print("Exiting debug mode.")
                return "Debug mode terminated."
            
            current_output, current_type, current_input = self.__call__(message=user_input)
            print(f"\n\nInput (Type: {current_type}):\n\n{current_input}\n\n[Agent Output (Type: {current_type})]:\n\n{current_output}\n\n")
            
            if "Answer:" in current_output:
                return current_output
            
            steps += 1
        
        return "No answer found in debug mode."
