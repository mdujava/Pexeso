from pexeso import *
from engine import *
import time


def main(debug = False, numberOfGames = 1000, numberOfPairs = 50, sizeOfMemory = 100, brakPoint = 100):
    startTime = time.time()
    dateStart = time.time()


    scoreA = 0
    scoreB = 0
    draw = 0
    debug = debug

    half = (numberOfPairs*2 + 1)/2

    for x in range(1, numberOfPairs*2 + 1):
        scoreA = 0
        scoreB = 0
        draw = 0
        print("start: " + str(x))
        print(str(time.time() - dateStart) + "\n")
        f = open('mem-mem-' + str(numberOfGames) + '-' + str(numberOfPairs) + '-pam-' + str(x) + '-' + str(sizeOfMemory)  + '.csv', 'w')
        for i in range(0, numberOfGames):
            game = Game(numberOfPairs, debug)
            
            engineOne = EngineMemory(game, x)
            engineTwo = EngineMemory(game, sizeOfMemory)
            #engine = EngineMemory(game, sizeOfMemory)

            if x < half:
                game.inicializeEngines(engineOne, engineTwo)
            else:
                game.inicializeEngines(engineTwo, engineOne)
            

            #game.playOneEngine()
            returnedThing = game.playTwoEngine()

            if len(returnedThing) == 3:
                debug = False

            if x < half:
                string = str(returnedThing[0]) + "," +  str(returnedThing[1])
            else:
                string = str(returnedThing[1]) + "," +  str(returnedThing[0])

            # calculate 
            if x < half:
                if returnedThing[0] > returnedThing[1]:
                    scoreA += 1
                elif returnedThing[0] < returnedThing[1]:
                    scoreB += 1
                else:
                    draw += 1
            else:
                if returnedThing[1] > returnedThing[0]:
                    scoreA += 1
                elif returnedThing[1] < returnedThing[0]:
                    scoreB += 1
                else:
                    draw += 1

            f.write(string + '\n')

            # print gps
            if i % brakPoint == brakPoint - 1:
                print("--- %s games per second ---" % (brakPoint/(time.time() - startTime)))
                startTime = time.time()

        f.write(str(scoreA) + "\n")
        f.write(str(scoreB) + "\n")
        f.write(str(draw) + "\n")

        f.close()

    dateEnd = time.time()

    f = open('stats.txt', 'w')
    f.write(str(dateStart) + "\n")
    f.write(str(dateEnd) + "\n")
    f.write(str((dateEnd - dateStart)/3600) + "hod\n")
    f.write(str((dateEnd - dateStart)/60) + "min\n")
    f.write(str((dateEnd - dateStart)%60) + "sec\n")
    f.close()

if __name__ == '__main__':
    main()