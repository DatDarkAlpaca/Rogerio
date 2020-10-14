from json import load
import traceback


# Loads a JSON file:
def get(filename):
    try:
        with open(filename) as json_file:
            return load(json_file)
    except AttributeError:
        raise AttributeError('[Json]: Unknown argument')
    except FileNotFoundError:
        raise FileNotFoundError('[Json]: {} wasn\'t found.'.format(filename))


# Modify JSON file:
def modify_existing_argument(filename, argument: str, *args):
    try:
        # Saves all the possible arguments:
        argument_list = []
        with open(filename, 'r') as f:
            data = f.readlines()
            for arg in data:
                arg = arg.split('=', 1)[0]
                argument_list.append(arg)

        # Modifies the arguments:
        with open(filename, 'r+') as f:
            line_list = f.readlines()
            line_to_modify = None

            # Search for the line number of the argument:
            for line_number, line in enumerate(line_list):
                if line.startswith('#') or line.isspace():  # Comments
                    pass
                else:
                    arg, value = line.split('=')
                    new_value = ' '.join(args)

                    if argument == arg:
                        line_to_modify = line_number
                        break

            # Modify this line:
            if line_to_modify is not None:
                line_list[line_to_modify] = arg + '=' + new_value + '\n'

                # Save:
                file = open(filename, 'w')
                file.writelines(line_list)
                file.close()
    except Exception as e:
        print('[ModifyArgument]: {}'.format(e))


# Traceback Maker:
def traceback_maker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = '```py\n{1}{0}: {2}\n```'.format(type(err).__name__, _traceback, err)
    return error if advance else f'{type(err).__name__}: {err}'
