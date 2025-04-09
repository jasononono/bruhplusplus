#include "tokenizer.hpp"
#include "parser.hpp"
#include <iostream>

using namespace std;
using namespace bpp_parser;

int main() {
    cout << "BRUH++ PARSER 0.1\n" << endl;

    FILE * fh = fopen("testFile.bpp", "r");
    if (!fh) { cerr << "Can't Find file." << endl; }
    fseek(fh, 0, SEEK_END);
    size_t fileSize = ftell(fh);
    fseek(fh, 0, SEEK_SET);
    string fileContents(fileSize, ' ');
    fread(&fileContents[0], 1, fileSize, fh);

    cout << fileContents << "\n\n";

    Tokenizer tokenizer;
    vector<Token> tokens = tokenizer.parse(fileContents);

    for (Token currToken : tokens) {
        currToken.debugPrint();
    }
    
    cout << "\n";

    Parser parser;
    parser.parse(tokens);
    
    return 0;
}