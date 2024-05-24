#include <iostream>
#include <vector>
#include <stack>

std::vector <std::pair<short, short> > conditions(0, {0, 0}); // {sum, numbers of cell}
short matrix[9][9], color[9][9], sum[9][9], iter[9][9];
short val = 0;

void writeFile(short a[][9]) {
    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) std::cout << a[i][j];
    }
}

void loang(short r, short c, short key) {
    if (r >= 0 && r < 9 && c >= 0 && c < 9 && color[r][c] == key) {
        color[r][c] = 0;
        iter[r][c] = val;
        loang(r + 1, c, key);
        loang(r, c - 1, key);
        loang(r, c + 1, key);
        loang(r - 1, c, key);
    }
    else {
        return;
    }
}

bool setUp() {
    for (int i = 0; i < 9; i++)
        for (int j = 0; j < 9; j++) 
            if (color[i][j] != 0) {
                loang(i, j, color[i][j]);
                val++;
            }
    conditions.resize(val);
    for (int i = 0; i < 9; i++)
        for (int j = 0; j < 9; j++) 
        {
            conditions[iter[i][j]].first += sum[i][j] - matrix[i][j];
            conditions[iter[i][j]].second += (matrix[i][j] == 0) ? 1 : 0;
        }
    return true;
}

bool feasible(short row, short column, short value) {
    if (conditions[iter[row][column]].first < 0) return false;
    else if (conditions[iter[row][column]].first == 0 && conditions[iter[row][column]].second > 0) return false;
    else if (conditions[iter[row][column]].first > 0 && conditions[iter[row][column]].second == 0) return false;

    for (int i = 0; i < 9; i++) 
        if (matrix[row][i] == value) return false;
    for (int i = 0; i < 9; i++) 
        if (matrix[i][column] == value) return false;
    short edge_r = row / 3 * 3, edge_c = column / 3 * 3;
    for (int i = 0; i < 9; i++) 
        if (matrix[edge_r+i/3][edge_c+i%3] == value) return false;
    return true;
}

void backtracking(short row, short column) {
    if (row > 8) {
        writeFile(matrix);
        exit(0);
    }
    else if (column > 8) {
        backtracking(row + 1, 0);
    }
    else if (matrix[row][column] != 0) {
        backtracking(row, column + 1);
    }
    else {
        for (int value = 1; value < 10; value++) {
            conditions[iter[row][column]].first -= value;
            conditions[iter[row][column]].second -= 1;
            if (feasible(row, column, value)) {
                matrix[row][column] = value;
                backtracking(row, column+1);
                matrix[row][column] = 0;
            }
            conditions[iter[row][column]].first += value;
            conditions[iter[row][column]].second += 1;
        }
    }
}

void solve() {
    backtracking(0, 0);
    std::cout << "Cannot solve the problem!";
}

int main() {
    for (int i = 0; i < 9; i++)
        for (int j = 0; j < 9; j++) std::cin >> matrix[i][j] >> sum[i][j] >> color[i][j];
    setUp();
    solve();
    return 0;
}