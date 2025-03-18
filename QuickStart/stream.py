import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

assistant = client.beta.assistants.create(
  name="Yong Math Tutor Test - With Stream",
  instructions="You are a personal math tutor. Write and run code to answer math questions.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
 
with client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
    stream=True,
) as stream:
  for event in stream:
    print(event.model_dump_json(indent=2, exclude_unset=True))

