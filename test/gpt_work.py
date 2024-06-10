# import streamlit as st

# import pandas as pd

# from datetime import datetime

# import os # 경로 탐색

# # 파일 업로드 함수
# # 디렉토리 이름, 파일을 주면 해당 디렉토리에 파일을 저장해주는 함수
# def save_uploaded_file(directory, file):
#     # 1. 저장할 디렉토리(폴더) 있는지 확인
#     #   없다면 디렉토리를 먼저 만든다.
#     if not os.path.exists(directory):
#         os.makedirs(directory)
    
#     # 2. 디렉토리가 있으니, 파일 저장
#     with open(os.path.join(directory, file.name), 'wb') as f:
#         f.write(file.getbuffer())
#     return st.success('파일 업로드 성공!')



# # 기본 형식
# def main():
#     st.title('앱 데시보드')

#     menu = ['이미지 업로드', 'csv 업로드', 'About', 'xlsx 업로드']

#     choice = st.sidebar.selectbox('메뉴', menu)
    
#     if choice == menu[0]:
#         st.subheader('이미지 파일 업로드')
#         img_file = st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
#         if img_file is not None: # 파일이 없는 경우는 실행 하지 않음
#             print(type(img_file))
#             print(img_file.name)
#             print(img_file.size)
#             print(img_file.type)

#             # 유저가 올린 파일을,
#             # 서버에서 처리하기 위해서(유니크하게) 
#             # 파일명을 현재 시간 조합으로 만든다. 
#             current_time = datetime.now()
#             print(current_time)
#             print(current_time.isoformat().replace(':', "_") + '.jpg') #문자열로 만들어 달라
#             # 파일 명에 특정 특수문자가 들어가면 만들수 없다.
#             filename = current_time.isoformat().replace(':', "_") + '.jpg'
#             img_file.name = filename

#             save_uploaded_file('image', img_file)

#             st.image(f'image/{img_file.name}')


#     elif choice == menu[1]:
#         st.subheader('csv 파일 업로드 ')

#         csv_file = st.file_uploader('CSV 파일 업로드', type=['csv'])

#         print(csv_file)
#         if csv_file is not None:
#             current_time = datetime.now()
#             filename = current_time.isoformat().replace(':', '_') + '.csv'

#             csv_file.name = filename

#             save_uploaded_file('csv', csv_file)

#             # csv를 보여주기 위해 pandas 데이터 프레임으로 만들어야한다.
#             df = pd.read_csv('csv/'+filename,encoding = 'cp949')
#             st.dataframe(df)

#     elif choice == menu[3]:
#         st.subheader('xlsx 파일 업로드 ')

#         xlsx_file = st.file_uploader('XLSX 파일 업로드', type=['xlsx'])

#         print(xlsx_file)
#         if xlsx_file is not None:
#             current_time = datetime.now()
#             filename = current_time.isoformat().replace(':', '_') + '.xlsx'

#             xlsx_file.name = filename

#             save_uploaded_file('xlsx', xlsx_file)

#             # xlsx를 보여주기 위해 pandas 데이터 프레임으로 만들어야한다.
#             # 엑셀 파일 열기
#             workbook = openpyxl.load_workbook('xlsx/'+filename)
#             worksheet = workbook.active
            
#             st.dataframe(workbook)


#     else :
#         st.subheader('이 대시보드 설명')

# if __name__ == '__main__':
#     main()

import streamlit as st
import os
import pandas as pd
import gspread


menu = ['토큰 작업 (전체)', '토큰 작업 (문장)','작업한 내용 확인'] #,'작업한 내용 확인 및 수정 (전체)'
choice = st.sidebar.selectbox('메뉴', menu)


# json 파일이 위치한 경로를 값으로 줘야 합니다.
json_file_path = "cryptic-honor-351410-5c57b4413112.json"
gc = gspread.service_account(json_file_path)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1YW08AaIgaPL-XvDCVu76vfFTPkCAW4JM-EsEjCJy1yU/edit?usp=sharing"
doc = gc.open_by_url(spreadsheet_url)


