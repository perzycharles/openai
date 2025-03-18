import os
from openai import OpenAI
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

print("In Progress...")

# Step 5: Create a run
# Option 1: Periodically retrieve the Run object to check the status
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/runs/runs.py#L536-L564
# run = client.beta.threads.runs.create(
#   thread_id=thread.id,
#   assistant_id=assistant.id,
#   max_completion_tokens=100
# )

# Step 6: Print result and delet the assistant
# while True:
# 	# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/runs/runs.py#L604-L615
# 	run_job = client.beta.threads.runs.retrieve(
# 		thread_id=thread.id,
# 		run_id=run.id
# 	)
# 	if run_job.status == 'completed': 
# 		# Source code: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/messages.py#L202-L217
# 		messages = client.beta.threads.messages.list(thread_id=thread.id)
# 		print("messages: ")
# 		for message in messages:
# 			assert message.content[0].type == "text"
# 			print({"role": message.role, "message": message.content[0].text.value})
# 		break
# 	elif run_job.status == 'incomplete':
# 		print("Run job is incompete due to ", run_job.incomplete_details)
# 		break


# Option 2 for Step 5 and 6: create_and_poll only returns when terminal_states, so don't need to periodically retrieve the Run object to check the status.
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/threads/runs/runs.py#L1019

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
  max_completion_tokens=100
)

if run.status == 'completed': 
	messages = client.beta.threads.messages.list(thread_id=thread.id)
	print("messages: ")
	for message in messages:
		assert message.content[0].type == "text"
		print({"role": message.role, "message": message.content[0].text.value})
elif run.status == 'incomplete':
	run_job = client.beta.threads.runs.retrieve(
	thread_id=thread.id,
	run_id=run.id
	)
	print("Run job is incompete due to ", run_job.incomplete_details)

# Step 7: delete assitant
# Definition: https://github.com/openai/openai-python/blob/2954945ecc185259cfd7cd33c8cbc818a88e4e1b/src/openai/resources/beta/assistants.py#L445-L455	
client.beta.assistants.delete(assistant.id)
