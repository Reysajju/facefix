# Install required libraries
!pip install flask opencv-python-headless face_recognition[cpu] moviepy

import cv2
import face_recognition
import moviepy.editor as mp
from flask import Flask, request, send_file
from google.colab import files  # Import the files module
import os

app = Flask(__name__)

@app.route('/process_video', methods=['POST'])
def process_video():
    # Install required libraries (remove duplicate installation)
    # !pip install opencv-python-headless
    # !pip install face_recognition[cpu]
    # !pip install moviepy

    # Ask the user to upload a video
    uploaded_video = files.upload()  # Use files.upload() for file upload in Colab
    uploaded_video_path = next(iter(uploaded_video))

    # Convert the video to 90 frames per second
    output_frames_folder = "frames"
    os.makedirs(output_frames_folder, exist_ok=True)

    clip = mp.VideoFileClip(uploaded_video_path)
    clip.write_images_sequence(f"{output_frames_folder}/frame%04d.jpg", fps=90)

    # Rest of your code...

    # Deblur faces in each frame
    for frame_file in os.listdir(output_frames_folder):
        frame_path = os.path.join(output_frames_folder, frame_file)

        # Load the frame
        image = cv2.imread(frame_path)

        # Find faces in the frame
        face_locations = face_recognition.face_locations(image)

        # Deblur each face
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face = image[top:bottom, left:right]

            # Apply Gaussian Blur for deblurring
            blurred_face = cv2.GaussianBlur(face, (15, 15), 0)

            # Replace the deblurred face in the original frame
            image[top:bottom, left:right] = blurred_face

        # Save the deblurred frame
        cv2.imwrite(frame_path, image)

    # Compile frames back to the original video with audio
    output_video_path = "output_video.mp4"
    clip = mp.ImageSequenceClip(f"{output_frames_folder}/", fps=90)
    clip.write_videofile(output_video_path, audio=uploaded_video_path)

    # Display the link to download the output video
    print(f"Video processed successfully! You can download it here: {output_video_path}")

    return send_file(output_video_path, as_attachment=True)

if __name__ == '__main__':
    # Run the Flask app on a specific port
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
