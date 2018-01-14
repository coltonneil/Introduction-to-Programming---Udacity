import random
import sys
import time
import pickle

# declare data to be used
difficultyList = ['Easy', 'Regular', 'Hard', 'Brutal']
scoreMultiplier = {'Easy': 0.5,
                   'Regular': 1.0,
                   'Hard': 1.5,
                   'Brutal': 3.0}
score = 0
scores = []
chances = 3
questionValue = 20
quizData = {
    'Easy': {
        'question': '___1___ statements determine which code gets executed. ___1___ statements are the main selection tool in python and are used extensively throughout any program. An ___1___ statement can be arbitrarily complex by using ___2___ which allows you to check additional logic when the previous check evaluates to ___3___. You can also use ___4___ as a catch all in case all previous test fail.',
        'key': ('if', 'elif', 'false', 'else'),
        'slots': ('___1___', '___2___', '___3___', '___4___')
    },
    'Regular': {
        'question': 'A ___1___ is an ___2___ collection of objects. It can contain any number of objects and can be arbitrarily nested. Objects within a ___1___ are accessed by ___3___ and are not actually stored within the ___1___ but are actually references to objects. This can cause some confusion, if an object that is contained in a ___1___ is changed outside of the ___1___ the change will be reflected inside the ___1___. Because of this it can often be useful to use a ___4___ when you need the feature set of a list without the mutability',
        'key': ('list', 'ordered', 'offset', 'tuple'),
        'slots': ('___1___', '___2___', '___3___', '___4___')
    },
    'Hard': {
        'question': 'A ___1___ is an ___2___ collection of objects that are accessed by ___3___ / ___4___ pairs. A ___1___ can store any number of objects and is arbitrarily nestable which allows for representation of complex data structures. Using a ___1___ can make for more human friendly data than a list which is simply accessed by ___5___ for example ___1___[___3___] is generally more readable list[index].',
        'key': ('dictionary', 'unordered', 'key', 'value', 'offset'),
        'slots': ('___1___', '___2___', '___3___', '___4___', '___5___')
    },
    'Brutal': {
        'question': 'The ___1___ module is invaluable when trying to store and access python data structures in a ___2___. Normally anything written to or read from a ___2___ in python is a ___3___, but by using ___1___ you can store things like lists, tuples, and dictionaries in a ___2___ using ___1___.___4___(data, ___2___) and then retrieve that data using ___1___.___5___(___2___). However, ___1___ is not available by default and must be included using "___6___ ___1___".',
        'key': ('pickle', 'file', 'string', 'dump', 'load', 'import'),
        'slots': ('___1___', '___2___', '___3___', '___4___', '___5___', '___6___')
    },
}
helpText = 'Welcome to the fill in the blanks quiz. The premise of the game is simple, you will be presented some text with several words removed, to earn points you must correctly guess which word belongs in the corresponding spot. Each question will give you three attempts, the first attempt will give you full points, the second attempt will give you half, and the third will earn 0. There are varying difficulties available, the higher the difficulty the higher the point multiplier.'

# print program intro, name of the program and author name
def intro():
    print
    print '-' * 27
    print '| Fill in the blanks quiz |'
    print '|     Colton Williams     |'
    print '-' * 27
    print
    initializeScores()
    mainMenu(True)

# prints out the main menu and allows user to select an option, takes parameter initialRun
# (boolean determines if the menu is printed)
def mainMenu(initialRun):
    if initialRun:
        print '-- Main menu --\n[1] - Start a new game\n[2] - View high scores\n[3] - Help\n[4] - Quit'
    choice = raw_input('Please choose an option:')
    if choice == '1':
        chooseDifficulty(True)
    elif choice == '2':
        viewScores()
    elif choice == '3':
        gameHelp()
    elif choice == '4':
        typePhrase('Goodbye', True)
    else:
        typePhrase('Invalid input', True)
        mainMenu(False)

# creates scores.txt if it does not already exist and populated it with
# the default scores
def initializeScores():
    try:
        scoreData = open('scores.txt', 'r')
        global scores
        scores = pickle.load(scoreData)
        scoreData.close()
    except IOError:
        scoreData = open('scores.txt', 'w')
        pickle.dump([['AAA', 0], ['AAA', 0], ['AAA', 0],
                     ['AAA', 0], ['AAA', 0]], scoreData)
        scoreData.close()
        initializeScores()

# prints the high scores stored in the scores.txt file
def viewScores():
    global scores
    typePhrase('\nHigh scores:', True)
    for item in scores:
        print item[0] + ' - ' + str(item[1])
    raw_input('Press any key to return to the main menu')
    print
    mainMenu(True)

# print the helpText which includes a brief overview of how the game works
def gameHelp():
    global helpText
    print helpText
    raw_input('Press any key to return to the main menu')
    print
    mainMenu(True)

# prompts user to select a difficulty from the difficultyList, takes
# parameter initial (boolean to determine whether or not to print the
# list)
def chooseDifficulty(initial):
    if initial:
        for index, option in enumerate(difficultyList):
            print '[' + str(index + 1) + '] - ' + str(option) + ' (Score x ' + str(scoreMultiplier[option]) + ')'
            if index == len(difficultyList) - 1:
                print '[' + str(index + 2) + '] - Return to the Main menu'
    typePhrase('Please choose a difficulty: ', False)
    choice = raw_input()
    try:
        choice = int(choice)
    except ValueError:
        choice = 0
    if choice > 0 and choice < len(difficultyList) + 1:
        setDifficulty(choice)
    elif choice == len(difficultyList) + 1:
        mainMenu(True)
    else:
        typePhrase('Invalid input', True)
        chooseDifficulty(False)

