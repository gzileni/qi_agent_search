import asyncio
import uuid
import os
import argparse
from py_agent_search import AgentSearch, send_log

redis_conf = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": os.getenv("REDIS_PORT", 6379),
    "db": os.getenv("REDIS_DB", 0)
}

async def main(question):
    """
    Main function to run the chat interaction.
    It initializes the Chat class and calls the chat method with a question and context.
    """
    try:
        thread_id = "agent_search_conversation"
        
        if not question:
            question = input("Enter your question: ")
        print("You can type 'exit' to quit the chat.")
        if question.lower() == 'exit':
            return
        # Send the initial log message
        send_log(message="Starting chat interaction", metadata={"question": question})
        print(f"Question: {question}\n Waiting for response...")
        
        agent = AgentSearch(redis_persistence_config=redis_conf)
        async for token in agent.stream(input=question, thread_id=thread_id):
            print(token, end="", flush=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        send_log(message="Error during chat interaction", metadata={"error": str(e)})
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat with AgentSearch")
    parser.add_argument("--question", type=str, help="Question to ask the agent")
    args = parser.parse_args()
    asyncio.run(main(args.question))