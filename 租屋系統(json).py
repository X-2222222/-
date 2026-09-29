houses=[]
from datetime import datetime
import json

def input_positive_integer(message):
    while True:
        try:
            value=int(input(message))
            if value>0:
                return value
            else:
                print('請輸入大於0的數字')
        except ValueError:
            print('請輸入數字') 

def input_phone(message):
    while True:
        phone=input(message)
        if phone.startswith('09') and len(phone)==10 and phone.isdigit():
            return phone
        elif phone.startswith('0') and len(phone)==10 and phone.isdigit():
            return phone
        elif '-' in phone:
            phone=phone.replace('-','')
            if phone.startswith('0') and phone.isdigit() and len(phone) in [9,10]:
                return phone
            else:
                print('電話格式錯誤，請重新輸入')
        else:
            print('電話格式錯誤，請輸入正確的手機或市話')

def show_menu():
    print('=====學生租屋系統=====')
    print('1.新增房源')
    print('2.刪除房源')
    print('3.修改房源')
    print('4.查詢房源')
    print('5.顯示所有房源')
    print('6.依租金搜尋房源')
    print('7.依房型搜尋房源')
    print('8.依地區搜尋房源')
    print('9.多項篩選')
    print('10.離開')

def select_menu():
    while True:
        try:
            select=int(input('請輸入功能選單編號:'))
            if 1<=select<=10:
                return select
            else:
                print('請輸入正確的編號')
        except ValueError:
            print('請輸入正確的編號')

def add_house():
    house_address=input('請輸入房屋地址及樓層:')
    house_rent=input_positive_integer('請輸入房屋租金:')
    while True:
        house_roomtype=input('請輸入房型(雅房/套房):')
        if house_roomtype in['雅房','套房']:
            break
        else:
            print('房型輸入錯誤，請輸入雅房或套房')
    house_contact=input_phone('請輸入房東連絡電話:')
    while True:
        try:
            house_checkin=input('請輸入可入住日期(YYYY-MM-DD):')
            datetime.strptime(house_checkin,'%Y-%m-%d')
            break
        except ValueError:
            print('日期格式輸入錯誤')
    house_fees=input_positive_integer('請輸入水電費用:')
    house_id=generate_house_id()
    house={'房屋編號':house_id,
           '房屋地址及樓層':house_address,
           '房屋租金':house_rent,
           '房型':house_roomtype,
           '房東連絡電話':house_contact,
           '可入住日期':house_checkin,
           '水電費用':house_fees}
    houses.append(house)
    save_houses()
    print(f'已新增房源:{house_address}')
    display_houses()

def delete_house():
    if len(houses)==0:
        print('目前沒有房源')
        return
    found=False
    house_id=int(input('請輸入要刪除的房源編號:'))
    for house in houses:
        if house['房屋編號']==house_id:
            houses.remove(house)
            found=True
            print(f"已刪除房源:{house['房屋地址及樓層']}")
            save_houses()
            break
    if not found:
        print(f'找不到編號:{house_id}，請重新輸入')
    
def modify_house():
    if len(houses)==0:
        print('目前尚未有房源')
        return
    while True:
        try:
            found=False
            house_id=int(input('請輸入要修改的房源編號:'))
            for house in houses:
                if house['房屋編號']==house_id:
                    found=True
                    print(f'房源{house["房屋地址及樓層"]}的資料如下:\n')
                    for key in house:
                        print(f'{key}: {house[key]}')
                    select=input('請輸入欄位名稱 (房屋地址及樓層/房屋租金/房型/房東連絡電話/可入住日期/水電費用):')
                    if select=='房屋地址及樓層':
                        new_address=input('請輸入新的房屋地址及樓層:')
                        house['房屋地址及樓層']=new_address
                    elif select=='房屋租金':
                        new_rent=input_positive_integer('請輸入新的房屋租金:')
                        house['房屋租金']=new_rent
                    elif select=='房型':
                        while True:
                            new_roomtype=input('請輸入新的房型(雅房/套房):')
                            if new_roomtype in['雅房','套房']:
                                break
                            else:
                                print('房型輸入錯誤，請輸入雅房或套房')
                        house['房型']=new_roomtype
                    elif select=='房東連絡電話':
                        new_contact=input_phone('請輸入房東連絡電話:') 
                        house['房東連絡電話']=new_contact
                    elif select=='可入住日期':
                        while True:
                            try:
                                new_checkin=input('請輸入可入住日期(YYYY-MM-DD):')
                                datetime.strptime(new_checkin,'%Y-%m-%d')
                                break
                            except ValueError:
                                print('日期格式輸入錯誤')
                        house['可入住日期']=new_checkin
                    elif select=='水電費用':
                        new_fees=input_positive_integer('請輸入新的水電費用:')
                        house['水電費用']=new_fees
                    else:
                        print(f'找不到欄位名稱:{select}，請重新輸入')
                    save_houses()
                    return
            if not found:
                print(f'找不到編號:{house_id}，請重新輸入')
        except ValueError:
            print('請輸入數字')   

