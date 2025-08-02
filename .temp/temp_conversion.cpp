
#include <iostream>
using namespace std;

// Uncomment this line to enable additional operations
#define ADDITIONALS

int main() {
    int a, b;
    cout << "Enter two numbers: ";
    cin >> a >> b;

    // Always do addition
    cout << "Sum: " << (a + b) << endl;

    // Do subtraction ONLY if ADDITIONALS is defined
    #ifdef ADDITIONALS
        cout << "Difference: " << (a - b) << endl;
    #endif
}