# sets the difficuly based on user choice, takes parameter choice (int that
# is greater than 0 but less than the length of the difficultyList)
def setDifficulty(choice):
    choice -= 1
    if choice == len(difficultyList) - 1:
        if confirmBrutal():
            playGame(difficultyList[choice], 0)
        else:
            chooseDifficulty(False)
    else:
        playGame(difficultyList[choice], 0)

# double check that user meant to select the hardest difficulty, included
# to lighten the mood
def confirmBrutal():
    typePhrase('Seriously? Are you sure?(y/n): ', False)
    firstConfirm = raw_input()
    if firstConfirm.lower() == 'y':
        typePhrase(
            'Think about your family! Do you really want to do this!?(y/n): ', False)
        secondConfirm = raw_input()
        if secondConfirm.lower() == 'y':
            return True
        else:
            return False
    else:
        return False

# starts the game, takes parameters difficulty (a string from
# difficultyList) and stage (an int to determine which blank we are
# filling)
def playGame(difficulty, stage):
    global score
    if stage == 0:
        typePhrase('game started with difficulty: ' + difficulty, True)
        print ''
    print quizData[difficulty]['question']
    getScore('Current')
    poseQuestion(difficulty, stage, 1)

# asks the question and gets a response, takes parameters difficulty (a
# string from difficultyList), stage (an int to determine which blank
# we are filling), and attempt (an int to determine how many tries the user
# has left)
def poseQuestion(difficulty, stage, attempt):
    typePhrase('\nWhat belongs at ' +
               quizData[difficulty]['slots'][stage] + '? (Attempt ' + str(attempt) + ' of ' + str(chances) + ')', True)
    response = raw_input()
    checkAnswer(difficulty, stage, response, attempt)

# takes the user response and checks it against the expected answer for the current question and stage, takes parameters difficulty (a
# string from difficultyList), stage (an int to determine which blank
# we are filling), response (a string containing the data entered by the user), and attempt (an int to determine how many tries the user
# has left)
def checkAnswer(difficulty, stage, response, attempt):
    if response.lower() == quizData[difficulty]['key'][stage]:
        typePhrase('\nCorrect!', True)
        setScore(difficulty, attempt)
        advance(difficulty, stage)
    elif response.lower() == 'quit':
        return
    else:
        if attempt == chances:
            typePhrase('\nIncorrect, that was the final attempt, the correct answer was: ' +
                       quizData[difficulty]['key'][stage], True)
            advance(difficulty, stage)
        else:
            typePhrase('Incorrect! Try again', True)
            poseQuestion(difficulty, stage, attempt + 1)

# moves the user to the next stage, takes parameters difficulty (a
# string from difficultyList) and stage (an int to determine which blank
# we are filling and therefore which blank is next)
def advance(difficulty, stage):
    quizData[difficulty]['question'] = quizData[difficulty]['question'].replace(
        quizData[difficulty]['slots'][stage], quizData[difficulty]['key'][stage])
    if stage < len(quizData[difficulty]['slots']) - 1:
        typePhrase('Advancing to the next round\n', True)
        playGame(difficulty, stage + 1)
    else:
        typePhrase('Game Complete', True)
        getScore('Final')

# included to give the game a more retro feel by having text appear as if
# it is being typed, takes parameters phrase (a string containing what you
# want printed) and newLine (a boolean to determine if we include a line
# return or not)
def typePhrase(phrase, newline):
    phraseList = list(phrase)
    for item in phraseList:
        sys.stdout.write(item)
        num = random.random()
        time.sleep(num / 30)
    if newline:
        print ''

# increments score by multiplying the value of the question with the
# difficulty multiplier and halves the value if they missed the first
# attempt, takes parameters difficulty ( a string from difficultyList to
# determine the multiplier to use) and attempt (an int to determine
# whether to give full or half credit)
def setScore(difficulty, attempt):
    global score, questionValue
    if attempt == 1:
        score += questionValue * scoreMultiplier[difficulty]
    elif attempt == 2:
        score += questionValue / 2 * scoreMultiplier[difficulty]

# returns the users score, takes parameter type (string 'Current'/'Final'
# to format the string for readability)
def getScore(type):
    global score
    typePhrase('\n' + type + ' score is: ' + str(score), True)
    if type == 'Final':
        checkScore(score)


# determines whether the final score is a new record and if it is get user
# initials and call saveScore(), takes parameter score (int representing
# the users score)
def checkScore(score):
    global scores
    maxIntialLength = 3
    index = 0
    for item in scores:
        if score > item[1]:
            typePhrase('New high score!', True)
            typePhrase('Please enter '+str(maxIntialLength)+' characters for your initials: ', False)
            initials = raw_input()
            while len(initials) != maxIntialLength:
                typePhrase(
                    'Invalid, please enter '+str(maxIntialLength)+' characters for your initials: ', False)
                initials = raw_input()
            scores[index:index] = [[initials.upper(), score]]
            scores = scores[:-1]
            saveScore(scores)
            break
        index += 1

# saves high scores to scores.txt, takes parameter scores (int
# representing users score)
def saveScore(scores):
    scoreData = open('scores.txt', 'w')
    pickle.dump(scores, scoreData)
    scoreData.close()

#begins program
intro()
