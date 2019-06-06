'''
    프로세스 데이터 뽑기 관련
    참고 링크 : https://thispointer.com/python-check-if-a-process-is-running-by-name-and-find-its-process-id-pid/
'''

import os
import psutil
import time

'''
    OS의 실행중인 프로세스를 출력함.
    현재 실행중인 모든 프로세스를 출력. PID번호 포함 
'''
proc_iter = psutil.process_iter()
for i in proc_iter:
    print(i)

print('\n\n\n///// 구분선 ////\n\n\n')
'''
    [프로세스명] 이름이 들어간 것을 골라서 출력함.
    python3 라는 프로세스만 골라서 출력함. PID번호 포함
'''
PROCNAME = "chrome.exe"     # 윈도 테스트
#PROCNAME = "python3"       # 리눅스 테스트

for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        print(proc)
    else:
        pass

print('\n\n\n///// 구분선 ////\n\n\n')
'''
    [프로세스명]이 포함되어있는 것이 실행되고 있는지 아닌지 확인 함수.
    param : Process Name
    return: 실행중이면 True, 실행중이지 않으면 False
'''
def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
# 함수 테스트
name = 'chrome'    # 찾을 프로세스 이름.
if checkIfProcessRunning( name ):
    print("%s 진행중" %name)
else:
    print("%s 은 없다." %name)


print('\n\n\n///// 구분선 ////\n\n\n')
'''
    [Process 명]으로 PID 번호, 이름, 발생시간 찾기.
    param : Process Name
    return: 딕셔너리형태 리스트로 출력. pid, ProcessName, 발생시간 데이터를 갖고있음.
'''
def findProcessIDByName(processName):
    listOfProcessObjects = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if processName.lower() in pinfo['name'].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return listOfProcessObjects

# 함수 테스트
listOfProcessIds = findProcessIDByName(name)
print(listOfProcessIds[0]['pid'])               # 정보 한개씩 프린트 테스트
print(listOfProcessIds[0]['name'])

# 프로레스명에 관한 데이터 모두 출력               # 정보 모두 출력 Tuple type으로 출력
if len(listOfProcessIds) > 0:
    print("Existing Process information")
    for elem in listOfProcessIds:
        processID = elem['pid']
        processName = elem['name']
        processCreationTime = time.strftime('%Y-%M-%d %H:%M:%S', time.localtime(elem['create_time']))
        print((processID, processName, processCreationTime))
else:
    print("No Running Process found with given Text")

# 프로레스명에 관한 데이터 모두 출력               # 정보 모두 출력 (간단히) data type으로 출력
procObjList = [procObj for procObj in psutil.process_iter() if 'chrome' in procObj.name().lower()]
for elem in procObjList:
    print(elem)