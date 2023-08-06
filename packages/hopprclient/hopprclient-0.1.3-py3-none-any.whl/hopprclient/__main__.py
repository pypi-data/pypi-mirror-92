#!/usr/bin/python

import os, sys, getopt, json
import stdiomask
from service_clients import http_service_client, files_service_client
import hoppr_client

def main(argv):

    try:
        opts, args = getopt.getopt(argv,'hadFf:e:s:w:', ['help', 'configure-auth', 'configure-dataset', 'force-upload', 'folder=', 'env=', 'batch-size=', 'batch-wait='])
    except getopt.GetoptError:
        print('Usage: hopprclient/app.py -f <folder>')
        sys.exit(2)

    folder = None
    env = 'prd'
    configure_auth = False
    configure_dataset = False
    force_upload = False
    batch_size = None
    batch_wait = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('To use hopprclient, you must specify a folder to scan for files to upload.')
            print('hopprclient/app.py -f <folder>')
            print()
            print('Please see the README for an explanation of all command line arguments.')
            sys.exit()
        elif opt in ('-f', '--folder'):
            folder = arg
        elif opt in ('-e', '--env'):
            print('Targeting ' + arg + ' environment.')
            env = arg
        elif opt in ('-a', '--configure-auth'):
            configure_auth = True
        elif opt in ('-d', '--configure-dataset'):
            configure_dataset = True
        elif opt in ('-F', '--force-upload'):
            force_upload = True
        elif opt in ('-s', '--batch-size'):
            batch_size = int(arg)
        elif opt in ('-w', '--batch-wait'):
            batch_wait = float(arg)

    base_url = 'https://api-' + env + '.hoppr.ai'
    
    if not os.path.isdir('.hoppr'):
        os.mkdir('.hoppr')

    app_config = {}
    credentials = None
    try:
        with open('.hoppr/config.json') as f:
            app_config = json.load(f)
            credentials = app_config['credentials']
            if credentials is not None:
                print('Credentials loaded from config file.')
                print('To reset the credentials, run the program with the -a (--configure-auth) argument.')
    except IOError:
        pass

    if credentials is None or configure_auth:
        credentials = {}
        print('Configuring credentials. Please enter your credentials at the prompt.')
        credentials['Hoppr-Account-Id'] = input('Account ID: ')
        credentials['Hoppr-Account-Secret'] = stdiomask.getpass(prompt='Account Secret: ')
        app_config['credentials'] = credentials

        with open('.hoppr/config.json', 'w') as f:
            json.dump(app_config, f, indent=2)
        
    if folder is None:
        print('No folder passed to process, exiting.')
        print('Usage: hopprclient/app.py -f <folder>')
        sys.exit()

    if not os.path.isdir(folder):
        print('Invalid folder passed to process, exiting.')
        sys.exit()

    http_client = http_service_client.HttpServiceClient(base_url, credentials)
    files_client = files_service_client.FilesServiceClient(http_client)
    client = hoppr_client.HopprClient(files_client)

    client.process(folder, configure_dataset, batch_size, batch_wait, force_upload)

if __name__ == '__main__':
    main(sys.argv[1:])