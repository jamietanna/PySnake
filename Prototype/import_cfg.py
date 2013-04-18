import sys
sys.path.append('/config') # need to add it to the system path to be able to import from inside a folder
import configparser

currentLevel = 'Level_One'

config = configparser.RawConfigParser()
config.add_section(currentLevel)
config.set(currentLevel, 'level_name', 'Level One')
config.set(currentLevel, 'max_balls', '5')
config.set(currentLevel, 'FPS', '20')

currentLevel = 'Level_Two'

config.add_section(currentLevel)
config.set(currentLevel, 'level_name', 'Level Two')
config.set(currentLevel, 'max_balls', '10')
config.set(currentLevel, 'FPS', '20')


# Writing our configuration file to 'example.cfg'
with open('levels.cfg', 'wb') as configfile:
    config.write(configfile)



config.read('levels.cfg')
levelName = config.get(currentLevel, 'level_name')
# getfloat() raises an exception if the value is not a float
# getint() and getboolean() also do this for their respective types
#a_float = config.getfloat('Section1', 'a_float')
max_balls = config.getint(currentLevel, 'max_balls')
print max_balls
print levelName

# Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
# This is because we are using a RawConfigParser().
#if config.getboolean('Section1', 'a_bool'):
#    print config.get('Section1', 'foo')