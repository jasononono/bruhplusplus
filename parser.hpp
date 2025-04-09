#pragma once

#include "tokenizer.hpp"
#include <optional>
#include <string>
#include <map>

namespace bpp_parser {
    
    using namespace std;
    
    enum BUILTIN_TYPE {
        VOID,
        INT32,
        UINT32,
        INT8
    };
    
    class Type {
    public:
        Type(const string &name = "", enum BUILTIN_TYPE type = VOID) : mName(name), mType(type) {}
        
        string mName;
        enum BUILTIN_TYPE mType;
        vector<Type> mFields; // for STRUCT only.
    };
    
    class Parser {
    public:
        Parser();
    
        void parse(vector<Token> &tokens);
        
    private:
        optional<Type> expectType();
        
        optional<Token> expectIdentifier(const string& name = string());
        optional<Token> expectOperator(const string& name = string());

        bool expectFunctionDefinition();
        
        vector<Token>::iterator mCurrentToken;
        vector<Token>::iterator mEndToken;
        map<string, Type> mTypes;
    };
}