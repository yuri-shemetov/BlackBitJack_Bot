from os import mkdir
import yadisk
from datetime import datetime
from . my_local_settings import yadisk_id, ya_secret, yadisk_token
import csv

def save_to_yadisk(id_user, path_jpg):
    y = yadisk.YaDisk(yadisk_id, ya_secret, yadisk_token)
    date = datetime.strftime(datetime.now(), "%d_%m_%y-%H-%M-%S")
    mounth = datetime.strftime(datetime.now(), "%y_%m")
    order = datetime.strftime(datetime.now(), "%d/%m/%y-%H:%M:%S")

    try:
        y.mkdir(f"/{mounth}")
    except:
        pass
    try:
        y.mkdir(f"/{mounth}/00_PHOTO")
    except:
        pass
    try:
        mkdir(f"{mounth}/")
    except:
        pass
     
    myData = [[f'{order} ', f'id: ', f'{id_user} ',  f'path_to_photo: ', f'{date}_id{id_user}.jpg']]
    path_csv = f'{mounth}/My_DATA.csv'
    
    with open(path_csv, 'a+') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(myData)
        file_csv.close()

    with open(path_csv, 'rb+') as file_csv:
        try:
            y.remove(f"/{mounth}/00_MY_DATA_{mounth}.csv", permanently=True)
        except:
            pass    
        y.upload(file_csv, f"/{mounth}/00_MY_DATA_{mounth}.csv")
        file_csv.close()
        
    with open(path_jpg, "rb") as photo:
        y.upload(photo, f"/{mounth}/00_PHOTO/{date}_id{id_user}.jpg")
        photo.close()

def save_to_yadisk_wallet(username, lastname, id_user, user_message):
    y = yadisk.YaDisk(yadisk_id, ya_secret, yadisk_token)
    date = datetime.strftime(datetime.now(), "%d_%m_%y-%H-%M-%S")
    mounth = datetime.strftime(datetime.now(), "%y_%m")

    try:
        mkdir(f"wallet/")
    except:
        pass
    try:
        y.mkdir(f"/{mounth}/00_WALLET")
    except:
        pass

    file_name = "wallet/" + f"{date}.txt"
    with open(file_name, 'w+') as message:
        message.write(f"{user_message}")
        message.close()

    with open(file_name, 'rb') as message:
        y.upload(message, f"/{mounth}/00_WALLET/{date}_id{id_user}_[{username}_{lastname}].txt")
        message.close()