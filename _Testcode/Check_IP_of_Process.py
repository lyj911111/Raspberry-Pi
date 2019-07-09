'''
    참고 링크: https://pydole.tistory.com/40

    프로세스 이름, 상태, 원격IP주소, Port번호 출력
'''

import psutil

for value in psutil.net_connections():
    try:
        if value.raddr[0] != '127.0.0.1':
            print(psutil.Process(value.pid).name(), value.status, value.raddr[0], value.raddr[1])
    except:
        pass