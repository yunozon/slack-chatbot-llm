from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# .envファイルから環境変数を読み込む
load_dotenv(find_dotenv())

# メールを下書きを作成する関数を定義
def draft_email_with_chatgpt(user_input):
    """
    ユーザーからの入力に基づいて、メールの下書きを作成する。
    Args:
        user_input (str): ユーザーからの入力(メッセージ内容)
    Returns:
        str: 作成されたメールの下書き
    """
    # チャットモデルの初期化
    chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature = 1.0)

    # システムメッセージのプロンプトを作成
    template = """

    あなたは新しいメールに基づいて返信するメールの草案を作成する有用なアシスタントです。
    ユーザーが迅速に完璧なメール返信を出来るようにサポートします。
    返信は簡潔で要点を押さえ、元のメールスタイルを模倣して、トーンを合わせてください。
    """
    # システムメッセージのプロンプトを作成
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    # ヒューマンメッセージプロンプトの作成
    human_template = "以下は返信するメールです。ユーザーのコメントも考慮して返信してください: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # チャットプロンプトを組み立てる
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt],
    )

    # LLMチェーンを作成 下記のコードは非推奨(バージョン理由により)
     # chain = LLMChain(llm=chat, prompt=chat_prompt)
    # response = chain.run(user_input=user_input, signature=signature)
    response = (chat_prompt | chat).invoke(input=user_input)

    return response

def draft_email_with_gemini(user_input):
    
    llm = ChatGoogleGenerativeAI(
        model = "gemini-1.5-flash-8b",
        temperature=1.0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    system_template = """

    あなたは新しいメールに基づいて返信するメールの草案を作成する有用なアシスタントです。
    ユーザーが迅速に完璧なメール返信を出来るようにサポートします。
    返信は簡潔で要点を押さえ、元のメールスタイルを模倣して、トーンを合わせてください。
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # ヒューマンメッセージプロンプトの作成
    human_template = "以下は返信するメールです。ユーザーのコメントも考慮して返信してください: {user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # チャットプロンプトを組み立てる
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt],
    )
    response = (chat_prompt | llm).invoke(input=user_input)
    return response
