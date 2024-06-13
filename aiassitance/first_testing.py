from typing_extensions import override
from openai import OpenAI
from openai import AssistantEventHandler



# From Quick start, override methods event handler
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
    
    
    # def on_message_done(self, message):    
    # Then, we use the `stream` SDK helper 
    # with the `EventHandler` class to create the Run 
    # and stream the response.
        # message_content = message.content[0].image_file
  
# assistant = client.beta.assistants.create(
#   name="Math Tutor",
#   instructions="You are a personal math tutor. Write and run code to answer math questions.",
#   tools=[{"type": "code_interpreter"}],
#   model="gpt-4o",
# )

# As an example
def uploadfile2assitant(assistant):
    client.beta.assistants.update(assistant_id=assistantid)

    # Create a vector store caled "Financial Statements"
    vector_store = client.beta.vector_stores.create(name="testjson")
    
    # Ready the files for upload to OpenAI
    file_paths = [r"C:\Users\MarcRotsaert\temp\test.json"]
    file_streams = [open(path, "rb") for path in file_paths]
    
    # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    # and poll the status of the file batch for completion.
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
      vector_store_id=vector_store.id, files=file_streams
    )
 
  # You can print the status and the file counts of the batch to see the result of this operation.
    print(file_batch.status)
    print(file_batch.file_counts)
    assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

# def uploadfile2thread(thread):
#     thread



if __name__=="__main__":
    assistant_id = "asst_NK4twNo6kRlGH37C6HbNsMYb"
    
    client = OpenAI()
    
    assistant = client.beta.assistants.retrieve(assistant_id)

    thread = client.beta.threads.create()

    message_file = client.files.create(file=open(r"C:\Users\MarcRotsaert\temp\temp.jpg", "rb"),
                                       purpose="assistants")

    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Show me the picture upside down?",
    attachments=[{ "file_id": message_file.id, "tools": [{"type": "code_interpreter"}]}],
    )    
    
    with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe.",
    event_handler=EventHandler(),
    ) as stream:
      stream.until_done()
