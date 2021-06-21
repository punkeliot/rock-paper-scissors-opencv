import cv2, numpy as np
import random
import time

win_name = 'Camera Matching'
MIN_MATCH = 10

detector = cv2.ORB_create(1000)

FLANN_INDEX_LSH = 6
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6,
                   key_size = 12,
                   multi_probe_level = 1)
search_params=dict(checks=32)
matcher = cv2.FlannBasedMatcher(index_params, search_params)

cap = cv2.VideoCapture(0)              
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

a = 0
b = 0
c = 0
turnos=[0,0,0]
comput=[0,0,0]
cont = 0

img1 = cv2.imread('piedra.jpg') 
img2 = cv2.imread('papel1.jpg') 
img3 = cv2.imread('tijera1.jpg') 


    
while cap.isOpened():       
       
    ret, frame = cap.read() 
    img = frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
     
    print(a)
    print(b)
    print(c)
   
    kp, desc = detector.detectAndCompute(gray, None)
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    kp2, desc2 = detector.detectAndCompute(gray2, None)
    kp3, desc3 = detector.detectAndCompute(gray3, None)
   
    matches1 = matcher.knnMatch(desc1, desc, 2)
    matches2 = matcher.knnMatch(desc2, desc, 2)
    matches3 = matcher.knnMatch(desc3, desc, 2)
    
    
    ratio = 0.75
    
    good_matches1 = [m[0] for m in matches1 \
                    if len(m) == 2 and m[0].distance < m[1].distance * ratio]
    good_matches2 = [m[0] for m in matches2 \
                    if len(m) == 2 and m[0].distance < m[1].distance * ratio]
    good_matches3 = [m[0] for m in matches3 \
                    if len(m) == 2 and m[0].distance < m[1].distance * ratio]    
    
        
    print('good matches 1:%d/%d' %(len(good_matches1),len(matches1)))
    print('good matches 2:%d/%d' %(len(good_matches2),len(matches2)))
    print('good matches 3:%d/%d' %(len(good_matches3),len(matches3)))
    
    
    matchesMask = np.zeros(len(good_matches1)).tolist()
    matchesMask = np.zeros(len(good_matches2)).tolist()
    matchesMask = np.zeros(len(good_matches3)).tolist()
    
   
    if (len(good_matches1)>10):
        a = a + len(good_matches1)
    if (len(good_matches2)>11):
        b = b + len(good_matches2)
    if (len(good_matches3)>10):
        c = c + len(good_matches3)    
  
    if (a>50 or b>50 or c>50):
        if(a>49):
            turnos[cont]=1
        elif(b>49):
            turnos[cont]=2
        elif(c>49):
            turnos[cont]=3
        
        a=0
        b=0
        c=0
        
        print('preparate para otro turno')
        time.sleep(5) 
        cont= cont+1
        if(cont==3):
            break
    
    
    cv2.imshow(win_name, frame)
    key = cv2.waitKey(1)
    if key == 27:    
            break          
            
else:
    print("can't open camera.")
cap.release()                          
cv2.destroyAllWindows()

simbolo = ['piedra','papel','tijera']

for i in range(3):
    print('turno',i+1)
    comput[i] = random.randrange(3)+1
    print('el jugador saco',simbolo[turnos[i]-1],' la computadora saco',simbolo[comput[i]-1])                                         #print('jugador:', simbolo[comput[i-1]],'computadora:', simbolo[turnos[i-1]])                 print('jugador:%d  computadora:%d' %(simbolo[comput[i-1]],turnos[i-1]))
print('')

puntosj=0
puntosc=0

for i in range(3): 
    
    jugad = turnos[i]
    compu = comput[i]
    
    print('en el juego #',i+1)
    if(jugad==compu):
        print('empate')
    else:
        if(jugad==1):
            if(compu==2):
                print('computadora gana')
                puntosc=puntosc+1 
            else:
                print('jugador gana')
                puntosj=puntosj+1
        elif(jugad==2):
            if(compu==3):
                print('computadora gana')
                puntosc=puntosc+1
            else:
                print('jugador gana')
                puntosj=puntosj+1
        else:
            if(compu==1):
                print('computadora gana')
                puntosc=puntosc+1
            else:
                print('jugador gana')
                puntosj=puntosj+1
print('')
print('')          
if(puntosc==puntosj ):
    print('EMPATE')
else:
    if(puntosc>puntosj):
        print('COMPUTADORA GANA')
    else:
        print('JUGADOR GANA')          