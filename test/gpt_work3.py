import streamlit as st
import os
import pandas as pd
import gspread
import psycopg2

st.sidebar.title('LLM 기반 AI학습용 데이터셋 구축 툴🌸')

menu = ['Token Positive 선별 작업 (전체)', 'Token Positive 선별 작업 (문장)','Token Positive 검수'] #,'작업한 내용 확인 및 수정 (전체)'
choice = st.sidebar.selectbox('작업', menu)

## db 연결
db = psycopg2.connect(host='localhost', dbname='fire_save',user='postgres',password=1234,port=5433)
cursor=db.cursor()


if choice == menu[0] :
    # get_all_values() 함수를 이용해 코드를 실행하면 리스트 형태의 값이 리턴됩니다.
    sheet_name = st.selectbox('시트명을 선택해주세요',
                            ('whitegray_1','whitegray_2','그 외'))
    
    method = st.selectbox('방법을 선택해주세요',
                            ('수동','자동'))
    
    if sheet_name == '그 외':
        sheet_name = st.text_input('시트명을 입력해주세요',
                                'whitegray_1')
        
    st.write('---------------------')

    ## db 데이터 불러오기
    cursor.execute(f"select * from {sheet_name}")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['id','folder_name', 'image_name', 'result_text', 'convert_text','tokens_positive_no'])
        
    work_range = st.selectbox('작업범위를 설정해주세요',
                            ('시작구간 선택 (200개 단위)','범위 선택')) # 전체

    if work_range == '시작구간 선택 (200개 단위)':
        min_number = st.number_input(
        f'시작하고자 하는 데이터가 있는 엑셀의 행을 입력하세요 (1-{len(df)-200})',
        min_value=1, max_value=len(df)+1, value=1, step=1)

        try:
            df = df.sort_values('id')
            df = df[min_number-1:min_number+199]

        except:
            st.error(f"작업을 시작하지않은 데이터가 포함되어있습니다. 작업 완료 또는 '범위선택'을 이용하여 작업해주세요.")
            df = df[:0]
        


    elif work_range == '범위 선택':
        # min~max value:입력 허용구간, value:최초 입력 값, step:증분 값
        min_number = st.number_input(
        f'숫자를 입력하세요(1-{len(df)+1})',
        min_value=1, max_value=len(df)+1, value=1, step=1)

        max_number = st.number_input(
        f'숫자를 입력하세요({min_number}-{len(df)+1})',
        min_value=min_number, max_value=len(df)+1, value=200, step=1)

        df = df[min_number-1:max_number]
    
    st.write('---------------------')
    

    text_col = list(df.columns).index('convert_text')

    # 'token' 열 추가
    token_col = text_col + 1

    row = 0
    count = 0
    count2 = 1

    while row < df.shape[0]:

        # 문장 가져오기
        text = df.iloc[row, text_col]

        if text == None:
            # 선택한 인덱스를 'token' 열에 저장
            token_value = ''
            df.iloc[row, token_col] = token_value
        
        else:
            words = text.split()        
            num = row+min_number
            st.info(f'{num}. {text}')

            #print(words)
            selected_words = st.multiselect('연관있는 단어를 모두 선택하세요.',
                                            words,
                                            key = count) 
            
            # 선택한 단어의 인덱스 출력
            if selected_words:
                selected_indices = [str(words.index(word)) for word in selected_words]
                print(selected_indices)
                test = sorted(map(int, selected_indices))
                test = [str (i) for i in test]

                st.text(f"선택한 단어: {', '.join(selected_words)}")
                st.text(f"해당 인덱스: {', '.join(test)}")

                # 선택한 인덱스를 'token' 열에 저장
                token_value = ', '.join(test)
                df.iloc[row, token_col] = token_value

                if method == '수동':
                    if st.button('입력',key = 'n' + str(count2)):
                        cursor.execute(f" UPDATE {sheet_name} SET tokens_positive_no='"+token_value.strip()+f"' WHERE id={num}")
                        db.commit()
                
                elif method == '자동':
                    cursor.execute(f" UPDATE {sheet_name} SET tokens_positive_no='"+token_value.strip()+f"' WHERE id={num}")
                    db.commit()
                

            else:   
                st.text("단어를 선택하지 않았습니다.")

        row += 1
        count += 1
        count2 += 1
        
    st.write('---------------------')
    st.write('결과')
    st.dataframe(df)



