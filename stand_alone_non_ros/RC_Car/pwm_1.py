try:
    while True:
        
        
        # throttle
        k = input()
        if k == 'w':
            print('forward')
        elif k == 'x':
            print('backward')
        elif k == 's':
            print('stop')
        else:
            print('neutral')
        
        
        # steer
        k = input()
        if k == 'a':
            print('left')
        elif k == 'd':
            print('right')
        else:
            print('center')
finally:
    #GPIO.cleanup()
    print('Goodbye')