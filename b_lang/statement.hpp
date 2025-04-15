#pragma once

#include "type.cpp"

namespace bpp_parser {

    using namespace std;

    enum class StatementKind {
        VARIABLE_DECLARATION,
        FUNCTION_CALL,
        LITERAL
    };

    static const char* sStatementKindStrings[] = {
        "VARIABLE_DECLARATION",
        "FUNCTION_CALL",
        "LITERAL"
    };

    class Statement {
    public:
        string mName;
        Type mType{Type("void", VOID)};
        vector<Statement> mParameters;
        StatementKind mKind{StatementKind::FUNCTION_CALL};

        void debugPrint();
    };
}