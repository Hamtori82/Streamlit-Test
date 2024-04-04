import os
import traceback
original_working_directory = os.getcwd()

## 로컬PC 경로
org = original_working_directory
def local_pc(org):
    os.chdir(org)

## 네트워크 폴더로 이동
def net_pc(route):
    #new_networked_directory = r'\\server\share\folder'
    #os.chdir(new_networked_directory)
    
    os.chdir(route)

## txt 폴더
def find_folders_with_txt(top_folder):
    net_pc(r'\\192.168.10.100\label\wildfire\labeling_workspace\save')
    folders_with_txt = []
    for root, dirs, files in os.walk(top_folder):
        for file in files:
            if file.endswith('.txt'):
                folders_with_txt.append(root)
                break  # 현재 폴더에 PNG 파일이 하나라도 있으면 추가 후 다음 폴더로 넘어감
    return folders_with_txt


## 라벨링 파일과 원천데이터 파일 비교
def folder_test(top_folder, folders1):

    net_pc(r'\\192.168.10.100\label\wildfire\labeling_workspace')

    t_n, s_n, f_n, f1_n = 0,0,0,0
    uf1 = []
    uf2 = []
    ufp = []

    for folder in folders1:
        folder_name = '/'.join(folder.split('\\')[2:])

        #print(folder_name)
        ## txt 
        txt_file_lst = os.listdir(f'./save/{folder}')
        ## img
        img_path = f"./upload/{top_folder}/{folder_name}"
        img_file_lst = os.listdir(img_path)
        
        file_lst_txt = [file for file in txt_file_lst if file.endswith(".txt")] 
        file_lst_img = [file for file in img_file_lst if file.endswith(".jpg") or file.endswith(".png")]
        
        txt_list = [word.strip('.txt') for word in file_lst_txt ]
        jpg_list = [word.strip('.jpg') for word in file_lst_img ]
        png_list = [word.strip('.png') for word in file_lst_img ]

        t_n += len(txt_list)
        f_n += 1
        
        unique_files1 = set(txt_list) - set(jpg_list) - set(png_list) 
        
        if len(unique_files1) > 0: 
            ufp.append(folder.split('\\')[1:])
            uf2.append(unique_files1)
            s_n += (len(txt_list) - len(unique_files1))
        else:
            s_n += len(txt_list)
            f1_n += 1

    print(f'<{top_folder} 폴더 데이터셋 속성 일치성 검사결과>\n') 
    print(f'1. 폴더 : {f1_n}/{f_n} ({round((f1_n/f_n)*100,2)}%)')
    print(f'2. 파일 : {s_n}/{t_n} ({round((s_n/t_n)*100,2)}%)')

    result_1 = f'<{top_folder} 폴더 데이터셋 속성 일치성 검사결과>\n' 
    result_2 = f'1. 폴더 : {f1_n}/{f_n} ({round((f1_n/f_n)*100,2)}%)'
    result_3 = f'2. 파일 : {s_n}/{t_n} ({round((s_n/t_n)*100,2)}%)'

    #result_1 = f"<{top_folder} 폴더 데이터셋 속성 일치성 검사결과>\n 1. 폴더 : {f1_n}/{f_n} ({round((f1_n/f_n)*100,2)}%) \n 2. 파일 : {s_n}/{t_n} ({round((s_n/t_n)*100,2)}%)"

    st.header(result_1)

    st.info(f'''
    {result_2}

    {result_3}
    ''')

    if t_n == s_n:    
        print('\n※ 라벨링데이터 파일명과 원천데이터파일명이 모두 일치합니다.')
        f'\n※ 라벨링데이터 파일명과 원천데이터파일명이 모두 일치합니다.'
    else:
        error_folder(ufp, uf2, top_folder)
    
    
    
## img 폴더
def find_folders_with_img(top_folder):
    net_pc(r'\\192.168.10.100\label\wildfire\labeling_workspace\upload')
    folders_with_img = []
    for root, dirs, files in os.walk(top_folder):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                folders_with_img.append(root)
                break  # 현재 폴더에 PNG 파일이 하나라도 있으면 추가 후 다음 폴더로 넘어감
    return folders_with_img




## 경로 이상 파일의 원래 위치 찾기
def error_folder(ufp, uf2, top_folder):
    
    folders2 = find_folders_with_img(top_folder)

    tt = []

    for u in ufp:
        ufp_name = '/'.join(u)

    rt1 = ""
    
    print('\n<오류데이터 내역> \n')
    st.subheader(f'<오류데이터 내역>')

    for folder in folders2:    
        ## img
        img_file_lst = os.listdir(folder)

        file_lst_img = [file for file in img_file_lst if file.endswith(".jpg") or file.endswith(".png")]
        
        if file_lst_img[0].endswith(".jpg"):
            img_list = [word.strip('.jpg')  for word in file_lst_img ]
        else:
            img_list = [word.strip('.png')  for word in file_lst_img ]

        for i in uf2:
            for f in list(i):
                if f in img_list:
                    tx = f'"{f}"과 동일한 이름을 가진 이미지가 {folder}폴더에 존재합니다.'
                    if tx not in tt:
                        print(f'1. 오류데이터명 : {f}.txt')
                        print(f'2. 오류데이터 저장위치 : /save/{top_folder}/{ufp_name}')
                        print(f'3. 해당 오류데이터와 세트인 원천데이터 저장위치 : upload/{folder}')
                        print('\n')
                        #print(tx)
                        tt.append(tx)

                        rt1 += f'● 오류데이터명 : {f}.txt\n'
                        rt1 += '\n'
                        rt1 += f'○ 오류데이터 저장위치 : /save/{top_folder}/{ufp[0]}\n'
                        rt1 += '\n'
                        rt1 += f'○ 해당 오류데이터와 세트인 원천데이터 저장위치 : upload/{folder}\n'
                        rt1 += '\n'
    print(rt1)
    st.error(rt1)

## 경로지정
net_pc(r'\\192.168.10.100\label\wildfire\labeling_workspace')

## top_folder명
folder_list = []
folder_rute = os.listdir('./upload/')
for i in range(0,len(folder_rute)):
    folder_list.append(f'{i} : {folder_rute[i]}')

import streamlit as st

option = st.selectbox(
    '폴더를 선정해주세요',
    folder_list)

st.write('You selected:', option)

#folder_num = input(f'폴더를 선정해주세요 : {folder_list}')
top_folder = folder_rute[int(option[0])]

folders1 = find_folders_with_txt(top_folder)
folder_test(top_folder, folders1)