def search_house():
    if len(houses)==0:
        print('目前沒有房源')
        return
    found=False
    house_id=int(input('請輸入要查詢的房源編號:'))
    for house in houses:
        if house['房屋編號']==house_id:
            print(f'房源{house["房屋地址及樓層"]}的資料如下:\n')
            for key in house:
                print(f'{key}: {house[key]}')
            found=True
            break
    if not found:
        print(f'找不到編號:{house_id}，請重新輸入')

def show_all_houses():
    if len(houses)==0:
        print('目前沒有房源')
        return
    elif len(houses)>0:
        print('目前所有房源如下:')
        for index, house in enumerate(houses):
            print(f'房屋編號:{house["房屋編號"]}')
            for key in house:
                print(f'{key}: {house[key]}')
            print('--------------------')

def display_houses():
    if len(houses)==0:
        print('目前沒有房源')
        return
    for house in houses:
        print(f'房屋編號:{house["房屋編號"]}')
        print(f'房屋地址及樓層:{house["房屋地址及樓層"]}')
        for key in house:
            print(f'{key}: {house[key]}')
        print('-'*20)

def search_houses_by_rent():
    if len(houses) == 0:
        print('目前沒有房源')
        return
    while True:
        try:
            min_rent=int(input('請輸入最低租金:'))
            max_rent=int(input('請輸入最高租金:'))
            found_houses=[]
            for house in houses:
                rent=int(house['房屋租金'])
                if min_rent<=rent<=max_rent:
                    found_houses.append(house)
            print('排序方式:')
            print('1.由低到高')
            print('2.由高到低')
            sort = input('請選擇排序方式編號:')
            if sort=='1':
                found_houses.sort(key=lambda house:int(house['房屋租金']))
            elif sort=='2':
                found_houses.sort(key=lambda house:int(house['房屋租金']),reverse=True)
            else:
                print('輸入錯誤已由系統自動設定由低到高排序')
                found_houses.sort(key=lambda house:int(house['房屋租金']))
            print('符合條件的房源如下:')
            for i, house in enumerate(found_houses):
                print(f'房屋編號:{house["房屋編號"]}')
                print(f'房屋地址及樓層:{house["房屋地址及樓層"]}')
                for key in house:
                    print(f"{key}: {house[key]}")
                print('-' * 20)
            break
        except ValueError:
            print('請輸入數字')

def search_houses_by_roomtype():
    if len(houses)==0:
        print('目前沒有房源')
        return
    while True:
        try:
            roomtype=input('請輸入想要的房型(雅房/套房):')
            found_houses=[]
            for house in houses:
                if house['房型']==roomtype:
                    found_houses.append(house)
            if found_houses:
                print('符合條件的房源如下:')
                for i, house in enumerate(found_houses):
                    print(f'房屋編號:{house["房屋編號"]}')
                    print(f'房屋地址及樓層:{house["房屋地址及樓層"]}')
                    for key in house:
                        print(f"{key}: {house[key]}")
                    print('-'*20)
                break
            else:
                print('沒有符合條件的房源')
        except ValueError:
            print('請輸入正確的房型')

