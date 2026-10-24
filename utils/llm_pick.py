
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


def pick_llm(level: str):
    """
    Picks the appropriate LLM based on the level of the question.
    """
    if level.lower() == "low":
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            temperature=0,
        )

    elif level.lower() == "medium":
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            temperature=0,
        )

    elif level.lower() == "high":
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.8-flash",
            temperature=0,
        )

    elif level.lower() == "claude":
        llm = ChatAnthropic(model_name="claude-sonnet-5")

    else:
        raise ValueError(f"Unsupported level: {level}")

    return llm


if __name__ == "__main__":
    llm_obj = pick_llm("low")
    response = llm_obj.invoke("What is the capital of France?")
    print(response.text)
