import streamlit as st

#st.title('Hello World!')

## 구글 연결
import gspread

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "F:/cryptic-honor-351410-5c57b4413112.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/161C34zeA2iEmrK_vbaktj3um-HNxgsDxkh1LSQCWNp0/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet("★일일 작업량")

## get_all_values() 함수를 이용해 코드를 실행하면 리스트 형태의 값이 리턴됩니다.
gc1 = gc.open("AI 데이터팀_데이터 구축 현황").worksheet('★일일 작업량')
gc2 = gc1.get_all_values()
gc3 = worksheet.get('B12:N')

## pandas 패키지를 활용해 데이터 프레임으로 받아올 수도 있습니다.
import pandas as pd
df = pd.DataFrame(gc3, columns=gc3[0])
df = df.reindex(df.index.drop(0))

def type_change(col):
    for i in range(1,len(df)+1):
        #print(i)
        if df.loc[i, col] is not None:
            if ',' in df.loc[i, col]:
                df.loc[i, col] = int(df.loc[i, col].replace(',',''))
            elif df.loc[i, col] == '':
                df.loc[i, col] = 0
            else:
                df.loc[i, col] = int(df.loc[i, col])

type_change('주간')
type_change('야간')
type_change('정상')

df['yyyy_mm'] = pd.to_datetime(df['작업일자']).dt.strftime('%Y-%m') #월

## 날짜별 작업구분별
df2 = df.loc[:,['작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','작업구분']).sum()


worker_name = ['전체'] + [x for x in list(df.loc[:,'담당자명'].drop_duplicates()) if x not in ['강민지','한혜림',None]]
work_day = ['전체'] + list(df.loc[:,'yyyy_mm'].drop_duplicates())
##

# 사이드바에 select box를 활용하여 종을 선택한 다음 그에 해당하는 행만 추출하여 데이터프레임을 만들고자합니다.
st.sidebar.title('작업량 관리🌸')

# select 변수에 사용자가 선택한 값이 지정됩니다
select_worker = st.sidebar.selectbox(
    '확인하고 싶은 작업자를 선택하세요',
    worker_name
)
select_work_day = st.sidebar.selectbox(
    '확인하고 싶은 날짜를 선택하세요',
    work_day
)

# 원래 dataframe으로 부터 선택한 종류들만 필터링 되어서 나오게 일시적인 dataframe을 생성합니다

if select_work_day == '전체':
    if select_worker == '전체':
        df3 = df.loc[:,['담당자명','작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','담당자명','작업구분']).sum()
        st.table(df3)
    else:
        df4 = df.loc[df.담당자명 == select_worker,['작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','작업구분']).sum()
        st.table(df4)

else:
    if select_worker == '전체':
        df3_d = df.loc[df.yyyy_mm == select_work_day,['담당자명','작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','담당자명','작업구분']).sum()
        st.table(df3_d)
        
    else:
       df4_d = df.loc[(df.담당자명 == select_worker) & (df.yyyy_mm == select_work_day),['작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','작업구분']).sum()
       st.table(df4_d)

# st.title('월별 작업자별')
# st.write(df2)

# st.write(df3)