
#main.py
import cv2 as cv
import numpy as np
import os
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
 


# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - Wildy W4lker')


# initialize the Vision class

enemy_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\video processing attempt 2\\image library\\cow\\cow3.png')
combat_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\video processing attempt 2\\image library\\cow\\remaining_health.png')

loop_time = time.time()
confidence_counter = 0 #every time it thinks we're out of combat, the counter goes up. when it hits a threshold, we find a new thing to fight
heelCooler = time.time() # used to wait a bit before reclicking an enemy

while(True):
    #take a screenshot
    screenshot = wincap.get_screenshot()

    # get an updated image of the game and look for active combat bar
    combat = combat_vision.find(screenshot, 0.90, 'rectangles')


    #if it can see the combat bar, it will return coords of the bar in a list
    if combat != []:
        confidence_counter = 0
        print("in combat")

    #if it can't see combt bar, it returns empty list
    if combat == []:
        confidence_counter += 1
        print("enemy might be dead, counter is %s" % str(confidence_counter))
    
    if confidence_counter >= 20:
        # find more enemy points
        print("we're pretty sure he's dead, finding another enemy...")
        enemyWindowCoords = enemy_vision.find(screenshot,0.6, 'rectangles')
        if enemyWindowCoords != [] and (time.time() - heelCooler) >4: 
            heelCooler = time.time() #this means it won't reclick in under 4 seconds 
            print('found enemy')
            enemyScreenCoords= wincap.get_screen_position(enemyWindowCoords)
            pyautogui.moveTo(enemyScreenCoords)
            time.sleep(np.random.normal(.1,.02))
            pyautogui.click()
            print('clicked enemy')                  
            
    
    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')