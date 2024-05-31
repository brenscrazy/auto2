import os
from pathlib import Path
import time
from datetime import datetime
from random import randrange
import dbm

from telethon.sync import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import SessionPasswordNeededError, ChannelsTooMuchError, ChannelInvalidError, ChannelPrivateError


def dbm_base():
    file = dbm.open('api2.dbm', 'c')
    try:
        file['api_id2']
    except:
        file['api_id2'] = input('Enter api_id:')
        file['api_hash2'] = input('Enter api_hash:')
        file['phone2'] = input('Enter phone number: ')
    file.close()
    return dbm.open('api2.dbm', 'r')


file = dbm_base()
api_id = int(file['api_id2'].decode())
api_hash = file['api_hash2'].decode()
phone = file['phone2'].decode()



BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = os.path.join(BASE_DIR, 'channels.txt')

client = TelegramClient('client2', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter code from TG: '))
    except SessionPasswordNeededError:
        client.sign_in(password=input('Enter code 2FA from TG: '))


with open(FILE_PATH) as file_channels:
    li = file_channels.read().split('\n')


def sleep():
    const = randrange(120, 300, 60)
    print(f'{datetime.now()}: Sleep for {const} secs.')
    time.sleep(const)


def error_processing(channel, message):
    file = open(os.path.join(BASE_DIR, "file_log.txt"), 'a')
    try:
        file.write(f'{datetime.now()}: Channel {channel}, {message}.\n')
    finally:
        file.close()


def joining_a_group(num):
    const = len(li) // num
    count_step = 0
    count_sub_chats = 0
    list_nosub_chats = []
    file = open(os.path.join(BASE_DIR, "file_log.txt"), 'a')
    start = datetime.now()
    try:
        file.write(f'{datetime.now()}: Joining groups\n')
    finally:
        file.close()
    with open("start_from.txt", "r") as f:
        start_from = int(f.read().strip())
    for e in range(start_from, len(li), num):
        count_step += 1
        if count_step <= const:
            for j in li[e:e + num]:
                ind = j.find("http")
                i = j[ind:]
                need_sleep = True
                while True:
                    try:
                        result = client(JoinChannelRequest(channel=i))
                        count_sub_chats += 1
                        print(f'{datetime.now()}: ({count_sub_chats}) Joined {i}')
                        with open("start_from.txt", "w") as f:
                            f.write(str(e + 1))
                        # print(client.get_entity(channel))
                        time.sleep(randrange(10, 20, 1))
                        break
                    except ChannelsTooMuchError:
                        error_processing(i, 'Too many joins.')
                        sleep()
                    except errors.FloodWaitError as e:
                        error_processing(i, 'Missed timings. Will join a bit later!')
                        print(f'{datetime.now()}: Will sleep for {e.seconds + 10}')
                        time.sleep(e.seconds + 10)
                    except ChannelInvalidError:
                        error_processing(i, 'Wrong channel object.')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
                    except ChannelPrivateError:
                        error_processing(i, 'Channel is private.')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
                    except errors.UsernameInvalidError as e:
                        error_processing(i, 'Wrong channel name.')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
                    except Exception as e:
                        error_processing(i, f'Channel name {i} is wrong, or does not exists')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
            if need_sleep:
                sleep()
        else:
           for j in li[e:e + num]:
                ind = j.find("http")
                i = j[ind:]
                need_sleep = True
                while True:
                    try:
                        result = client(JoinChannelRequest(channel=i))
                        count_sub_chats += 1
                        print(f'{datetime.now()}: ({count_sub_chats}) Joined {i}')
                        # print(client.get_entity(channel))
                        time.sleep(randrange(10, 20, 1))
                        break
                    except ChannelsTooMuchError:
                        error_processing(i, 'Too many joins.')
                        sleep()
                    except errors.FloodWaitError as e:
                        error_processing(i, 'Missed timings. Will join a bit later!')
                        print(f'{datetime.now()}: Will sleep for {e.seconds + 10}')
                        time.sleep(e.seconds + 10)
                    except ChannelInvalidError:
                        error_processing(i, 'Wrong channel object.')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
                    except ChannelPrivateError:
                        error_processing(i, 'Channel is private.')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
                    except errors.UsernameInvalidError as e:
                        error_processing(i, 'Wrong channel name.')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
                    except Exception as e:
                        error_processing(i, f'Channel name {i} is wrong, or does not exists')
                        list_nosub_chats.append(i)
                        need_sleep = False
                        break
    file_nosub_channels = open(os.path.join(BASE_DIR, "nosub_channels.txt"), 'w')
    try:
        for i in list_nosub_chats:
            file_nosub_channels.write(f'{i}\n')
    finally:
        file_nosub_channels.close()
    end = datetime.now()
    file1 = open(os.path.join(BASE_DIR, "file_log.txt"), 'a')
    try:
        file1.write(f'{datetime.now()}: Finished .\n Time: {end - start}.\n Joined {count_sub_chats} chats out of {len(li)}\n')
    finally:
        file1.close()


if __name__ == '__main__':
    print(f'{datetime.now()}: Started')
    joining_a_group(5)
    client.disconnect()
    try:
        os.remove(os.path.join(BASE_DIR, 'api2.dbm.bak'))
        os.remove(os.path.join(BASE_DIR, 'api2.dbm.dir'))
        os.remove(os.path.join(BASE_DIR, 'api2.dbm.dat'))
        os.remove(os.path.join(BASE_DIR, 'client2.session'))
    except OSError:
        pass
    print(f'{datetime.now()}: Finished')
