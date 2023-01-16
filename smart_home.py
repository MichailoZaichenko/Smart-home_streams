import threading, requests,json, datetime, sys
sm = threading.Semaphore(2)
data = None
lock_data = threading.Lock()
exit = threading.Event()
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
                        temp = task2()["temperature"]
                        humidity = task2()["humidity"]
                        print(f"Текущая температура: {temp} ℃, текущая влажность: {humidity}")
                        lock_data.release()
                    case "a":
                        pass
                    case "b":
                        task1()

            case "s":
                chois3 = input("Что вы хотите узнать в счетчике? Электроенергия(E), Газ(G), Вода(W), Bозврат на прошлую страницу(B)")
                match chois3.lower():
                    case "e":
                        lock_data.acquire()
                        electricity = task2()["meter"]["electricity"]["consumption"]
                        print(f"споживання електроенергії: {electricity} Кв")
                        lock_data.release()
                    case "g":
                        lock_data.acquire()
                        gas = task2()["meter"]["gas"]["consumption"]
                        print(f"споживання електроенергії: {gas} м3")
                        lock_data.release()
                    case "w":
                        lock_data.acquire()
                        water = task2()["meter"]["water"]["consumption"]
                        print(f"споживання електроенергії: {water} м3")
                        lock_data.release()
                    case "b":
                        task1()
            case "k":
                chois4 = input("Что вы хотите узнать или сделать в котле? Состояние(C), Включить(P), Выключить(U), Bозврат на прошлую страницу(B)")
                match chois4.lower():
                    case "c":
                        lock_data.acquire()
                        boiler_temp = task2()['boiler']["temperature"]
                        boiler_pres = task2()['boiler']["pressure"]
                        print(f"Теспература в бойлере: {boiler_temp} ℃, давление в боллере {boiler_pres}")
                        lock_data.release()
                    case "p":
                        lock_data.acquire()
                        if task2()['boiler']['isRun'] == False:
                            task2()['boiler']['isRun'] = True
                        print("Болер включён!")
                        lock_data.release()
                    case "u":
                        lock_data.acquire()
                        if task2()['boiler']['isRun'] == True:
                            task2()['boiler']['isRun'] = False
                        print("Болер выключен!")
                        lock_data.release()
                    case "b":
                        task1()
            case "m":
                lock_data.acquire()
                print(data)
                lock_data.release()
            case "e":
                sys.exit()
        exit.set()

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
            file.write(time + "\n" + str(data))
        lock_data.release()
        

th1 = threading.Thread(target=task1)
th2 = threading.Thread(target=task2, daemon=True)


th1.start()
th2.start()

# timer = threading.Timer(5, task2)
# timer.start()

th2.join()
th1.join()

