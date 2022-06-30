import camera
# from camera_corridor import Corridor

# als old
import old

if __name__ == '__main__':
    print( " === Starting Program === " )
    
    # als old
    cam = old.Camera()
    cam.video_blob_direction()

    cam = camera.Camera()
    cam.video_blob_direction()


    print("done with main function :)")