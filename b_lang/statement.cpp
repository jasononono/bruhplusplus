#include "statement.hpp"

namespace bpp_parser {

    using namespace std;

    void Statement::debugPrint() {
        cout << sStatementKindStrings[int(mKind)] << " ";
        cout << mType.mName << " " << mName << " " << " (\n";
        for (Statement statement : mParameters) {
            statement.debugPrint();
        }
        cout << ")" << endl; 
    }
}