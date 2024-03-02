import argparse
import random
import urllib.request

from cowsay import *

def bullscows(guess: str, secret: str) -> (int, int):
    """
    возвращает количество «быков» и «коров» из guess в secret
    bullscows("ропот", "полип") -> (1, 2) («о» — бык, «о» и «п» — коровы)
    """
    c = 0
    b = 0
    
    g = list(guess)
    g_set = set(g)
    
    s = list(secret)
    s_set = set(s)
    
    c = len(g_set & s_set)
    
    for i in range(len(g)):
        if g[i] == s[i]:
            b += 1
            
    return (b, c)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    """
    функция-приложение, обеспечивающая геймплей:
        Задумывает случайное слово из списка слов words: list[str]
        Спрашивает у пользователя слово с помощью функции ask("Введите слово: ", words)
        Выводит пользователю результат с помощью функции inform("Быки: {}, Коровы: {}", b, c)
        Если слово не отгадано, переходит к п.1 
        Если слово отгадано, возвращает количество попыток — вызовов ask()
    """
    ask_cnt = 0
    b = 0
    secret = random.choice(words)
    # print(secret)
    
    while b != len(secret):
        guess = ask("Введите слово: ", words)
        ask_cnt += 1

        (b, c) = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        if b == len(secret):
            print('Попыток: ', ask_cnt)
            break
    
    return ask_cnt

def ask(prompt: str, valid: list[str] = None) -> str:
    """
    Если необязательный параметр valid не пуст, 
    допустим только ввод слова из valid, иначе спрашивает повторно
    
    ask("Введите слово: ", words)
    """
    if valid:
        while True:
            tmp = input(cowsay(prompt, cow = get_random_cow()))
            if tmp in valid:
                break
    else:
        tmp = input(cowsay(prompt, cow = get_random_cow()))
    
    return tmp

def inform(format_string: str, bulls: int, cows: int) -> None:
    """
    inform("Быки: {}, Коровы: {}", b, c)
    """
    print(cowsay(format_string.format(bulls, cows), cow = get_random_cow()))

def download_words(url):
    with urllib.request.urlopen(url) as response:
        words = response.read().decode('utf-8').splitlines()
    return words

def choose_words(words, length):
    valid_words = [word for word in words if len(word) == length]
    return valid_words

def main():
    parser = argparse.ArgumentParser(description='Bulls and Cows game.')
    parser.add_argument('dictionary', help='Name of the file or URL containing words')
    parser.add_argument('length_w', nargs = '?', type=int, default=5, help='Length of the words (default: 5)')

    args = parser.parse_args()
    
    if args.dictionary.startswith('http'):
        words = download_words(args.dictionary)
    else:
        with open(args.dictionary, 'r') as file:
            words = file.read().splitlines()

    if not words:
        print('Error: Empty dictionary')
        return
    
    valid_words = choose_words(words, args.length_w)
    
    gameplay(ask, inform, valid_words)
    
    
if __name__ == '__main__':
    main()