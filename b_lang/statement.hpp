#pragma once

#include "type.cpp"

namespace bpp_parser {

    using namespace std;

    enum class StatementKind {
        VARIABLE_DECLARATION,
        FUNCTION_CALL
    };

    class Statement {
    public:
        string mName;
        Type mType;
        vector<Statement> mParameters;
        StatementKind mKind{StatementKind::FUNCTION_CALL};

        void debugPrint();
    };
}