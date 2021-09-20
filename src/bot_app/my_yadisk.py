import yadisk
from datetime import datetime
from . my_local_settings import yadisk_id, ya_secret, yadisk_token


def save_to_yadisk(username, lastname, id_user, path_jpg):
    y = yadisk.YaDisk(yadisk_id, ya_secret, yadisk_token)
    date = datetime.strftime(datetime.now(), "%d_%m_%y_%a_%H-%M-%S")
    try:
        y.mkdir(f"/{username}_{lastname}_{id_user}")
    except:
        pass

    with open(path_jpg, "rb") as f:
        y.upload(f, f"/{username}_{lastname}_{id_user}/{date}.jpg")
        f.close()

def save_to_yadisk_wallet(username, lastname, id_user, user_message):
    y = yadisk.YaDisk(yadisk_id, ya_secret, yadisk_token)
    date = datetime.strftime(datetime.now(), "%d_%m_%y_%a_%H-%M-%S")
    try:
        y.mkdir(f"/{username}_{lastname}_{id_user}")
    except:
        pass

    file_name = "wallet/" + f"{date}.txt"
    with open(file_name, 'w+') as message:
        message.write(f"{user_message}")
        message.close()

    with open(file_name, 'rb') as message:
        y.upload(message, f"/{username}_{lastname}_{id_user}/{date}.txt")
        message.close()