if choice == menu[0] :

    ## get_all_values() 함수를 이용해 코드를 실행하면 리스트 형태의 값이 리턴됩니다.
    sheet_name = st.selectbox('시트명을 선택해주세요',
                              ('whitegray_1','whitegray_2','그 외'))
    
    if sheet_name == '그 외':
        sheet_name = st.text_input('시트명을 입력해주세요',
                                   'whitegray_1')
        
    st.write('---------------------')
        
    gc1 = doc.worksheet(sheet_name) ## 입력받도록!
    work_range = st.selectbox('작업범위를 설정해주세요',
                              ('시작구간 선택 (200개 단위)','범위 선택')) # 전체..
        
    gc_df = gc1.get('A2:E')
    gc3 = pd.DataFrame(gc_df, columns=gc_df[0])

    if work_range == '시작구간 선택 (200개 단위)':
        min_number = st.number_input(
		f'시작하고자 하는 데이터가 있는 엑셀의 행을 입력하세요 (3-{len(gc3)-200})',
        min_value=3, max_value=len(gc3)+1, value=3, step=1)

        try:
            gc2 = gc1.get(f'A{min_number-1}:E{min_number+201}')
            print(gc2)
            gc3 = pd.DataFrame(gc2, columns=gc_df[0])
        except:
            st.error(f"작업을 시작하지않은 데이터가 포함되어있습니다. 작업 완료 또는 '범위선택'을 이용하여 작업해주세요.")
            gc_df = gc1.get('A2:E2')
            gc3 = pd.DataFrame(gc_df, columns=gc_df[0])
        


    elif work_range == '범위 선택':
        # min~max value:입력 허용구간, value:최초 입력 값, step:증분 값
        min_number = st.number_input(
		f'숫자를 입력하세요(3-{len(gc3)+1})',
        min_value=3, max_value=len(gc3)+1, value=3, step=1)

        max_number = st.number_input(
		f'숫자를 입력하세요({min_number}-{len(gc3)+1})',
        min_value=min_number, max_value=len(gc3)+1, value=203, step=1)

        gc2 = gc1.get(f'A{min_number-1}:E{max_number}')
        gc3 = pd.DataFrame(gc2, columns=gc_df[0])
    
    st.write('---------------------')

    gc3 = gc3.reindex(gc3.index.drop(0))

    text_col = list(gc3.columns).index('Convert text')

    # 'token' 열 추가
    token_col = gc3.shape[1]
    gc3['Token positive no.'] = ''

    row = 0
    count = 0

    while row < gc3.shape[0]:

        # 문장 가져오기
        text = gc3.iloc[row, text_col]

        

        # 문장을 띄어쓰기 단위로 나누기
        #print(text, row)

        if text == None:
            #print(text, row)
            # 선택한 인덱스를 'token' 열에 저장
            token_value = ''
            gc3.iloc[row, token_col] = token_value
        
        else:
            words = text.split()

            #if work_range == '선택':
            #    id_num = min_number-2
            #    st.info(f'{row+id_num}. {text}')

            #else:
            #    st.info(f'{row+1}. {text}')
            
            num = row+min_number-2
            st.info(f'{num}. {text}')

            #print(words)
            selected_words = st.multiselect('연관있는 단어를 모두 선택하세요.',
                                            words,
                                            key = count) 
            
            # 선택한 단어의 인덱스 출력
            if selected_words:
                selected_indices = [str(words.index(word)) for word in selected_words]

                st.text(f"선택한 단어: {', '.join(selected_words)}")
                st.text(f"해당 인덱스: {', '.join(selected_indices)}")

                # 선택한 인덱스를 'token' 열에 저장
                token_value = ', '.join(selected_indices)
                gc3.iloc[row, token_col] = token_value

            else:
                st.text("단어를 선택하지 않았습니다.")

        row += 1
        count += 1
        
    st.write('---------------------')
    st.write('결과')
    st.dataframe(gc3)



elif choice == menu[1]:
    text = st.text_input('문장을 입력해주세요',
                                   'Always fighting')
    
    # # 함수형태로 번역기 형태 만들기
    # def google_trans(messages):
    #     from googletrans import Translator
        
    #     google = Translator()
    #     result = google.translate(messages, dest="ko")
        
    #     return result.text
    
    st.info(google_trans(text))

    # 문장을 띄어쓰기 단위로 나누기
    words = text.split()

    selected_words = st.multiselect('연관있는 단어를 모두 선택하세요.',
                                    words)
    
    # 선택한 단어의 인덱스 출력
    if selected_words:
        selected_indices = [str(words.index(word)) for word in selected_words]

        st.text(f"선택한 단어: {', '.join(selected_words)}")
        st.text(f"해당 인덱스: {', '.join(selected_indices)}")
    


elif choice == menu[2]:

