以下を参照
https://github.com/mkazutaka/software-design-202408-llmapp

# 仮想環境の構築（たぶん初回のみでいいはず）
python3 -m venv venv

# アクティベート（毎回）
source venv/bin/activate

# パッケージインストール（初回のみ）
pip install langchain==0.2.3
pip install langchain-openai==0.1.8
pip install streamlit==1.35.0

または

pip install -r requirements.txt
