# -*- coding: utf-8 -*-

#TODO: SANITIZE FUCKING EVERYTHING THAT I GET FROM ANYWHERE. REMOVE EVERY ASCII LITERAL EXCEPT FOR \n AND \t. FUCK THEM.


import os, time, datetime, ConfigParser, stat
from sys import platform as _platform

#TODO: Move all strings somewhere else (for easier localisation)

SETTINGS_OVERRIDE = False               #Ignores the settings file completely. Uses the defaults below.
SETTINGS_FILE_LOCATION = ""             #Don't change this unless you REALLY have to.
SETTINGS_FILE_NAME = "settings.ini"     #Same with this one.

FILES_LOCATION = "C:/TEST1"
OVERWRITE_DUPLICATE_FILES = True
MOVED_FILE_PERMISSIONS_ENABLE = True   #LINUX ONLY
MOVED_FILE_PERMISSIONS_VALUE = 17      #LINUX ONLY
AUTO_RECHECK = False
RECHECK_MINS = 15
SCAN_DEPTH = 2

#move_orders file settings
MOVE_FILE_DIRECTORY = ""                #Nothing for same directory
MOVE_FILE_NAME = "move_orders.txt"      #Don't bother changing this either.
MOVE_FILE_SEPERATOR = "||"
MOVE_NAME_SEPERATOR = "**"

#VERY VERY EXPERIMENTAL
PLATFORM_OVERRIDE_ENABLE = False
PLATFORM_OVERRIDE_STRING = "linux"      #win32, linux, darwin

DEBUG_OUTPUT_ENABLE = False
EVERYTHING_BUT_MOVE = False              #Good for testing, does everything except actually perform the move.   #ADD TO SETTINGS.INI
UNIT_TEST_ENABLE = True                                                                                        #ADD TO SETTINGS.INI

#TRUE/FALSE ACCEPTED STRINGS
TRUE_STRINGS = ['true', 'True', 'Yes', 'yes', 'aye', '1', 'Y', 'yarp']
FALSE_STRINGS = ['false', 'False', 'No', 'no', 'neigh', '0', 'N', 'narp']
#INVALID CHARS IN NAMES/DIRECTORIES (MOSTLY ASCII LITERALS)
INVALID_CHARS = ['\b', '\a', '\r' '\f'] #Fuck these literals in particular
#CHARS THAT MAY BREAK THINGS (especially in windows)
WARNING_CHARS = ['/', '*'] #TODO: ADD MORE

#Everything that isn't a setting
MOVES_FILES_LIST = []
ERRORS_LIST = []


def intToChmodPerm(input):
    """Outputs stat permission value based on int from user settings"""
    if input==0: return stat.S_ISUID    #Set user ID on execution.
    elif input==1: return stat.S_ISGID  #Set group ID on execution.
    elif input==2: return stat.S_ENFMT  #Record locking enforced.
    elif input==3: return stat.S_ISVTX  #Save text image after execution.
    elif input==4: return stat.S_IREAD  #Read by owner.
    elif input==5: return stat.S_IWRIT  #Write by owner.
    elif input==6: return stat.S_IEXEC  #Execute by owner.
    elif input==7: return stat.S_IRWXU  #Read, write, and execute by owner.
    elif input==8: return stat.S_IRUSR  #Read by owner.
    elif input==9: return stat.S_IWUSR  #Write by owner.
    elif input==10: return stat.S_IXUSR #Execute by owner.
    elif input==11: return stat.S_IRWXG #Read, write, and execute by group.
    elif input==12: return stat.S_IRGRP #Read by group.
    elif input==13: return stat.S_IWGRP #Write by group.
    elif input==14: return stat.S_IXGRP #Execute by group.
    elif input==15: return stat.S_IRWXO #Read, write, and execute by others.
    elif input==16: return stat.S_IROTH #Read by others.
    elif input==17: return stat.S_IWOTH #Write by others.
    elif input==18: return stat.S_IXOTH #Execute by others.
    else: return None

def debugOut(output):
    """Outputs debug stuff when enabled in settings"""
    if DEBUG_OUTPUT_ENABLE: 
        print "DEBUG: "+output

def stringToBool(input):
    if str(input) in TRUE_STRINGS: return True
    elif str(input) in FALSE_STRINGS: return False
    else:
        print "ERROR parsing string to boolean (true/false)\n"\
        + "Input: '"+input+"'\n"\
        + "Typically caused by an error in the settings file. Check for errors.\n"\
        + "Accepted values:\n(TRUE) "+str(TRUE_STRINGS)+"\n(FALSE) "+str(FALSE_STRINGS)
        exit()