elif choice == menu[1]:
    text = st.text_input('문장을 입력해주세요',
                                   'Always fighting')

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

    ## db 데이터 불러오기
    cursor.execute(f"select * from {sheet_name}")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=['id','folder_name', 'image_name', 'result_text', 'convert_text','tokens_positive_no'])
        
    work_range = st.selectbox('작업범위를 설정해주세요',
                            ('시작구간 선택 (200개 단위)','범위 선택')) # 전체

    if work_range == '시작구간 선택 (200개 단위)':
        min_number = st.number_input(
        f'시작하고자 하는 데이터가 있는 엑셀의 행을 입력하세요 (1-{len(df)-200})',
        min_value=1, max_value=len(df)+1, value=1, step=1)

        try:
            df = df.sort_values('id')
            df = df[min_number-1:min_number+199]

        except:
            st.error(f"작업을 시작하지않은 데이터가 포함되어있습니다. 작업 완료 또는 '범위선택'을 이용하여 작업해주세요.")
            df = df[:0]
        


    elif work_range == '범위 선택':
        # min~max value:입력 허용구간, value:최초 입력 값, step:증분 값
        min_number = st.number_input(
        f'숫자를 입력하세요(1-{len(df)+1})',
        min_value=1, max_value=len(df)+1, value=1, step=1)

        max_number = st.number_input(
        f'숫자를 입력하세요({min_number}-{len(df)+1})',
        min_value=min_number, max_value=len(df)+1, value=200, step=1)

        df = df[min_number-1:max_number]
    
    st.write('---------------------')
    

    text_col = list(df.columns).index('convert_text')
    index_col = list(df.columns).index('tokens_positive_no')

    # 'token' 열 추가
    token_col = df.shape[1]
    
    df['token'] = ''

    row = 0
    
    while row < df.shape[0]:
        try:
            # 문장 가져오기
            text = df.iloc[row, text_col]
            index_no = df.iloc[row, index_col]


            # 문장을 띄어쓰기 단위로 나누기
            if text is not None:
                words = text.split()
                index_num = index_no.split(',')
                word = [] 

                for no in index_num:
                    #print(text, index_num, no)
                    
                    if no is not '' and no is not ' ':
                        word.append(words[int(no)])
                    
                st.info(f'{row+min_number}. {text}')
                st.text(f"선택한 단어: {', '.join(word)}")
                st.text(f"해당 인덱스: {', '.join(index_num)}")

                selected_words = st.multiselect('수정을 원하시는 경우 단어를 재선택하세요.',
                                                        words)
                
                if selected_words:
                    selected_indices2 = [str(words.index(word)) for word in selected_words]
                    print(selected_indices2)
                    test = sorted(map(int, selected_indices2))
                    test = [str (i) for i in test]

                    token_value2 = ', '.join(test)

                    st.text(f"재선택한 단어: {', '.join(selected_words)}")
                    st.text(f"해당 인덱스: {', '.join(test)}")

                    word = selected_words
                    df.iloc[row, index_col] = token_value2



                    if st.button('수정',key = 'n' + str(row)):
                        cursor.execute(f" UPDATE {sheet_name} SET tokens_positive_no='"+token_value2.strip()+f"' WHERE id={row+min_number}")
                        db.commit()
                    

                       
                else:   
                    st.text("단어를 선택하지 않았습니다.")

                    
                # 선택한 인덱스를 'token' 열에 저장
                token_value = ', '.join(word)
                df.iloc[row, token_col] = token_value
                
        
        except:
            st.error(f'{row+min_number}. {text}')

            if index_no is None:
                st.write('토큰 선택 작업을 수행하지 않았습니다.')
            
            else:
                st.write('범위에 오류가 있습니다.')
                st.text(f"선택 인덱스: {', '.join(index_num)}")
                st.text(f"해당 문장 범위 : 0 ~ {len(words)-1}")
            
        row += 1
            
    st.write('---------------------')
    st.write('결과')
    st.dataframe(df)
