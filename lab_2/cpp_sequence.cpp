#include <iostream>
#include <string>
#include <random>

using namespace std;

int main() {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distrib(0, 1);

    string sequence;
    for (int i = 0; i < 128; ++i) {
        sequence += distrib(gen) ? '1' : '0';
    }

    cout << sequence << endl;

    return 0;
}