import camera
from camera_corridor import Corridor

if __name__ == '__main__':
    print( " === Starting Program === " )
    
    corridor = Corridor()
    cam = camera.Camera()
    cam.video_blob_direction()
    cam.juno_detection()