def getSettings():
    """Gets program settings from a settings file"""
    debugOut("getSettings ENTER")

    if SETTINGS_OVERRIDE:
        print "################################\n"\
            + "# WARNING! SETTINGS OVERRIDDEN #\n"\
            + "################################\n"
        return

    settings = ConfigParser.ConfigParser()

    global FILES_LOCATION
    global OVERWRITE_DUPLICATE_FILES
    global MOVED_FILE_PERMISSIONS_ENABLE
    global MOVED_FILE_PERMISSIONS_VALUE
    global AUTO_RECHECK
    global RECHECK_MINS
    global SCAN_DEPTH
    global MOVE_FILE_SEPERATOR
    global MOVE_NAME_SEPERATOR
    global PLATFORM_OVERRIDE_ENABLE
    global PLATFORM_OVERRIDE_STRING
    global DEBUG_OUTPUT_ENABLE
    global DICKBUTT_ENABLE

    #Make a new settings file if one doesn't exist.
    if not os.path.exists(SETTINGS_FILE_LOCATION+SETTINGS_FILE_NAME):
        print "WARNING - settings.ini not found. Making one with default settings.\n"

        settings_file = open(SETTINGS_FILE_LOCATION+SETTINGS_FILE_NAME, 'w')

        settings.add_section('Files')
        settings.set('Files', 'Files Location', str(FILES_LOCATION))
        settings.set('Files', 'Overwrite Duplicate Files', str(OVERWRITE_DUPLICATE_FILES))
        settings.set('Files', 'Moved Files Permissions Enable', str(MOVED_FILE_PERMISSIONS_ENABLE))
        settings.set('Files', 'Moved Files Permissions Value', str(MOVED_FILE_PERMISSIONS_VALUE))
        settings.set('Files', 'File Scan Depth', str(SCAN_DEPTH))

        settings.add_section('Auto Check')
        settings.set('Auto Check', 'Auto Check Enable', str(AUTO_RECHECK))
        settings.set('Auto Check', 'Check Rate (mins)', str(RECHECK_MINS))

        settings.add_section('Move Orders')
        settings.set('Move Orders', 'File Location Seperator', str(MOVE_FILE_SEPERATOR))
        settings.set('Move Orders', 'File Name End Seperator', str(MOVE_NAME_SEPERATOR))

        settings.add_section('Platform Override')
        settings.set('Platform Override', 'Platform Override Enable', str(PLATFORM_OVERRIDE_ENABLE))
        settings.set('Platform Override', 'Platform Override Option', str(PLATFORM_OVERRIDE_STRING))

        settings.add_section('Other')
        settings.set('Other', 'Debug Output Enable', str(DEBUG_OUTPUT_ENABLE))

        settings.write(settings_file)
        settings_file.close()
        time.sleep(0.5)

    settings.read(SETTINGS_FILE_LOCATION+SETTINGS_FILE_NAME)

    FILES_LOCATION                  = settings.get('Files', 'Files Location')
    OVERWRITE_DUPLICATE_FILES       = stringToBool(settings.get('Files', 'Overwrite Duplicate Files'))
    MOVED_FILE_PERMISSIONS_ENABLE   = stringToBool(settings.get('Files', 'Moved Files Permissions Enable'))
    MOVED_FILE_PERMISSIONS_VALUE    = int(settings.get('Files', 'Moved Files Permissions Value'))
    SCAN_DEPTH                      = int(settings.get('Files', 'File Scan Depth'))
    AUTO_RECHECK                    = stringToBool(settings.get('Auto Check', 'Auto Check Enable'))
    RECHECK_MINS                    = int(settings.get('Auto Check', 'Check Rate (mins)'))
    MOVE_FILE_SEPERATOR             = settings.get('Move Orders', 'File Location Seperator')
    MOVE_NAME_SEPERATOR             = settings.get('Move Orders', 'File Name End Seperator')
    PLATFORM_OVERRIDE_ENABLE        = stringToBool(settings.get('Platform Override', 'Platform Override Enable'))
    PLATFORM_OVERRIDE_STRING        = settings.get('Platform Override', 'Platform Override Option')
    DEBUG_OUTPUT_ENABLE             = stringToBool(settings.get('Other', 'Debug Output Enable'))

    print "FILES LOCATION = "+FILES_LOCATION

def sendEmail():
    """Sends an email of what just happened"""
    #TODO: Implement this!
    print "Sending Email...."
    print "(EMAIL ALERTS COMING SOON!)"

    return True

