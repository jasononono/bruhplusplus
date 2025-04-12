#pragma once

#include "statement.cpp"

namespace bpp_parser {

    using namespace std;

    class ParameterDefinition {
    public:
        string mName;
        Type mType;

        void debugPrint() const;
    };

    class FunctionDefinition {
    public:
        string mName;
        vector<ParameterDefinition> mParameters;
        vector<Statement> mStatements;

        void debugPrint() const;
    };
}