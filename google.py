import streamlit as st
import pandas as pd

#st.title('Hello World!')

## 구글 연결
import gspread

# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "cryptic-honor-351410-5c57b4413112.json"
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
st.sidebar.title('AI Hub 작업량 관리🌸')

select_work = st.sidebar.selectbox(
    '작업 선택',
    ['전체 진행률 확인','작업자 확인'])

if select_work == '전체 진행률 확인':
    
    ### NAS 데이터 기준
    cctv = pd.read_csv('cctv_save.csv')
    drone = pd.read_csv('drone_save.csv')
    drone_etc = pd.read_csv('drone_etc_save.csv')

    upload_data = pd.read_csv('upload_data.csv')

    # 데이터프레임 결합
    merged_df = pd.concat([cctv, drone,drone_etc])
    # 같은 행 값 합치기
    final_df = merged_df.groupby(['folder', 'kind'])[['day','night','etc']].sum().reset_index()

    save_data = pd.DataFrame(columns=['folder','kind','save'])
    save_data['folder'] = list(final_df['folder'])
    save_data['kind'] = list(final_df['kind'])
    save_data['save'] = list(final_df[['day','night','etc']].sum(axis=1))


    ## Google Sheet
    dataa = df[df['최상위폴더명'] == 'aihub']
    dataa = dataa.fillna(0)

    google_sheet_cctv = pd.DataFrame(columns=['folder','kind','day','night','etc'])
    google_sheet_drone = pd.DataFrame(columns=['folder','kind','day','night','etc'])
    google_sheet_drone_etc = pd.DataFrame(columns=['folder','kind','day','night','etc'])

    dataa_cctv = dataa[dataa['촬영도구'] == '일반카메라']
    dataa_drone = dataa[dataa['촬영도구'] == '드론']
    dataa_drone_etc = dataa[dataa['촬영도구'] == '드론-기타']

    google_sheet_cctv ['folder'] = dataa_cctv['하위폴더명']
    google_sheet_cctv ['kind'] = dataa_cctv['상위폴더명'].str.split('-').str[0]
    google_sheet_cctv ['day'] = dataa_cctv['주간']
    google_sheet_cctv ['night'] = dataa_cctv['야간']
    google_sheet_cctv ['etc'] = dataa_cctv['etc']
    
    google_sheet_drone ['folder'] = dataa_drone['하위폴더명']
    google_sheet_drone ['kind'] = dataa_drone['상위폴더명'].str.split('-').str[0]
    google_sheet_drone ['day'] = dataa_drone['주간']
    google_sheet_drone ['night'] = dataa_drone['야간']
    google_sheet_drone ['etc'] = dataa_drone['etc']

    google_sheet_drone_etc ['folder'] = dataa_drone_etc['하위폴더명']
    google_sheet_drone_etc ['kind'] = dataa_drone_etc['상위폴더명'].str.split('-').str[0]
    google_sheet_drone_etc ['day'] = dataa_drone_etc['주간']
    google_sheet_drone_etc ['night'] = dataa_drone_etc['야간']
    google_sheet_drone_etc ['etc'] = dataa_drone_etc['etc']

    # 데이터프레임 결합
    merged_df2 = pd.concat([google_sheet_cctv, google_sheet_drone,google_sheet_drone_etc])

    int_col = ['day', 'night', 'etc']

    for ic in int_col:
        if merged_df2[ic].dtypes == 'object':
            merged_df2[ic] = merged_df2[ic].str.replace(',', '').fillna(0).astype(int)

    # 같은 행 값 합치기
    final_df2 = merged_df.groupby(['folder', 'kind'])[['day','night','etc']].sum().reset_index()

    google_work_data = pd.DataFrame(columns=['folder','kind','work'])
    google_work_data['folder'] = list(final_df2['folder'])
    google_work_data['kind'] = list(final_df2['kind'])
    google_work_data['work'] = list(final_df2[['day','night','etc']].sum(axis=1))

    work_data = upload_data.merge(save_data)
    work_folder = pd.merge(upload_data,save_data, how='outer', indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
    final_work = work_data.merge(google_work_data)

    ## 작업자 & 시간
    worker_data = pd.DataFrame(columns=['folder','kind','last_worker','start', 'last'])

    for n in range(0, len(final_work)):
        f = final_work.loc[n,'folder']
        t = final_work.loc[n,'kind']
        name = list(set(dataa[(dataa['상위폴더명'] == f'{t}-images') & (dataa['하위폴더명'] == f)]['담당자명']))
        day = list(dataa[(dataa['상위폴더명'] == f'{t}-images') & (dataa['하위폴더명'] == f)]['작업일자'])
        worker_data.loc[n] = [f,t,name[-1],day[0],day[-1]]
    
    #final_work['check_work'] = ['일치' if final_work['save'][i] == final_work['work'][i] else '확인필요' for i in range(len(final_work))]
    
    final_work['status'] = ['완료' if final_work['img'][i] == final_work['save'][i] else '-' for i in range(len(final_work))]

    st.text('전체 작업')
    st.dataframe(final_work)

    st.text('작업자')
    st.dataframe(worker_data.sort_values('last'))

    st.text('남은 폴더')
    st.dataframe(work_folder)

    
elif select_work == '작업자 확인':
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
            st.header('월별 작업량1')
            st.dataframe(df3)
            a = df.loc[:,['작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','작업구분']).sum()
            st.header('월별 작업량2')
            st.dataframe(a.sum(axis=1))
        else:
            df4 = df.loc[df.담당자명 == select_worker,['작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','작업구분']).sum()
            st.dataframe(df4)

    else:
        if select_worker == '전체':
            df3_d = df.loc[df.yyyy_mm == select_work_day,['담당자명','작업구분','주간','야간','정상','yyyy_mm']].groupby(['yyyy_mm','담당자명','작업구분']).sum()
            st.dataframe(df3_d)

            new_df = df.loc[df.yyyy_mm == select_work_day,['담당자명','작업구분','주간','야간','정상','작업일자']]  # filtered_df의 복사본 생성
            new_df['down_at'] = pd.to_datetime(new_df['작업일자'], format='%Y-%m-%d')
            new_df['week_start'] = new_df['down_at'] - pd.to_timedelta(new_df['down_at'].dt.dayofweek, unit='d')
            weekly_df = new_df.groupby(['작업구분', 'week_start'])[['주간','야간','정상']].sum().reset_index() # video_id 와 week_start 가 index로 가버리기 때문에 rest_index() 필요

            st.dataframe(weekly_df)  
            
        else:
            df4_d = df.loc[(df.담당자명 == select_worker) & (df.yyyy_mm == select_work_day),['최상위폴더명','상위폴더명','하위폴더명','작업일자','작업구분','주간','야간','정상']]
            st.dataframe(df4_d)

            # filtered_df  데이터
            import datetime
            import pandas as pd

            new_df = df4_d.copy()  # filtered_df의 복사본 생성
            new_df['down_at'] = pd.to_datetime(df4_d['작업일자'], format='%Y-%m-%d')
            new_df['week_start'] = new_df['down_at'] - pd.to_timedelta(new_df['down_at'].dt.dayofweek, unit='d')
            weekly_df = new_df.groupby(['작업구분', 'week_start'])[['주간','야간','정상']].sum().reset_index() # video_id 와 week_start 가 index로 가버리기 때문에 rest_index() 필요

            st.dataframe(weekly_df)  

