# maya_ultimate.py

import os
import datetime
import webbrowser
import speech_recognition as sr
import pyttsx3
import pyautogui
import keyboard
import psutil
import requests
import subprocess
import json
import threading
import time
import cv2
from deepface import DeepFace
from googletrans import Translator
import openai

# === CONFIGURATION ===
openai.api_key = "your_openai_api_key_here"  # Replace with your key
GITHUB_UPDATE_URL = "https://raw.githubusercontent.com/your_user/your_repo/main/maya_ultimate.py"

# === INIT ===
recognizer = sr.Recognizer()
engine = pyttsx3.init()
translator = Translator()
language = 'hi'


def speak(text):
    translated = translator.translate(text, dest=language).text
    engine.say(translated)
    engine.runAndWait()


def greet_user():
    hour = datetime.datetime.now().hour
    greeting = "राम राम! MAYA सक्रिय है। बताइए कैसे मदद करूँ?"
    speak(greeting)


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio, language="hi-IN")
        return query.lower()
    except Exception:
        return ""


def open_website(site):
    webbrowser.open(site)
    speak("लो खोल दिया")


def control_apps(command):
    if "notepad" in command:
        subprocess.Popen("notepad.exe")
    elif "chrome" in command:
        subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    else:
        speak("मुझे वो ऐप नहीं मिला")


def write_text(text):
    pyautogui.write(text)
    pyautogui.press('enter')


def update_from_github():
    try:
        r = requests.get(GITHUB_UPDATE_URL)
        if r.status_code == 200:
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(r.text)
            speak("अपडेट पूरा हुआ")
        else:
            speak("कोई नया अपडेट नहीं मिला")
    except:
        speak("अपडेट चेक करते समय त्रुटि हुई")


def detect_face_emotion():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("face.jpg", frame)
        try:
            analysis = DeepFace.analyze(img_path="face.jpg", actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
            speak(f"आप {emotion} लग रहे हैं")
        except:
            speak("चेहरा पहचानने में समस्या हुई")
    cap.release()
    cv2.destroyAllWindows()


def chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are MAYA, a helpful multilingual assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        speak(reply)
    except:
        speak("उत्तर पाने में समस्या हुई")


def background_tasks():
    while True:
        time.sleep(3600)
        update_from_github()


def main():
    greet_user()
    threading.Thread(target=background_tasks, daemon=True).start()
    while True:
        print("Listening...")
        query = listen()
        print(f"Command: {query}")

        if "गूगल खोलो" in query:
            open_website("https://www.google.com")
        elif "नया टैब" in query:
            pyautogui.hotkey("ctrl", "t")
        elif "फेस पहचानो" in query:
            detect_face_emotion()
        elif "लिखो" in query:
            speak("क्या लिखूं?")
            text = listen()
            write_text(text)
        elif "अपडेट चेक करो" in query:
            update_from_github()
        elif "बोलो" in query:
            chatgpt_response(query)
        elif "बंद हो जाओ" in query:
            speak("ठीक है, अलविदा")
            break
        elif query != "":
            chatgpt_response(query)


if __name__ == "__main__":
    main()
