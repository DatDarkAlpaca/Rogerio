from os import chdir, remove


# Saves the current stream:
def save_stream(config_file, reply):
    # Change back to the bot directory (just in case):
    chdir(config_file['bot_dir'])

    try:
        with open(config_file['temp_stream'], 'a') as temp:
            temp.write(reply + '\n')
    except:
        temp = open(config_file['temp_stream'], 'w+')
        temp.write(reply + '\n')
        temp.close()
    finally:
        print('[Stream]: Something went wrong while trying to save the stream.')


# Deletes the current stream:
def delete_stream(config_file):
    try:
        remove(config_file['temp_stream'])
    except Exception as e:
        print('[Stream]: Something went wrong while trying to delete the stream. {}'.format(e))
