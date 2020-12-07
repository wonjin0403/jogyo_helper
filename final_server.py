#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
from threading import Thread, Lock
import time
import datetime
import threading
import os

lock = Lock()
HOST = '10.16.129.164' 
PORT = 35357
num = 5 #학생명수
subject = '시험과목명' #시험과목명 지정
clients = {}
clients_num = {}
cnt = [[0]*4 ]*30 #오류별로 칸운트
def handle_recive(client_socket, addr, user, warning_path):
    client_socket.sendall('HELLO CLIENT {name}'.format(name = user).encode('ascii'))   
    os.chdir(warning_path) # 폴도로 이동  
    while True:
        data = client_socket.recv(1024) #경고 종류 입력 받기
        time = datetime.datetime.now()
        string = data.decode('ascii') #시간, 여러 경고가 겹쳐서 나올때
        if(string != 'e'):
            cnt[clients_num[user]][3]+= 1
            if(string == 'c'): #case1
                cnt[clients_num[user]][0] += 1
                print('time : {t}, {U} : {check}, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total = {n} \n'.format(t = time, U = user, check = '응시자 이외의 인원이 감지되었습니다.',case1 = cnt[clients_num[user]][0], case2 = cnt[clients_num[user]][2], sou_detection = cnt[clients_num[user]][1], n = cnt[clients_num[user]][3]))
                os.chdir(warning_path) # 폴도로 이동  
                file = open("total_warning_log.txt", "a")
                file.write('time : {t}, {U} : {check}, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total = {n} \n'.format(t = time, U = user, check = '응시자 이외의 인원이 감지되었습니다.',case1 = cnt[clients_num[user]][0], case2 = cnt[clients_num[user]][2], sou_detection = cnt[clients_num[user]][1], n = cnt[clients_num[user]][3]))
                file.close()    
            elif(string == 's'):
                cnt[clients_num[user]][1] += 1
                print('time : {t}, {U} : {check}, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total = {n} \n'.format(t = time, U = user, check = '소리감지',case1 = cnt[clients_num[user]][0], sou_detection = cnt[clients_num[user]][1], case2 = cnt[clients_num[user]][2],  n = cnt[clients_num[user]][3]))
                os.chdir(warning_path) # 폴도로 이동  
                file = open("total_warning_log.txt", "a")
                file.write('time : {t}, {U} : {check}, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total = {n} \n'.format(t = time, U = user, check = '소리감지',case1 = cnt[clients_num[user]][0], sou_detection = cnt[clients_num[user]][1], case2 = cnt[clients_num[user]][2],  n = cnt[clients_num[user]][3]))
                file.close()    
            elif string == 'f': 
                cnt[clients_num[user]][2]+= 1
                print('time : {t}, {U} : {check}, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total = {n} \n'.format(t = time, U = user, check = '응시자가 사라졌습니다.',
                                                                                       case1 = cnt[clients_num[user]][0], case2 = cnt[clients_num[user]][2], sou_detection = cnt[clients_num[user]][1], n = cnt[clients_num[user]][3]))
                os.chdir(warning_path) # 폴도로 이동  
                file = open("total_warning_log.txt", "a")
                file.write('time : {t}, {U} : {check}, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total = {n} \n'.format(t = time, U = user, check = '응시자가 사라졌습니다.',
                                                                                       case1 = cnt[clients_num[user]][0], case2 = cnt[clients_num[user]][2], sou_detection = cnt[clients_num[user]][1], n = cnt[clients_num[user]][3]))
                file.close()
                    
        elif(string == 'e'):
            print("{U} 시험종료".format(U=user))
            os.chdir(warning_path) # 폴도로 이동  
            file = open("total_warning_log.txt", "a")
            file.write('시험종료, case1_total : {case1}, case2_total : {case2}, 소리감지_total : {sou_detection}, total : {Total}'.format(case1 = cnt[clients_num[user]][0], sou_detection = cnt[clients_num[user]][1], case2 = cnt[clients_num[user]][2], Total = cnt[clients_num[user]][3]))
            file.close()
            break

    del clients[user]
    client_socket.close()


    
def run_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        #s.setblocking(1)
        global clients, num
        num = 0
        
        while True:
            s.listen(num)
            client_socket, addr = s.accept() 
            user = client_socket.recv(1024) #학번 입력 받기
            user = user.decode('ascii')
            
            lock.acquire()
            #학번으로 폴더 생성
            try:
                if not(os.path.isdir(user)): 
                    st_path = os.path.join(path, user)
                    os.mkdir(st_path)
                    os.chdir(st_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print('File already exists')
                        
            clients[user]=client_socket
            clients_num[user] = num # 학번별로 인덱스 생성
            num+=1 # 학번별로 인덱스 생성
            lock.release()
            
            st_path = os.getcwd()
            print(datetime.datetime.now(), '{name} Connected'.format(name = user))
            warning_path = os.path.join(st_path, 'Warning_log')
            os.mkdir(warning_path) # 폴더 생성
            receive_thread = Thread(target=handle_recive, args=(client_socket, addr, user, warning_path))
            receive_thread.daemon = True
            receive_thread.start()
            
global path
path = os.path.join(os.getcwd(), subject)
os.mkdir(path) #시험과목명으로 폴더 생성
os.chdir(path) #생성한 폴더로 이동
socket_thread = Thread(target=run_socket)
socket_thread.start()

socket_thread.join()


# In[ ]:




