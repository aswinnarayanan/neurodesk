
def check_path(path_string, is_dir, create=False):
    if path_string:
        try:
            input_path = pathlib.Path(path_string).resolve(strict=True)
        except FileNotFoundError:
            input_path = pathlib.Path(path_string).resolve(strict=False)
            print(f'{input_path} not found')
            if is_dir and create:
                input(f'Creating {input_path}. Press Enter to continue...')
                try:
                    input_path.mkdir(parents=True, exist_ok=False)
                except PermissionError:
                    print(f'PermissionError creating {input_path}')
                    return None
            else:
                return None
        if os.access(input_path, os.W_OK):
            return input_path
        else:
            print(f'{input_path} not writable')
            return None
    else:
        return None

def from_config_or_input(config, section, name, description, is_dir, create, force_input=False, test_function=None):
    try:
        path_string = config.get(section, name)
    except (configparser.NoSectionError, configparser.NoOptionError):
        path_string = None

    input_path = check_path(path_string, is_dir)
    while force_input or not input_path:
        path_string = input(f'Enter new {description} (Press [Enter] to skip): ')
        input_path = check_path(path_string, is_dir) or input_path
        if input_path and input_path.exists():
            break
        else:
            print('Invalid. Retry ...')
            continue

    config[section][name] = str(input_path)
    with open(CONFIG_FILE, 'w+') as fh:
        config.write(fh)

    return input_path
    # args.init = True

    # installation_dir = from_config_or_input(
    #     config=config, section='neurodesk',
    #     name='installation_dir', description='Installation Directory', 
    #     is_dir=True, create=True, force_input=args.init)

    # local_applications_dir = from_config_or_input(
    #     config=config, section='neurodesk',
    #     name='applications_dir', description='Applications Directory', 
    #     is_dir=True, create=False, force_input=args.init)

    # local_desktop_directories_dir = from_config_or_input(
    #     config=config, section='neurodesk',
    #     name='desktop_directories_dir', description='Desktop Directory', 
    #     is_dir=True, create=False, force_input=args.init)

    # local_applications_menu = from_config_or_input(
    #     config=config, section='neurodesk',
    #     name='applications_menu', description='Application Menu', 
    #     is_dir=False, create=False, force_input=args.init)




