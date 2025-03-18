import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

assistant = client.beta.assistants.create(
  name="Yong Math Tutor Test - Without Stream",
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

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(thread_id=thread.id)

  print("messages: ")
  for message in messages:
    assert message.content[0].type == "text"
    print({"role": message.role, "message": message.content[0].text.value})
else:
  print(run.status)