def getMoveOrders(): 
    """DEPRECIATED"""

    move_orders_list = []
    move_file = open(MOVE_FILE_DIRECTORY+MOVE_FILE_NAME)
    lines = str.split(move_file.read(),"\n")

    for i, line in enumerate(lines):
        if MOVE_FILE_SEPERATOR in line:
            move_orders_list.append(line.split(MOVE_FILE_SEPERATOR))
        else:
            print "CANT READ LINE {0} IN move_orders.txt!\n{1}\n".format(i+1,line)

    move_file.close()
    return move_orders_list


def getMoveOrders2():
    """Supports end operators"""

    move_orders_list = []

    move_file = open(MOVE_FILE_DIRECTORY+MOVE_FILE_NAME) #TODO: Move this string to the top

    lines = str.split(move_file.read(), "\n") #Split file by new lines

    for i, line in enumerate(lines):

        #Sanitize all the incoming orders
        for char in INVALID_CHARS:
            line = line.replace(char, "")

        if not line == "" and MOVE_FILE_SEPERATOR in line:
            if MOVE_NAME_SEPERATOR in line:
                split_line = line.split(MOVE_FILE_SEPERATOR)
                split_line2 = split_line[0].split(MOVE_NAME_SEPERATOR)
                move_orders_list.append([split_line2[0], split_line2[1], split_line[1]])

            else:
                move_orders_list.append(line.split(MOVE_FILE_SEPERATOR))

        else:
            print "(Ignoring invalid line: '"+str(line)+"')"

    move_file.close()
    if DEBUG_OUTPUT_ENABLE:
        print "MOVE ORDERS:"
        for move in move_orders_list:
            print repr(move) #print literals too

    return move_orders_list


def getFiles(dir) :
    """Gets filenames in directory"""
    #TODO: this could be much better by checking if the folder exists before getting the files.
    #TODO: Filter out imvalid charecters for os.walk here (like \).

    try:
        #filenames = next(os.walk(dir.encode('utf8')))[2] #BUGGY AS FUCK ON LINUX FOR NO GOOD REASON
        filenames = []
        dirnames = []

        for(dpath, dnames, fnames) in os.walk(dir):
            filenames.extend(fnames)
            dirnames.extend(dnames)
            break

        print dirnames

    #This exception is usually catastrophic (not finding the source folder).
    except Exception as exc:
        print "ERROR GETTING FILES! (Ignore if target folder does not yet exist) DIR = "+dir
        print exc
        print "END OF ERROR"
        filenames = [] #Make an empty filenames object so it continues as usual.

    if DEBUG_OUTPUT_ENABLE:
        debugOut("Files found:")
        for file in filenames:
            debugOut("\t"+file)

    return filenames

def fileSearcher(dir):
    try:
        #filenames = next(os.walk(dir.encode('utf8')))[2] #BUGGY AS FUCK ON LINUX FOR NO GOOD REASON
        filenames = []
        dirnames = []

        for(dpath, dnames, fnames) in os.walk(dir):
            filenames.extend(fnames)
            dirnames.extend(dnames)
            break

        filenamesandpaths = []
        for f in filenames:
            filenamesandpaths.append(dir+'/'+str(f))

        dirnamesandpaths = []
        for d in dirnames:
            dirnamesandpaths.append(dir+'/'+str(d))


    except Exception as exc:
        print "ERROR GETTING FILES! (Ignore if target folder does not yet exist) DIR = "+dir
        print exc
        print "END OF ERROR"
        filenames = [] #Make an empty filenames object so it continues as usual.

    if DEBUG_OUTPUT_ENABLE:
        debugOut("Files found:")
        for file in filenames:
            debugOut("\t"+file)

    data = {'files': filenames, 'filesandpaths': filenamesandpaths, 'dirs': dirnamesandpaths}
    return data



def getFiles2(dir, depth = SCAN_DEPTH):
    '''Improvement on getFiles, now scans through directories recursivly through subdirectories! Yay!'''

    files = []
    filesandpaths = []
    data = fileSearcher(dir)
    files.extend(data['files'])
    filesandpaths.extend(data['filesandpaths'])

    dirs = data['dirs']

    while depth is not 0 and dirs is not None:
        depth = depth - 1

        for subdir in dirs:
            data = fileSearcher(subdir)
            dirs = dirs + data['dirs'] 
            files = files + data['files']
            filesandpaths = filesandpaths + data['filesandpaths']
            dirs.remove(subdir)

    data = {'files': files, 'filesandpaths': filesandpaths}
    return data
    

