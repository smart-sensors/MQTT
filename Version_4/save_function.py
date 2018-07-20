#Import Libraries
from ConfigParser import*

#Initializes dictionary with options and assosiated values
value_list = {}

#Reads options and assosiated values
def read_config(SectionName):
    config = ConfigParser()
    config.read('config.ini')
    #Checks whether or not user defined section is found inside the configuation file
    section_flag = config.has_section(SectionName)

    if section_flag == True:
    #Creates a dictionary with options and assosiated values of user defined section found inside the configuation file
        for name, value in config.items(SectionName):
            value_list.update({name:value})

    return value_list

#Writes user defined Value to user defined section at a configuration file
def write_config(SectionName,Value):
    #initize valriables
    list_num = 0
    config = ConfigParser()

    config.read('config.ini')
    #Checks whether or not user defined section is found inside the configuation file
    section_flag = config.has_section(SectionName)

    #If user defined section is found inside the configuration file
    if section_flag == True:
        #Checks whether or not user defiend option is found inside the configuration file
        option_flag = config.has_option(SectionName,'%i' % list_num)

        #Increment save slot number to find available slots
        while option_flag:
            list_num = list_num + 1
            option_flag = config.has_option(SectionName,'%i' % list_num)
        #Initilize available save slot number
        option = ("%i" % list_num)

        #Checks wheter or not if the user defined value is founnd inside the configuration file
        for name, value in config.items(SectionName):
            if value == Value:
                same_flag = True
            else:
                same_flag = False

        #Writes the user defined value to available save slot
        if same_flag == False:
            config_file = open('config.ini','w')
            config.set(SectionName, option, Value)
            config.write(config_file)

    #If user defined section is not found, it creates a new section in the configuration file
    else:
        config_file = open ('config.ini','ab')
        config_update = ConfigParser()
        config_update.add_section(SectionName)
        #Writes user defined value into new section 
        config_update.set(SectionName,'%i' % list_num, Value)
        config_update.write(config_file)
