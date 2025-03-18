import os
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Step 1: Upload a file 
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/files.py#L60-L71
file = client.files.create(
  file=open("city.csv", "rb"),
  purpose='assistants'
)

# Step 2: Create an assistant
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/assistants.py#L57-L77
assistant = client.beta.assistants.create(
  name="Yong Test Without Streaming- Favoriate City",
  instructions="You are a helpful assistant. When asked a question, you answer the question",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

# Step 3: Create a thread
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/threads.py#L92-L104
thread = client.beta.threads.create()

# Step 4: Add a message to this thread
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/messages.py#L53-L67
user_input = input("Enter a name who you want see his/her favriate city in the CSV file. i.e. Tina Escobar: ")
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="Explain why a city is the favorite city of " + user_input
)
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.

print("In Progress...")

# Step 5: Create a run
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/runs/runs.py#L1109-L1136
with client.beta.threads.runs.stream(
  thread_id=thread.id,
  assistant_id=assistant.id,
  max_completion_tokens=300,
  event_handler=EventHandler(),
) as stream:
  stream.until_done()
  for event in stream:
    print(event.model_dump_json(indent=2, exclude_unset=True))

# Step 6: delete assitant
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/assistants.py#L445-L455	
client.beta.assistants.delete(assistant.id)
