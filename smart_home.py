import threading, requests,json, time, os
sm = threading.Semaphore(2)
data = None
lock_data = threading.Lock()
def task1():
    choise1 = input("Что вы хотите узнать? Температура/Влажность(T), Счетчики(S), Котел(K), Журнал(M)")
    match choise1.lower():
        case "t":
            chois2 = input("Что вы хотите узнать в температуре? Текущая температура/влажность(N), Средняя температура/влажность(A), Bозврат на прошлую страницу(B)")
            match chois2.lower():
                case "n":
                    temp = task2()["temperature"]
                    humidity = task2()["humidity"]
                    print(f"Текущая температура: {temp} ℃, текущая влажность: {humidity}")
                case "a":
                    pass
                case "b":
                    task1()

        case "s":
            chois3 = input("Что вы хотите узнать в счетчике? Электроенергия(E), Газ(G), Вода(W), Bозврат на прошлую страницу(B)")
            match chois3.lower():
                case "e":
                    electricity = task2()["meter"]["electricity"]["consumption"]
                    print(f"споживання електроенергії: {electricity} Кв")
                case "g":
                    gas = task2()["meter"]["gas"]["consumption"]
                    print(f"споживання електроенергії: {gas} м3")
                case "w":
                    water = task2()["meter"]["water"]["consumption"]
                    print(f"споживання електроенергії: {water} м3")
                case "b":
                    task1()
        case "k":
            chois4 = input("Что вы хотите узнать или сделать в котле? Состояние(C), Включить(P), Выключить(U), Bозврат на прошлую страницу(B)")
            match chois4.lower():
                case "c":
                    boiler_temp = task2()['boiler']["temperature"]
                    boiler_pres = task2()['boiler']["pressure"]
                    print(f"Теспература в бойлере: {boiler_temp} ℃, давление в боллере {boiler_pres}")
                case "p":
                    print("Болер включён!")
                case "u":
                    print("Болер выключен!")
                case "b":
                    task1()
        case "m":
            print(data)

def task2( ):
    while True:
        global data
        response = requests.get("http://localhost:8000/cgi-bin/exemple_json.py")
        lock_data.acquire()
        data = json.loads(response.text)
        time.sleep(5)
        lock_data.release()
        return data
        # data = response.json()
        # with open("example.txt", "w") as file:
        #     data = json.load(file)
        #     print(f"Дата: {datetime.datetime()}, содержимоє: {data}")

th1 = threading.Thread(target=task1)
th2 = threading.Thread(target=task2, daemon=True)


th1.start()
th2.start()

timer = threading.Timer(5, task2)
timer.start()

th2.join()
th1.join()

