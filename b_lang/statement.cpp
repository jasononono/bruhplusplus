#include "statement.hpp"

namespace bpp_parser {

    using namespace std;

    void Statement::debugPrint() {
        cout << mType.mName << " " << mName << " ";
        for (Statement statement : mParameters) {
            statement.debugPrint();
        }
        cout << endl;
    }
}