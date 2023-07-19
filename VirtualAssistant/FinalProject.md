# Overview

I created a virtual assistant program that listens for various trigger words then executes a command.

I wrote this program mainly to challenge myself, and venture into the realm of truly useful softwares.
Additionally, I am building a smart mirror with a raspberry pi and would like to use this program as a 
way to interact with the smart mirror.


[Software Demo Video](https://youtu.be/OSh6a7sGPbg)

# Development Environment

I used visual studio code to create this software

This program is written in python. I used quite a few different libraries including speech_recognition, 
word2number, pyttsx3, pyjokes, requests, time, and threading


# Useful Websites

- [SpeechRecognition 3.10.0](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 2.90](https://pypi.org/project/pyttsx3/)

# Future Work

- The biggest problem I faced is words that sound similar. I had to make several workarounds to make sure words didn't get mixed up.
  For example, I had a method named set timer with the trigger word of timer, but it kept thinking I was saying time, so it would call the speak_time method instead.
- Add more commands. I want to make this relatively expansive and personalized.
- I would like to get a custom voice instead of using Windows' built in voices. There are other python libraries that allow for this, so I would just have to download and 
  implement those.