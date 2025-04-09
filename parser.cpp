#include "parser.hpp"
#include <iostream>

namespace bpp_parser {
    
    using namespace std;
    
    bool Parser::expectFunctionDefinition() {
        optional<Type> possibleType = expectType();
        
        if (possibleType.has_value()) { // type?
            optional<Token> possibleName = expectIdentifier();
            
            if (possibleName.has_value()) { // name?
                optional<Token> possibleOperator = expectOperator("(");
                
                if (possibleOperator.has_value()) { // operator?
                    
                    cout << ">>> function '" << possibleName -> mText << "' detected" << endl;
                    return true;
                } else {
                    --mCurrentToken;
                    --mCurrentToken;
                }
            } else {
                --mCurrentToken;
            }
        }
        return false;
    }
    
    void Parser::parse(vector<Token> &tokens) {
        mEndToken = tokens.end();
        mCurrentToken = tokens.begin();
        
        while (mCurrentToken != mEndToken) {
            if (expectFunctionDefinition()) {
                
            } else {
                cerr << "Unknown identifier " << mCurrentToken -> mText << "." << endl;
                ++mCurrentToken;
            }
        }
    }
    
    optional<Token> Parser::expectIdentifier(const string &name) {
        if (mCurrentToken == mEndToken) {return nullopt;}
        if (mCurrentToken -> mType != IDENTIFIER) {return nullopt;}
        if (!name.empty() && mCurrentToken -> mText != name) {return nullopt;}
    
        Token returnToken = *mCurrentToken;
        ++mCurrentToken;
        return returnToken;
    }
    
    optional<Token> Parser::expectOperator(const string &name) {
        if (mCurrentToken == mEndToken) {return nullopt;}
        if (mCurrentToken -> mType != OPERATOR) {return nullopt;}
        if (!name.empty() && mCurrentToken -> mText != name) {return nullopt;}
    
        Token returnToken = *mCurrentToken;
        ++mCurrentToken;
        return returnToken;
    }
    
    Parser::Parser() {
        mTypes["void"] = Type("void", VOID);
        mTypes["int"] = Type("int", INT32);
        mTypes["char"] = Type("char", INT8);
    }
    
    optional<Type> Parser::expectType() {
        optional<Token> possibleType = expectIdentifier();
        if (!possibleType) { return nullopt; }
        
        map<string, Type>::iterator foundType = mTypes.find(possibleType -> mText);
        if (foundType == mTypes.end()) {
            --mCurrentToken;
            return nullopt;
        }
        
        return foundType -> second;
    }
}