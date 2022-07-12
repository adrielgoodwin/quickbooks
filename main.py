from vosk import Model, KaldiRecognizer
import pyaudio
from pynput.keyboard import Key, Controller
import pyautogui

model = Model(r"C:\Users\Anna\PycharmProjects\pythonProject\vosk-model-eng")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

keyboard = Controller()


def tab():
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)


def enter():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    tab()


def selectDebitClearing():
    pyautogui.write("deb")
    tab()


def card(cardType, batch, amount):
    pyautogui.write(f'Deposit-Moneris {batch}')
    tab()
    tab()
    selectDebitClearing()
    pyautogui.write(f'Moneris Batch {batch}')
    tab()
    tab()
    pyautogui.write(cardType)
    tab()
    pyautogui.write(amount)


def cheque(amount):
    tab()
    tab()
    selectDebitClearing()
    pyautogui.write('Cheque deposit - ATM')
    tab()
    tab()
    pyautogui.write('Cheque')
    tab()
    pyautogui.write(amount)


def addCashDeposit(amount):
    tab()
    tab()
    selectDebitClearing()
    pyautogui.write("Cash")
    tab()
    tab()
    pyautogui.write("cash")
    tab()
    pyautogui.write(amount)


def pettyCash(amount):
    tab()
    tab()
    pyautogui.write("Pett")
    tab()
    pyautogui.write("Replenish petty cash")
    tab()
    tab()
    pyautogui.write("cash")
    tab()
    pyautogui.write(f'-{amount}')


def drawings(amount):
    tab()
    tab()
    pyautogui.write("D Goo")
    tab()
    pyautogui.write("Cash drawings")
    tab()
    tab()
    pyautogui.write("cash")
    tab()
    pyautogui.write(f'-{amount}')


def eft(amount):
    # top memo
    pyautogui.write('Deposit - EFT')
    tab()
    tab()
    selectDebitClearing()
    # line memo
    pyautogui.write('EFT reciept')
    tab()
    tab()
    # pmt method
    pyautogui.write('EFT')
    tab()
    # amount
    pyautogui.write(amount)


def date(month, day, year):
    pyautogui.write(f'{monthNumbers[month]}/{day}/{year}')
    tab()


monthNumbers = {
    "january": '01',
    "february": '02',
    "march": '03',
    "april": '04',
    "may": '05',
    "june": '06',
    "july": '07',
    "august": '08',
    "september": '09',
    "october": 10,
    "november": 11,
    "december": 12,
}

numbers = {
    "zero": 0,
    "one": 1,
    "to": 2,
    "too": 2,
    "two": 2,
    "three": 3,
    "four": 4,
    "before": 4,
    "for": 4,
    "or": 4,
    "five": 5,
    "six": 6,
    "sticks": 6,
    "sex": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "dying": 9,
    "time": 9,
    "ten": 10,
    "dot": '.',
    "dots": '.',
    "dog": '.',
    "dogs": '.',
    "door": '.',
    "taught": '.',
    "diet": '.',
    "dodge": '.',
}


def combineNumbers(textNumbers):
    combinedNumber = ''
    for n in textNumbers:
       combinedNumber += f'{numbers[n]}'
    return combinedNumber


def checkIfNumbersAreGood(textNumbers):
    for n in textNumbers:
        if n in numbers:
            continue
        else:
            return False
    return True


while True:
    data = stream.read(4096)
    year = 21
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text)
        phrase = text[14: -3].split()
        if len(phrase) > 0:
            if phrase[0] == "visa" or phrase[0] == "mastercard" or phrase[0] == "interact":
                if len(phrase) > 1:
                    amt = phrase[4:]
                    if checkIfNumbersAreGood([phrase[1], phrase[2], phrase[3]]) and checkIfNumbersAreGood(amt):
                        batchNumber = combineNumbers([phrase[1], phrase[2], phrase[3]])
                        amt = combineNumbers(amt)
                        card(phrase[0], batchNumber, amt)
            if phrase[0] == "it" or phrase[0] == "date" or phrase[0] == "eight":
                if len(phrase) > 3:
                    if checkIfNumbersAreGood([phrase[2], phrase[3]]):
                        day = combineNumbers([phrase[2], phrase[3]])
                        date(phrase[1], day, year)
            if phrase[0] == "e":
                if len(phrase) > 4:
                    amt = phrase[3:]
                    if checkIfNumbersAreGood(amt):
                        amt = combineNumbers(amt)
                        eft(amt)
            if phrase[0] == "check" or phrase[0] == "cheque" or phrase[0] == "shaq":
                amt = phrase[1:]
                if checkIfNumbersAreGood(amt):
                    amt = combineNumbers(amt)
                    cheque(amt)
            if phrase[0] == "enter" or phrase[0] == "submit":
                enter()
            if phrase[0] == "tab" or phrase[0] == "tap" or phrase[0] == "out":
                tab()
            if phrase[0] == "cash" or phrase[0] == "ash":
                if phrase[1] == "petty":
                    amt = phrase[2:]
                    if checkIfNumbersAreGood(amt):
                        amt = combineNumbers(amt)
                        pettyCash(amt)
                elif phrase[1] == "drawings":
                    amt = phrase[2:]
                    if checkIfNumbersAreGood(amt):
                        amt = combineNumbers(amt)
                        drawings(amt)
                else:
                    amt = phrase[1:]
                    if checkIfNumbersAreGood(amt):
                        amt = combineNumbers(amt)
                        addCashDeposit(amt)

        # if phrase[0] == "set":
            #     if phrase[1] == "year":
            #


    # Settings: Command = "SETTINGS" -Moneris 551       deb Moneris Batch 551       visa    111.1
    # "Choose Year": say the year
    # Date: [Month, Day] "June 6"
    # Top Memo: [Type, [Number]] "Deposit", "EFT", "Moneris" => "335"
    # Amount: [Number] "1145.34"