def moveFile(fileOrigin,fileName,fileDestination,overwrite=False):
    """DO THE MOVING THING"""
    #TODO: MOVE THIS SHIT TO THE TOP (REPEATED ELSEWHERE))
    #TODO: TRIM THIS THE FUCK DOWN. THE PROCESSES ARE ALL THE SAME AT THIS LEVEL
    if PLATFORM_OVERRIDE_ENABLE:
        _platform = PLATFORM_OVERRIDE_STRING

    if EVERYTHING_BUT_MOVE:
        print "EVERYTHING BUT MOVE MODE ENABLED, PRETENDING TO MOVE FILE"
        return

    if _platform == "win32": #Working on most systems
        #DO WINDOWS MOVE
        try:
            if not os.path.exists(fileDestination):
                print "\t\tWARNING! Directory '"+str(fileDestination)+"' not found. Making a new one...."
                os.makedirs(fileDestination)
                if MOVED_FILE_PERMISSIONS_ENABLE:
                    print "\t\tPermissions are not currently supported with Windows, so turning it on is pointless."

            os.rename(fileOrigin+"/"+fileName, fileDestination+"/"+fileName)
            print "\t\tFile move successful!"

            if MOVED_FILE_PERMISSIONS_ENABLE:
                print "\t\tPermissions are not currently supported with Windows, so turning it on is pointless."

        except Exception as e:
            print e
            raise e


    elif _platform == "darwin": #Should be similar to Linux
        #DO OSX MOVE
        print "WARNING! OSX NOT SUPPORTED! EXITING!"
        exit()



    elif _platform == "linux": #Largely untested
        #DO LINUX MOVE
        try:
            if not os.path.exists(fileDestination.replace("\r", "")):
                print "\t\tWARNING! Directory '"+str(fileDestination)+"' not found. Making a new one...."
                os.makedirs(fileDestination)

                if MOVED_FILE_PERMISSIONS_ENABLE:
                    print "\t\tChanged directory permissions to "+str(MOVED_FILE_PERMISSIONS_VALUE)
                    os.chmod(fileDestination, stat.S_IRWXO)

            os.rename((fileOrigin+"/"+fileName).replace("\r", ""), (fileDestination+"/"+fileName).replace("\r", ""))
            print "\t\tFile move successful!"
            if MOVED_FILE_PERMISSIONS_ENABLE:
                os.chmod((fileDestination+"/"+fileName).replace("\r", ""), stat.S_IRWXO)
                print "\t\tChanged file permissions to "+str(MOVED_FILE_PERMISSIONS_VALUE)

        except Exception as e:
            print e
            raise e

    else:
        print "ERROR! OS not supported! Oh no!.\nOS found: "+str(_platform)+"\nExiting...."
        exit()


def removeFile(file):
    """Delete a specific file"""

    _platform = PLATFORM_OVERRIDE_STRING #FIX THIS!

    if PLATFORM_OVERRIDE_ENABLE:
        _platform = PLATFORM_OVERRIDE_STRING

    if _platform == "win32":
        #WINDOWS
        try:
            os.remove(file)
            return True
        except Exception as exc:
            print e
            raise e

    elif _platform == "linux":
        #LINUX
        try:
            os.remove(file)
            #os.System("rm "+file) #alternative
            return True
        except Exception as exc:
            print e
            raise e

    elif _platform == "darwin":
        #OSX
        try:
            os.remove(file)
            #os.System("rm "+file) #alternative
            return True
        except Exception as exc:
            print e
            raise e

    else:
        print "ERROR! OS not supported! Oh no!.\nOS found: "+str(_platform)+"\nExiting...."
        #return False
        exit()


