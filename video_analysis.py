from dotenv import load_dotenv
import google.generativeai as genai
import os
import time


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def upload_video(video_file_name):
    print(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name)
    print(f"Completed upload: {video_file.uri}")

    while video_file.state.name == "PROCESSING":
        print('Waiting for video to be processed.')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    print(f'Video processing complete: ' + video_file.uri)

    return video_file


def generate_gemini_response(video_file):
    # Get the prompt.
    prompt = input("Enter your prompt: ")
    if prompt == "exit":
        return 0

    # Set the model to Gemini 1.5 Pro.
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

    # Make the LLM request.
    print("Making LLM inference request...")
    response = model.generate_content([prompt, video_file],
                                    request_options={"timeout": 600})
    return response.text

def delete_video(video_file):
    genai.delete_file(video_file.name)
    print(f'Deleted file {video_file.uri}')
    

def main():
    video_file = upload_video("videos\\aihiringtrends.mp4")
    while True:
        response = generate_gemini_response(video_file)
        if response == 0:
            break
        print(response)
    
    response = input("Delete video? (y/n): ")
    if response == "y":
        delete_video(video_file)
        
        
if __name__=="__main__":
    main()