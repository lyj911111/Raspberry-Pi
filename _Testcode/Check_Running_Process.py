import os
import psutil

'''
    OS의 실행중인 프로세스를 출력함.
    현재 실행중인 모든 프로세스를 출력. PID번호 포함 
'''
proc_iter = psutil.process_iter()
for i in proc_iter:
    print(i)


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
# 함수테스트
name = 'pycharm'    # 찾을 프로세스 이름.
if checkIfProcessRunning( name ):
    print("%s 진행중" %name)
else:
    print("%s 은 없다." %name)


