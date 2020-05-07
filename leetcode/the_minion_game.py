vowels = {"A", "E", "I", "O", "U"}
def minion_game(string):
    s_score = 0
    k_score = 0
    l = len(string)
    for i, a in enumerate(string):
        if a in vowels:
            s_score += l - i
        else:
            k_score += l - i
            
    print(s_score, k_score)

if __name__ == '__main__':
    minion_game("BANANA")
    minion_game("BANANANAAAS")