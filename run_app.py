import os
import sys

# 작업 디렉토리 변경
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# streamlit 실행
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "app.py"]
sys.exit(stcli.main())