def checkFiles2():
    """Supports getMoveOrders2(), overwriting files"""

    for moveOrder in getMoveOrders2():
        ##print "Checking for files...."
        filenames = getFiles(FILES_LOCATION) #TODO: Make this get called less often

        ####### WITH END OPERATOR
        if len(moveOrder) is 3:
            #If the move order is three (end operator found), do search like this

            print "\nChecking for matches with '"+moveOrder[0]+"'...'"+moveOrder[1]+"'"

            for filename in filenames: #Iterate through the list of files
                if filename.startswith(moveOrder[0]) and filename.endswith(moveOrder[1]):
                    print "\tFound a match!\n\t\t"\
                         +"Filename:\t{0}\n\t\t".format(filename)\
                         +"Match Criteria:\t{0} ... {1}\n\t\t".format(moveOrder[0],moveOrder[1])\
                         +"Move Location:\t{0}\n".format(moveOrder[2])

                    if filename in getFiles(moveOrder[2].encode('utf8')):
                        print "WARNING - Duplicate of '"+filename+"' found in '"+ moveOrder[2]

                        if OVERWRITE_DUPLICATE_FILES:
                            print "WARNING - Overwriting file"
                            removeFile(moveOrder[2]+'/'+filename)
                            moveFile(FILES_LOCATION,filename,moveOrder[2],True)

                        else:
                            print "WARNING - Skipping file"

                    else:
                        moveFile(FILES_LOCATION,filename,moveOrder[2])

        elif len(moveOrder) is 2:
            #If the move order is three (end operator found), do search like this

            print "Checking for matches with '"+moveOrder[0]+"'"

            for filename in filenames: #Iterate through the list of files

                if filename.startswith(moveOrder[0]): #Check if filename matches what the move order asks for
                    print "\tFound a match!\n\t\t"\
                         +"Filename:\t{0}\n\t\t".format(filename)\
                         +"Match Criteria:\t{1}\n\t\t".format(moveOrder[0])\
                         +"Move Location:\t{2}\n".format(moveOrder[1])

                    if filename in getFiles(moveOrder[1]): #Get rid of \ chartecters to denote spaces. It fucks with getFiles.
                        print "WARNING - Duplicate of '"+filename+"' found in '"+ moveOrder[1]

                        if OVERWRITE_DUPLICATE_FILES:
                            print "WARNING - Overwriting file"
                            removeFile(moveOrder[1]+'/'+filename)
                            moveFile(FILES_LOCATION,filename,moveOrder[1],True)

                        else:
                            print "WARNING - Skipping file"

                    else:
                        moveFile(FILES_LOCATION,filename,moveOrder[1])

        else:
            print "ERROR! Move Order not recognised: '"+str(moveOrder)+"'\n Skipping it."


def unitTest():
    """tests functionality"""

    print "################################\n"\
        + "# WARNING! UNIT TESTS ENABLED! #\n"\
        + "################################\n"

    print "START OF TESTS\n"
    print "Prerequisites:\n"\
        + "\t- A source folder with files in it\n"\
        + "\t- A properly configured settings file\n"\
        + "\t- At least one valid move order\n"

    """stringToBool"""
    print "stringToBool()"
    for true_string in TRUE_STRINGS:
        if stringToBool(true_string):
            print "\tPASSED\tInput = "+true_string+" Output = TRUE"
        else:    
            print "\tFAILED\tInput = "+true_string

    for false_string in FALSE_STRINGS:
        if not stringToBool(false_string):
            print "\tPASSED\tInput = "+false_string+" Output = FALSE"
        else:
            print "\tFAILED\tInput = "+false_string

    """getMoveOrders2"""
    print "\ngetMoveOrders2()"

    orders = getMoveOrders2()
    print "\t\tOrders found:"
    for order in orders:
        print "\t\t\t"+str(order)
    if len(orders) is not 0:
        print "\tPASSED\tOrders Found = "+str(len(orders))
    else:
        print "\tFAILED\tOrders Found = "+str(len(orders))

    """getFiles"""
    print "\ngetFiles()"

    files = getFiles2(FILES_LOCATION)
    print "\t\tFiles Found:"
    for filename in files['filesandpaths']:
        print "\t\t\t"+str(filename)
    if len(files['filesandpaths']) is not 0:
        print "\tPASSED\tFiles Found = "+str(len(files['filesandpaths']))
    else:
        print "\tFAILED\tFiles Found = "+str(len(files['filesandpaths']))

    """getSettings"""
    print "\ngetSettings()"

    global AUTO_RECHECK
    AUTO_RECHECK = "TEST_VALUE"
    getSettings()
    if AUTO_RECHECK!="TEST_VALUE":
        print "\tPASSED\tAUTO_RECHECK Value = "+str(AUTO_RECHECK)
    else:
        print "\tFAILED\tAUTO_RECHECK Value = "+str(AUTO_RECHECK)


    print "\nEND OF TESTS"



##PROGRAM START
print "~~~~~~~~~~~~~~~~~~~~~~\n"\
     +"~   fileMover v0.1   ~\n"\
     +"~~~~~~~~~~~~~~~~~~~~~~\n"



#print(fileSearcher('C://test'))


if UNIT_TEST_ENABLE:
    getSettings()
    unitTest()
    exit()

while True:

    getSettings() #Get user settings before anything happens.

    #checkFiles() #do the check
    checkFiles2() #New checker with end operator support.

    if AUTO_RECHECK:
        rctime = datetime.datetime.now()+datetime.timedelta(seconds=RECHECK_MINS*60)
        printtime = str(rctime.hour)+":"+str(rctime.minute)+":"+str(rctime.second)

        print "\nFINSHED CHECKING. WILL CHECK AGAIN AT "+printtime
        time.sleep(RECHECK_MINS*60)

    else:
        break

print "\nFinished!"
##PROGRAM END                               
