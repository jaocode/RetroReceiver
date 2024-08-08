# RetroReceiver
A Python script that attempts to receive programs transmitted during episodes of The Computer Program, a 1980s BBC show.

## Dependencies
### Python
Script was tested using Python 3.12.4 on MacOS. It should work on other platforms. 

### OpenCV 
Install using "python3 -m pip install opencv-python" 

### ffmpeg libraries
Likely required for loading video content with OpenCV. How you obtain them depends on the OS you're using. 

On MacOS, the libraries can be obtained using [Homebrew](https://brew.sh) package manager

On Linux distributions based on Debian,like Ubuntu, they can be installed via apt-get.

## Running the Script
Create input, ouput, frames/light and frames/dark folders where the retro_receiver script resides. 

Place the input video into the input folder. 

Update the settings block of the script to customize it for your input video. 

- Edit the vidcap line to point to an input video.
- start_timestamp: specifies the timestamp in seconds the script should begin analyzing frames.
- end_timestamp: specifies the timestamp in seconds the script stop analyzing frames.
- pixel_x and pixel_y: points the script to where it should be testing the video transmitted bits. 
- skip_frames: tells the script to skip looking at every other frame. May not be of real value. 
- ignore_header_bits: When true, the script attempts to ignore the leading '1' bits. It will start recording bits after the first '0'. May not be of real value.
- save_frames: When true, each analyzed frame is saved off and sorted into a folder based if the pixel test detected light or dark. Useful for debugging that all video frames properly interpreted. 
- brightness_threshold: Sets the threshold for the pixel test for what level of intensity should be considered light. May need to tweak this based on the quality of the video. 

Run the script using command "python3 retro-receiver.py"

## Output
When the script is finished running, a file called output.bin is created in the output folder. This is a binary file built from the bits interpreted from the video transmission. In theory, if all went well this would be a program that runs on a C64 or BBC Micro. 

The correctness of this output is questionable. There aren't any materials to test against and not much is known about how the binary transmissions were processed using original hardware. Due to the nature of how broadcast recordings work and digital video encoding, corruption my have been injected into the recordings themselves. Even the host of the show acknowledges they've gotten the transmission wrong before, so there is no gurantee the original broadcast transmitted a viable program.  
