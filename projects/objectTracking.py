from imports import *

def select_tracker(tracker_type):
    if tracker_type == 'MIL':
        return cv.TrackerMIL_create()
    elif tracker_type == 'KCF':
        return cv.TrackerKCF_create()
    elif tracker_type == 'CSRT':
        return cv.TrackerCSRT_create()
    else:
        raise ValueError('Unsupported tracker type')
    
def main():
    tracker_types = ['MIL', 'KCF', 'CSRT']
    for i, tracking_type in enumerate(tracker_types, start=1):
        print("{} {}".format(i, tracking_type))
    tracker_choice = int(input("Select Tracking Type: ")) - 1
    tracker_type = tracker_types[tracker_choice]

    tracker = select_tracker(tracker_type)

    video  = cv.VideoCapture(0) # Just using webcam, you can change 0 into a different number and add functionality later
    if not video.isOpened():
        print("Error, Could not open video")
        sys.exit()
    
    ok, frame = video.read()
    if not ok:
        print("Error, Could not read video file")
        sys.exit()

    bounding_box = cv.selectROI(frame, False)
    ok = tracker.init(frame, bounding_box)

    while True:
        ok, frame = video.read()
        if not ok:
            break
        ok, bounding_box = tracker.update(frame)
        if ok:
            p1 = (int(bounding_box[0]), int(bounding_box[1]))
            p2 = (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3]))
            cv.rectangle(frame, p1, p2, (0,255,0), 2, 1)
        else:
            cv.putText(frame, "Tracking has failed", (100, 80), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv.putText(frame, tracker_type + " Tracker", (100,20), cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        
        cv.imshow("Tracking", frame)
        if cv.waitKey(1) & 0xFF == 27:
            break

    video.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
                          
