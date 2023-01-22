import threading, requests,json, datetime, sys
import time as t

sm = threading.Semaphore(2)
data = None
lock_data = threading.Lock()
exit = threading.Event()

def Average_temp( ):
    data = []
    with open('data.txt', 'r') as f:
        data = f.readlines()
    count = len(data)
    if count >= 6:
        data = data[-1:-7:-1]
    elif count > 0:
        data = data[-1, -count-1, -1]
    data = data.map(lambda x: int(x), data)
    return sum(data) / count

def task1():
    global exit
    while True:
        choise1 = input("Что вы хотите узнать? Температура/Влажность(T), Счетчики(S), Котел(K), Журнал(M), Выход(E)")
        match choise1.lower():
            case "t":
                chois2 = input("Что вы хотите узнать в температуре? Текущая температура/влажность(N), Средняя температура/влажность(A), Bозврат на прошлую страницу(B)")
                match chois2.lower():
                    case "n":
                        lock_data.acquire()
                        temp = data["temperature"]
                        humidity = data["humidity"]
                        print(f"Текущая температура: {temp} ℃, текущая влажность: {humidity}")
                        lock_data.release()
                    case "a":
                        print(Average_temp())
                    case "b":
                        task1()

            case "s":
                chois3 = input("Что вы хотите узнать в счетчике? Электроенергия(E), Газ(G), Вода(W), Bозврат на прошлую страницу(B)")
                match chois3.lower():
                    case "e":
                        lock_data.acquire()
                        electricity = data["meter"]["electricity"]["consumption"]
                        print(f"споживання електроенергії: {electricity} Кв")
                        lock_data.release()
                    case "g":
                        lock_data.acquire()
                        gas = data["meter"]["gas"]["consumption"]
                        print(f"споживання електроенергії: {gas} м3")
                        lock_data.release()
                    case "w":
                        lock_data.acquire()
                        water = data["meter"]["water"]["consumption"]
                        print(f"споживання електроенергії: {water} м3")
                        lock_data.release()
                    case "b":
                        task1()
            case "k":
                chois4 = input("Что вы хотите узнать или сделать в котле? Состояние(C), Включить(P), Выключить(U), Bозврат на прошлую страницу(B)")
                match chois4.lower():
                    case "c":
                        lock_data.acquire()
                        boiler_temp = data['boiler']["temperature"]
                        boiler_pres = data['boiler']["pressure"]
                        print(f"Теспература в бойлере: {boiler_temp} ℃, давление в боллере {boiler_pres}")
                        lock_data.release()
                    case "p":
                        lock_data.acquire()
                        if data['boiler']['isRun'] == False:
                            data['boiler']['isRun'] = True
                        print("Болер включён!")
                        lock_data.release()
                    case "u":
                        lock_data.acquire()
                        if data['boiler']['isRun'] == True:
                            data['boiler']['isRun'] = False
                        print("Болер выключен!")
                        lock_data.release()
                    case "b":
                        task1()
            case "m":
                lock_data.acquire()
                print(data)
                lock_data.release()
            case "e":
                exit.set()
                sys.exit()


def task2( ):
    while True:
        if exit.is_set():
            return
        global data
        response = requests.get("http://localhost:8000/cgi-bin/exemple_json.py")
        lock_data.acquire()
        data = json.loads(response.text)
        time = str(datetime.datetime.now())
        with open("data.txt", "a")as file:
            file.write(str(data) + "\n")
        lock_data.release()
        t.sleep(5)


th1 = threading.Thread(target=task1)
th2 = threading.Thread(target=task2, daemon=True)


th1.start()
th2.start()

# timer = threading.Timer(5, task2)
# timer.start()

th2.join()
th1.join()