## get_all_values() 함수를 이용해 코드를 실행하면 리스트 형태의 값이 리턴됩니다.
    sheet_name = st.selectbox('시트명을 선택해주세요',
                              ('whitegray_1','whitegray_2','그 외'))
    
    if sheet_name == '그 외':
        sheet_name = st.text_input('시트명을 입력해주세요',
                                   'whitegray_1')
        
    st.write('---------------------')
        
    gc1 = doc.worksheet(sheet_name) ## 입력받도록!
    work_range = st.selectbox('작업범위를 설정해주세요',
                              ('전체','선택'))
        
    gc_df = gc1.get('B2:F')
    gc3 = pd.DataFrame(gc_df, columns=gc_df[0])

    if work_range == '선택':
        # min~max value:입력 허용구간, value:최초 입력 값, step:증분 값
        min_number = st.number_input(
		f'숫자를 입력하세요(3-{len(gc3)+1})',
        min_value=3, max_value=len(gc3)+1, value=3, step=1)

        max_number = st.number_input(
		f'숫자를 입력하세요({min_number}-{len(gc3)+1})',
        min_value=min_number, max_value=len(gc3)+1, value=len(gc3)+1, step=1)

        gc2 = gc1.get(f'B{min_number-1}:E{max_number}')
        gc3 = pd.DataFrame(gc2, columns=gc_df[0])
    
    st.write('---------------------')

    gc3 = gc3.reindex(gc3.index.drop(0))

    text_col = list(gc3.columns).index('Convert text')
    index_col = list(gc3.columns).index('Token positive no.')

    # 'token' 열 추가
    token_col = gc3.shape[1]
    
    gc3['token'] = ''

    row = 0

    try:

        while row < gc3.shape[0]:

            # 문장 가져오기
            text = gc3.iloc[row, text_col]
            index_no = gc3.iloc[row, index_col]

            # 문장을 띄어쓰기 단위로 나누기
            if text is not None:
                words = text.split()
                index_num = index_no.split(',')

                word = [] 

                for no in index_num:
                    print(text, index_num, no)
                    if no is not '' and no is not ' ':
                        word.append(words[int(no)])

                st.info(text)
                st.text(f"선택한 단어: {', '.join(word)}")
                st.text(f"해당 인덱스: {', '.join(index_num)}")
            
                # 선택한 인덱스를 'token' 열에 저장
                token_value = ', '.join(word)
                gc3.iloc[row, token_col] = token_value


            row += 1
        
        st.write('---------------------')
        st.write('결과')
        st.dataframe(gc3)

    except: 
        st.write('범위에 오류가 있습니다.')
        st.text(f"선택 인덱스: {', '.join(index_num)}")
        st.text(f"해당 문장 범위 : 0 ~ {len(words)-1}")
        print()


# elif a == '5':

#     # 엑셀 파일 열기
#     juso = input('엑셀주소를 입력하세요 (.xlsx) :')
#     workbook = openpyxl.load_workbook(juso)
#     worksheet = workbook.active

#     # 열 제목 확인 및 위치 찾기
#     col_titles = [cell.value for cell in worksheet[1]]
#     text_col = col_titles.index('Convert text') + 1
#     index_col = col_titles.index('Token positive no.') + 1

#     # '새로운 인덱스' 열 추가
#     token_col = worksheet.max_column + 1
#     worksheet.cell(row=1, column=token_col, value='new_index')

#     # 데이터 처리
#     row = 2
#     while row < worksheet.max_row+1:
#         # 문장 가져오기
#         text = worksheet.cell(row=row, column=text_col).value
#         index_no = worksheet.cell(row=row, column=index_col).value
        
#         # 문장을 띄어쓰기 단위로 나누기
#         words = text.split()
#         index_num = index_no.split(',')
#         out_index = [x for x in  list(range(0,len(words))) if x not in [int(x) for x in index_num]]

#         word_index = []

#         print(text)

#         for no in index_num:
#             select = input(f"{words[int(no)]}이(가) 옳게 추출된 Token인가요? (옳다면 'y or 1')")
#             if select.lower() == 'y' or select == '1':
#                 word_index.append(no)
            
#             nius = len(index_num)-len(word_index)
        
#         print(f'{len(index_num)} 중에서 {nius}개 수정하였습니다.')

#         print(' '*50)

#         chuchu = input("고르지 않은 토큰 한번 더 확인해보시겠나요? (선택하려면 'y or 1')")

#         print(' '*50)

#         if chuchu.lower() == 'y' or chuchu == '1':

#             print(text)

#             for na_no in out_index:
#                 select2 = input(f"{words[int(na_no)]}을 추가할까요? (선택하려면 'y or 1')")
#                 if select2.lower() == 'y' or select2 == '1':
#                     word_index.append(str(na_no))
            
#             print(f'새로운 단어 {len(word_index)-(len(index_num)-nius)}개 추가되었습니다.')
            

            

        
#         # 선택한 인덱스를 'token' 열에 저장
#         token_value = ', '.join(word_index) #[str(x) for x in word_index] 
#         worksheet.cell(row=row, column=token_col, value=token_value)
    
#         currentCell = worksheet.cell(row=row, column=token_col)
#         currentCell.alignment = Alignment(vertical="center")

#         row += 1

#     # 엑셀 파일 저장
#     print(' '*50)
#     #file_save = input('엑셀파일로 내보내기하시겠습니까? (y or 1)')
#     #if file_save == '1' or file_save.lower() == 'y':
#     name = input('저장할 파일이름 :')
#     workbook.save(f'C:/gpt_work/{name}.xlsx')

#     print("작업이 완료되었습니다.")