def search_houses_by_area():
    if len(houses)==0:
        print('目前沒有房源')
        return
    while True:
        try:
            area=input('請輸入想要的地區:')
            found_houses=[]
            for house in houses:
                if area in house['房屋地址及樓層']:
                    found_houses.append(house)
            if found_houses:
                print('符合條件的房源如下:')
                for i, house in enumerate(found_houses):
                    print(f'房屋編號:{house["房屋編號"]}')
                    print(f'房屋地址及樓層:{house["房屋地址及樓層"]}')
                    for key in house:
                        print(f"{key}: {house[key]}")
                    print('-'*20)
                break
            else:
                print('沒有符合條件的房源')
        except ValueError:
            print('請輸入正確的地區')
    
def search_houses_by_multiple():
    if len(houses)==0:
        print('目前沒有房源')
        return
    filiter_houses=[]
    min_rent = None
    max_rent = None
    roomtype = None
    area = None
    while True:
        print('=====多功能查詢=====')
        print('1.租金')
        print('2.房型')
        print('3.地區')
        print('4.開始搜尋')
        select=int(input('請輸入篩選編號:'))
        if select==1:
            min_rent=int(input('請輸入最低租金:'))
            max_rent=int(input('請輸入最高租金:'))
        elif select==2:
            roomtype=input('請輸入想要的房型(雅房/套房):')
        elif select==3:
            area=input('請輸入想要的地區:')
        elif select==4:
            if min_rent is None and roomtype is None and area is None:
                print('尚未選擇任何篩選條件')
                continue
            filiter_houses=[]
            for house in houses:
                rent_ok=True
                roomtype_ok=True
                area_ok=True
                if min_rent is not None and max_rent is not None:
                    rent=int(house['房屋租金'])
                    rent_ok=min_rent<=rent<=max_rent
                if roomtype is not None:
                    roomtype_ok=house['房型']==roomtype
                if area is not None:
                    area_ok=area in house['房屋地址及樓層']
                if rent_ok and roomtype_ok and area_ok:
                    filiter_houses.append(house)
            if filiter_houses:
                    print('符合條件的房源如下:')
                    for i, house in enumerate(filiter_houses):
                        print(f'房屋編號:{house["房屋編號"]}')
                        print(f'房屋地址及樓層:{house["房屋地址及樓層"]}')
                        for key in house:
                            print(f"{key}: {house[key]}")
                        print('-'*20)
            else:
                print('沒有符合條件的房源')     
            return     

def save_houses():
    with open('houses.json','w',encoding='utf-8') as file:
        json.dump(houses,file,ensure_ascii=False,indent=4)
    print('已儲存至houses.json')

def load_houses():
    global houses
    try:
        with open('houses.json','r',encoding='utf-8') as file:
            houses=json.load(file)
    except FileNotFoundError:
        houses=[]
    except json.JSONDecodeError:
        print('houses.json檔案格式錯誤，請檢查檔案內容')
        houses=[]

def generate_house_id():
    if len (houses)==0:
        return 1
    else:
       ids=[]
       for house in houses:
           ids.append(house['房屋編號'])
       return max(ids)+1


def main():
    print('歡迎使用學生租屋系統')
    load_houses()
    show_menu()
    select=select_menu()
    while True:
        if select==1:
            add_house()
            show_menu()
            select=select_menu()
        elif select==2:
            delete_house()
            show_menu()
            select=select_menu()
        elif select==3:
            modify_house()
            display_houses()
            show_menu()
            select=select_menu()
        elif select==4:
            search_house()
            show_menu()
            select=select_menu()
        elif select==5:
            show_all_houses()
            show_menu()
            select=select_menu()
        elif select==6:
            search_houses_by_rent()
            show_menu()
            select=select_menu()
        elif select==7:
            search_houses_by_roomtype()
            show_menu()
            select=select_menu()
        elif select==8:
            search_houses_by_area()
            show_menu()
            select=select_menu()
        elif select==9:
            search_houses_by_multiple()
            show_menu()
            select=select_menu()    
        elif select==10:
            break

main()