import cv2
import numpy as np
import argparse

# The below code is modified from groupgets official github repo: https://github.com/groupgets/purethermal1-uvc-capture/blob/master/python/uvc-radiometry.py
def y16_to_8bit(data):
    '''
    Converts the Y16 format data to RGB888.
    Parameters:
        Input:
            data : 16 bit numpy array of incoming frame data.
        Return:
            rgb_data : Converted RGB data.
    '''
    cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)        
    np.right_shift(data, 8, data)                               
    rgb_data = cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)     
    return rgb_data

                
def main():
    '''
    Main Program.
    Parameters:
        input : Camera node number of Pure thermal camera.
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=int, default=0, help='Input device camera node number')
    args = parser.parse_args()

    device_index = int(args.input)
    cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    cap = cv2.VideoCapture(device_index,cv2.CAP_V4L2)    
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)

    # Querying Y16 format
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','1','6',' '))
    cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
    
    while True:
        try:
            stream_ret, frame = cap.read()
            frame = cv2.resize(frame[:,:], (640, 480))  # (optional) to upscale the thermal camera feed to 640x480
            img = y16_to_8bit(frame)
            img = cv2.GaussianBlur(img,(5,5),0)         # (optional) to smooth the thermal camera feed
            
            if stream_ret == False:
                break
            
            cv2.imshow('image',img)

            if cv2.waitKey(1) == ord('q'):              # Stop the streaming if button 'q' is pressed
                break
            
        except Exception as e:
            print("exception is %s"%str(e))
            break
        
    cap.release()
    cv2.destroyAllWindows()    


if __name__ == "__main__":
    main()
