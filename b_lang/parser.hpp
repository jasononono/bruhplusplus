#pragma once

#include "tokenizer.cpp"

namespace bpp_parser {
    
    using namespace std;
    
    class Parser {
    public:
        Parser();
    
        void parse(vector<Token> &tokens);
        void debugPrint() const;
        
    private:
        optional<Type> expectType();
        
        optional<Token> expectIdentifier(const string& name = string());
        optional<Token> expectOperator(const string& name = string());

        bool expectFunctionDefinition();
        
        vector<Token>::iterator mCurrentToken;
        vector<Token>::iterator mEndToken;
        map<string, Type> mTypes;
        map<string, FunctionDefinition> mFunctions;

        optional<vector<Statement>> parseFunctionBody();
        optional<Statement> parseOneStatement();
    };
}