#include "parser.hpp"

namespace bpp_parser {
    
    using namespace std;
    
    bool Parser::expectFunctionDefinition() {
        vector<Token>::iterator parseStart = mCurrentToken;
        optional<Type> possibleType = expectType();
        
        if (possibleType.has_value()) { // type?
            optional<Token> possibleName = expectIdentifier();
            
            if (possibleName.has_value()) { // name?
                optional<Token> possibleOperator = expectOperator("(");
                
                if (possibleOperator.has_value()) { // operator?

                    FunctionDefinition func;
                    func.mName = possibleName -> mText;
                    
                    while(!expectOperator(")").has_value()) {
                        optional<Type> possibleParamType = expectType();
                        if (!possibleParamType.has_value()) {
                            throw runtime_error("Expected type at start of argument");
                        }
                        optional<Token> possibleVariableName = expectIdentifier();

                        ParameterDefinition param;
                        param.mType = possibleParamType -> mName;
                        if (possibleVariableName.has_value()) {
                            param.mName = possibleVariableName -> mText;
                        }
                        func.mParameters.push_back(param);

                        if (expectOperator(")").has_value()) {
                            break;
                        }

                        if (!expectOperator(",").has_value()) {
                            throw runtime_error("Expected parameter seperator");
                        }
                    }

                    optional<vector<Statement>> statements = parseFunctionBody();
                    if (!statements.has_value()) {
                        mCurrentToken = parseStart;
                        return false;
                    }
                    func.mStatements.insert(func.mStatements.begin(), statements -> begin(), statements -> end());


                    mFunctions[func.mName] = func;

                    return true;
                } else {
                    mCurrentToken = parseStart;
                }
            } else {
                mCurrentToken = parseStart;
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
        mTypes["double"] = Type("double", DOUBLE);
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

    optional<vector<Statement>> Parser::parseFunctionBody() {
        if (!expectOperator("{").has_value()) {
            return nullopt;
        }

        vector<Statement> statements;

        optional<Statement> statement = parseOneStatement();
        if (statement.has_value()) {
            statements.push_back(statement.value());
        }

        // if (!expectOperator("}").has_value()) {
        //     throw runt ime_error("Unbalanced '{'.");
        // }

        return statements;
    }

    void Parser::debugPrint() const {
        for (auto funcPair : mFunctions) {
            funcPair.second.debugPrint();
        }
    }

    optional<Statement> Parser::parseOneStatement() {
        vector<Token>::iterator startToken = mCurrentToken;
        optional<Type> possibleType = expectType();
        if (!possibleType.has_value()) {
            mCurrentToken = startToken;
            return nullopt;
        }

        optional<Token> possibleVariableName = expectIdentifier();
        if (!possibleType.has_value()) {
            mCurrentToken = startToken;
            return nullopt;
        }

        Statement statement;

        statement.mKind = StatementKind::VARIABLE_DECLARATION;
        statement.mName = possibleVariableName -> mText;
        statement.mType = possibleType.value();

        return statement;
    }
}