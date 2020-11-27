import os, sys
import json
import jsonschema

LEGEND = "This log is a short version, for details pls see log_detailed.txt\n" \
         "\n" \
         "Error messages you may encounter: \n" \
         "\n" \
         "'<someproperty>' is a required property\n" \
         "That means you need to add the missing property to the json file.\n" \
         "If you're seeing repeating messages that means you probably need to add " \
         "the properties to several places in the json file. " \
         "Log_detailed will have respective indices for your convinience.\n" \
         "\n" \
         "'<somevalue>' is not of type '<sometype>'\n" \
         "correct the value to be of the type '<sometype>'\n" \
         "if '<somevalue>' is None then the data is missing and you need to add it\n" \
         "\n\n" \
         "The Log:\n"

def validtr(events, schemas):
    log = open('log.txt', 'w')
    log.write(LEGEND)
    logd = open('log_detailed.txt', 'w')
    li = list(events)
    pyschemas = [(schema.name, json.load(open(schema))) for schema in schemas]

    print('Starting validation...')
    for event in li:
        if event.is_file() and not event.name.startswith('.'):
            print(str(event.name))
            try:
                pyevent = json.loads(open(event).read())
                pydata = (pyevent['event'], pyevent['data'])
            # except KeyError or TypeError:
            except:
                continue
        else:
            continue

        for pyschema in pyschemas:
            if pydata[0] == pyschema[0].split('.')[0]:
                valr = jsonschema.Draft7Validator(pyschema[1])
                errors = valr.iter_errors(pydata[1])
                log.write(event.name)
                log.write('\n')
                log.write('error(s):\n')
                logd.write(event.name)
                logd.write('\n')
                logd.write('error(s):\n')
                for error in errors:
                    log.write(str(error).splitlines()[0])
                    log.write('\n')
                    logd.write(str(error))
                    logd.write('\n')
                log.write('\n')
                log.write('---------------------------------------')
                log.write('\n\n')
                logd.write('\n')
                logd.write('---------------------------------------')
                logd.write('\n\n')

    print('Validation complete. See results in log.txt and log_detailed.txt')
    log.close()

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        epath = ''
        spath = ''
        while not epath or not spath:
            epath = str(input('Enter absolute path to events directory: '))
            spath = str(input('Enter absolute path to schemas directory: '))
        events = os.scandir(epath)
        schemas = os.scandir(spath)
        validtr(events, schemas)
    else:
        sys.stderr.write('No arguments required. Run this script without arguments.')
