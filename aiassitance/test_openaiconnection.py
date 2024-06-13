from openai import OpenAI, AssistantEventHandler
from typing_extensions import override


assistantid = "asst_NK4twNo6kRlGH37C6HbNsMYb"

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




  

if __name__=="__main__":
  client = OpenAI()
  # with open(r"C:\Users\MarcRotsaert\temp\test.json", "rb") as g:
  #   uploaded_file = client.files.create(file=g, purpose='assistants')
  # client.files.create(file=uploaded_file, purpose='search')
  # print(client)
  assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o",
  )
  
  
  # upload_file(assistant)


  # print(assistant.tool_resources)
  thread = client.beta.threads.create()

  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
  )
  print(message)
  with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistantid,
    instructions="Please address the user as Jane Doe. The user has the right account. Return my own name after the answer",
    event_handler=EventHandler(),
  ) as stream:
    stream.until_done()
