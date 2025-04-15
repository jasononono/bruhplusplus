#include "functionDefinition.hpp"

namespace bpp_parser {

    using namespace std;

    void FunctionDefinition::debugPrint() const {
        cout << mName << "(\n";

        for (ParameterDefinition param : mParameters) {
            param.debugPrint();
        }

        cout << ")\n{\n";
        for (Statement statement : mStatements) {
            statement.debugPrint();
        }
        cout << "}" << endl;
    }

    void ParameterDefinition::debugPrint() const {
        cout << mType.mName << " " << mName << endl;
    }
}