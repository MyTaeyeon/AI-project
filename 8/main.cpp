#include <iostream>
#include <cstring>
#include <iomanip>
#include <cstdlib>

using namespace std;

struct Point {
    short x;
    int _score;
};

enum Turn{ IMNOTHING, HUMAN, COMPUTER};

short board[1024]; // -1: the wall
                   //  0: the free square 
                   //  1: the square occupied by human
                   //  2: the square occupied by computer
short sz = 30;   // sz = correct_sz + 2
short bestMove = -1;

int maxScoreCom = 0, maxScoreHuman = 0;

// give score for each cell in the board
int caro[1024];

int max_depth = 6;
bool game_over = false;

short AttackScores[] = {0, 2, 18, 162, 1400};
short DefendScores[] = {0, 1,  9,  81,  729};

short exdirections[4]; /* 5 cells in row,
                          5 cells in column,
                          5 cells in diagonal from left,
                          5 cells in diagonal from right  
                        */

int max_element(int a[], int length) {
    int l = 0;
    for (int i = 1; i < length; i++)
        if (a[i] > a[l]) l = i;
    return l;
}

int min_element(int a[], int length) {
    int l = 0;
    for (int i = 1; i < length; i++)
        if (a[i] < a[l]) l = i;
    return l;
}

// set up the board and update size
void init(short n) {
    sz = n+2;
    memset(board, 0, sizeof(board));
    exdirections[0] = 1; exdirections[1] = sz;
    exdirections[2] = sz+1; exdirections[3] = sz-1;

    for (short i = 0; i < sz-2; ++i) board[i] = -1;
    for (short i = sz-1; i < sz*(sz-1); i += sz) {
        board[i] = -1;
        board[i+1] = -1;
    }
    for (short i = sz*(sz-1); i < sz*sz; i++) board[i] = -1;
}

// draw the board game 
void Render() {
    for (int i = sz; i < sz*(sz-1); i++) {
        switch (board[i])
        {
        case 0:
            cout << "|   ";break;
        case 1:
            cout << "| X ";break;
        case 2:
            cout << "| O ";break;
        default:
            break;
        }
        
        if (i % sz == sz-1) cout << "|\n";
    }
}

// Check to know the game is over
bool isWin(short key) {
    for (int i = sz; i < sz*(sz-1); i++) 
        for (short x: exdirections) {
            int cnt = 0;
            for (int j = 0; j < 5*x; j += x)
                if (board[i+j] == -1) break;
                else if (board[i+j] == key) cnt += 1;
                else break;
            if (cnt == 5) return true;
            else return false;
        }
    return false;
}

// fint best move
void giveScore(int dir, int _turn) {
    for (int cell = sz; cell < sz*(sz-1); cell++) {
        int cntCom = 0, cntHuman = 0;
        bool is_vain_effort = false;
        for (int l = 0; l < dir*5; l += dir) {
            if (board[cell + l] == -1) { // blocked by the wall
                is_vain_effort = true; 
                break;
            }
            if (board[cell + l] == 1) cntHuman++;
            else if (board[cell + l] == 2) cntCom++;
        }

        if (is_vain_effort) continue; 

        // Neither the computer nor the human can achieve a sequence of five stones.
        if (cntCom * cntHuman == 0 && cntHuman != cntCom) {
            for (int l = 0; l < dir*5; l+= dir) 
                if (board[cell+l] == 0) { // the square not be occupied
                    // The chance for computer 
                    if (cntHuman == 0) {
                        if (_turn == HUMAN)
                            caro[cell+l] = -caro[cell+l] + DefendScores[cntCom];
                        else
                            caro[cell+l] += AttackScores[cntCom];
                    }

                    // The chance for enemy
                    if (cntCom == 0) {
                        if (_turn == COMPUTER)
                            caro[cell+l] += AttackScores[cntHuman];
                        else
                            caro[cell+l] = -caro[cell+l] + DefendScores[cntHuman];
                        if (cntHuman == 4 || cntCom == 4)
                            caro[cell+l] *= 2;
                    }
                    if (_turn == HUMAN) {
                        caro[cell+l] *= -1;
                    }
                }
        }
    }
}

// take the stock of the situation
void evaluation(int _turn) {
    memset(caro, 0, sizeof(caro));
    caro[(sz+1)*sz/2] = 2;
    for (short i = 0; i < sz-2; ++i) caro[i] = -49999;
    for (short i = sz-1; i < sz*(sz-1); i += sz) {
        caro[i] = -49999;
        caro[i+1] = -49999;
    }
    for (short i = sz*(sz-1); i < sz*sz; i++) caro[i] = -49999;
    giveScore(exdirections[0], _turn);
    giveScore(exdirections[1], _turn);
    giveScore(exdirections[2], _turn);
    giveScore(exdirections[3], _turn);
}

void minimax(int depth, bool is_max) {
    if (depth > max_depth) return;

    if (is_max) {
        int max = -50000;
        evaluation(COMPUTER);
        Point *_Com;
        _Com = new Point[3];

        for (int i = 0; i < 3; i++) {
            _Com[i].x = max_element(caro, sz*sz);
            _Com[i]._score = caro[_Com[i].x];
            caro[_Com[i].x] = 0;
        }

        for (int i = 0; i < 3; i++) {
            Point temp_Com = _Com[i];
            board[temp_Com.x] = COMPUTER;

            if (isWin(COMPUTER)) {
                max = 50000;
                board[temp_Com.x] = 0;
                if (depth == 1) bestMove = _Com[i].x;
                break;
            }

            minimax(depth+1, false);
            board[temp_Com.x] = 0;
            if (max < maxScoreCom) {
                if (depth == 1) bestMove = _Com[i].x;
                max = maxScoreCom;
            }
        }
        maxScoreHuman = max;
    }
    else {
        int min = 50000;
        evaluation(HUMAN);
        Point *_Human;
        _Human = new Point[3];
        for (int i = 0; i < 3; i++) {
            _Human[i].x = min_element(caro, sz*sz);
            _Human[i]._score = caro[_Human[i].x];
            caro[_Human[i].x] = 0;
        }
        for (int i = 0; i < 3; i++) {
            Point temp_human = _Human[i];
            board[temp_human.x] = HUMAN;
            if (isWin(HUMAN)) {
                min = -50000;
                board[temp_human.x] = 0;
                break;
            }
            
            minimax(depth+1, true);
            board[temp_human.x] = 0;
            if (min > _Human[i]._score) min = _Human[i]._score;
        }
        maxScoreCom = min;
    }
}

int main() {
    init(15);

    while (!game_over)
    {
        // input: row x column y
        // board[x*sz+y] = HUMAN

        // check if game over?
        // game_over = isWin(HUMAN)

        // minimax(1, true);
        // output: bestMove

        // check if game over?
        // game_over = isWin(COMPUTER);

        // if you wanna computer play first then call minimax before you get input from human
    }
    return 0;
}