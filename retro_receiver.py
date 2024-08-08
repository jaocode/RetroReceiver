import cv2
from util.bit_writer import BitWriter as BW

def is_shade_of_white(pixel, threshold):
    # Check if all color channels are above the threshold
    return all(channel >= threshold for channel in pixel)

def timestamp_to_frame(timestamp, fps):
    # Convert timestamp (in seconds) to frame number
    return int(timestamp * fps)

#BEGIN=================SETTINGS=========================
vidcap = cv2.VideoCapture('./input/ENHANCED_C64.mp4')
start_timestamp = 0  # Start time in seconds
end_timestamp = 0 # End time in seconds
# Specify the pixel coordinates (x, y)
pixel_x = 254  # Replace with your desired x-coordinate
pixel_y = 187  # Replace with your desired y-coordinate

# Set to true to skip every other frame. May be helpful when for some broadcast conversions.
skip_frames = False
# Set to True to trim header bits
ignore_header_bits = False
# Set to save off each frame as .jpg sorted into light or dark folders
save_frames = True

brightness_threshold = 128 # Define your brightness threshold (0-255)
#END=================SETTINGS=========================

# Get video properties
fps = vidcap.get(cv2.CAP_PROP_FPS)
print (f'Video FPS: {fps}')

frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
print (f'Video total frames: {frame_count}') 

# Calculate the start frame from the timestamp
start_frame = timestamp_to_frame(start_timestamp, fps)
print (f'Transmission start frame: {start_frame}')

# Calculate the end frame from the timestamp
if end_timestamp != 0:
    end_frame = timestamp_to_frame(end_timestamp, fps)
else:
    end_frame = frame_count

print (f'Transmission end frame: {end_frame}')

count = start_frame

skip_frame = False

# Set the video capture to the start frame
vidcap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

success,image = vidcap.read()

bw = BW('./output/output.bin')

#For testing output
bit_stream_test = ''

while success:
    print (f'Checking frame: {count}')
    # Check if the coordinates are within the frame bounds
    if skip_frame == False:
        if pixel_y < image.shape[0] and pixel_x < image.shape[1]:
            # Get the color of the pixel (BGR format)
            pixel_color = image[pixel_y, pixel_x]
            
            # Determine if the pixel is white or black
            if is_shade_of_white(pixel_color, brightness_threshold):
                if save_frames:
                    cv2.imwrite("./frames/light/frame%d.jpg" % count, image)     # save frame as JPEG file     
                if ignore_header_bits == False:
                    bit_stream_test += '1'
                    bw.write_bit(1)
            else:
                if save_frames:
                    cv2.imwrite("./frames/dark/frame%d.jpg" % count, image)     # save frame as JPEG file     
                if ignore_header_bits == False:
                    bit_stream_test += '0'
                    bw.write_bit(0)
                ignore_header_bits = False
        else:
            print(f'Frame {count}: Pixel coordinates ({pixel_x}, {pixel_y}) are out of bounds')
 
    success,image = vidcap.read()
    #print('Read a new frame: ', success)
    count += 1
    if skip_frames:
        skip_frame = not skip_frame

    if (end_timestamp != 0) and (count > end_frame):
        break

bw.close()

# Release the video capture object
vidcap.release()
#print(bit_stream_test)
print("Frame extraction and pixel color checking completed.")