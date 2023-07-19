import speech_recognition as sr
import commands as c
import time

def main():
    carry_on = True
    while carry_on:
        c.engine.setProperty('voice', c.voices[3].id) 
        wake_command = c.listen().lower()
        if "steve" in wake_command:
            c.wake_up()
            command = c.listen().lower()
            c.process_command(command)
        time.sleep(1)
        
if __name__ == "__main__":
    main()
