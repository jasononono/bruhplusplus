#pragma once

#include "functionDefinition.cpp"

namespace bpp_parser {

    using namespace std;

    enum TokenType {
        WHITESPACE,
        IDENTIFIER,
        INTEGER_LITERAL,
        FLOAT_LITERAL,
        STRING_LITERAL,
        OPERATOR,
        STRING_ESCAPE_SEQUENCE,
        POTENTIAL_FLOAT,
        POTENTIAL_COMMENT,
        COMMENT
    };

    static const char *sTokenTypeStrings[] = {
        "WHITESPACE",
        "IDENTIFIER",
        "INTEGER_LITERAL",
        "FLOAT_LITERAL",
        "STRING_LITERAL",
        "OPERATOR",
        "STRING_ESCAPE_SEQUENCE",
        "POTENTIAL_FLOAT",
        "POTENTIAL_COMMENT",
        "COMMENT"
    };

    class Token {
    public:
        enum TokenType mType{WHITESPACE};
        string mText;
        size_t mLineNumber{0};

        void debugPrint() const;
    };

    class Tokenizer {
    public:
        vector<Token> parse(const string &program);

    private:
        void endToken(Token &token, vector<Token> &tokens);
    };

}