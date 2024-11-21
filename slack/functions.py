from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# .envファイルから環境変数を読み込む
load_dotenv(find_dotenv())

# メールを下書きを作成する関数を定義
def draft_email(user_input):
    pass
