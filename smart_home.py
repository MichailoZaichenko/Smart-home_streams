import threading, requests,json, time
lock = threading.Lock()
sm = threading.Semaphore(2)

def task1():
    choise1 = input("Что вы хотите узнать? Температура/Влажность(T), Счетчики(S), Котел(K), Журнал(M)")
    match choise1.lower():
        case "t":
            chois2 = input("Что вы хотите узнать в температуре? Текущая температура/влажность(N), Средняя температура/влажность(A), Bозврат на прошлую страницу(B)")
            match chois2.lower():
                case "n":
                    pass
                case "a":
                    pass
                case "b":
                    pass

        case "s":
            chois3 = input("Что вы хотите узнать в счетчике? Электроенергия(E), Газ(G), Вода(W), Bозврат на прошлую страницу(B)")
            match chois3.lower():
                case "e":
                    pass
                case "g":
                    pass
                case "w":
                    pass
                case "b":
                    pass
        case "k":
            chois4 = input("Что вы хотите узнать или сделать в котле? Состояние(C), Включить(P), Выключить(U), Bозврат на прошлую страницу(B)")
            match chois4.lower():
                case "c":
                    pass
                case "p":
                    pass
                case "u":
                    pass
                case "b":
                    pass
        case "m":
            pass

def task2( ):
    while True:
        obj = None
        response = requests.get("http://localhost:8000/cgi-bin/exemple_json.py")
        obj = json.loads(response.text)
        print(obj)
        time.sleep(5)

th1 = threading.Thread(target=task1)
th2 = threading.Thread(target=task2)


th1.start()
th1.join()

th2.start()
th2.join()
