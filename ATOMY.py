import streamlit as st
import pandas as pd

#st.title('Hello World!')

## 구글 연결
import gspread

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "cryptic-honor-351410-5c57b4413112.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/13KBZYE2A9PsMaBkUUdcxgE1IUmHyhvmMFd7lixQWEhM/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet("시트1")

## get_all_values() 함수를 이용해 코드를 실행하면 리스트 형태의 값이 리턴됩니다.
gc1 = gc.open("애터미 제품 잔량").worksheet('시트1')
gc2 = gc1.get_all_values()
gc3 = worksheet.get('A2:B')

## pandas 패키지를 활용해 데이터 프레임으로 받아올 수도 있습니다.
import pandas as pd
df = pd.DataFrame(gc3, columns=gc3[0])
df = df.reindex(df.index.drop(0))

st.dataframe(df)