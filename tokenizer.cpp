#include "tokenizer.hpp"
#include <stdexcept>
#include <iostream>

namespace bpp_parser {

    using namespace std;

    vector<Token> Tokenizer::parse(const string &program) {
        vector<Token> tokens;
        Token currentToken;

        currentToken.mLineNumber = 1;

        for (char ch : program) {
            if (currentToken.mType == STRING_ESCAPE_SEQUENCE) {
                switch(ch) {
                    case 'n':
                        currentToken.mText.append(1, '\n');
                        break;
                    case 'r':
                        currentToken.mText.append(1, '\r');
                        break;
                    case 't':
                        currentToken.mText.append(1, '\t');
                        break;
                    case '\\':
                        currentToken.mText.append(1, '\\');
                        break;
                    default:
                        throw runtime_error(string("unknown escape sequence: \\") + string(1, ch) + " in string on line" + to_string(currentToken.mLineNumber));
                        break;
                }
                currentToken.mType = STRING_LITERAL;
                continue;
            } else if (currentToken.mType == POTENTIAL_COMMENT && ch != '/') {
                currentToken.mType = OPERATOR;
                endToken(currentToken, tokens);
                continue;
            }

            switch(ch) {

                // NUMBERS

                case '0':
                case '1':
                case '2':
                case '3':
                case '4':
                case '5':
                case '6':
                case '7':
                case '8':
                case '9':
                    if (currentToken.mType == WHITESPACE) {
                        currentToken.mType = INTEGER_LITERAL;
                        currentToken.mText.append(1, ch);
                    } else if (currentToken.mType == POTENTIAL_FLOAT) {
                        currentToken.mType = FLOAT_LITERAL;
                        currentToken.mText.append(1, ch);
                    } else {
                        currentToken.mText.append(1, ch);
                    }
                    break;

                case '.':
                    if (currentToken.mType == WHITESPACE) {
                        currentToken.mType = POTENTIAL_FLOAT;
                        currentToken.mText.append(1, ch);
                    } else if (currentToken.mType == INTEGER_LITERAL) {
                        currentToken.mType = FLOAT_LITERAL;
                        currentToken.mText.append(1, ch);
                    } else if (currentToken.mType == STRING_LITERAL) {
                        currentToken.mText.append(1, ch);
                    } else {
                        endToken(currentToken, tokens);
                        currentToken.mType = OPERATOR;
                        currentToken.mText.append(1, ch);
                        endToken(currentToken, tokens);
                    }
                    break;

                // IDENTIFIERS

                case '!':
                case '=':
                case '+':
                case '-':
                case '*':
                case '{':
                case '}':
                case '[':
                case ']':
                case '(':
                case ')':
                    if (currentToken.mType != STRING_LITERAL) {
                        endToken(currentToken, tokens);
                        currentToken.mType = OPERATOR;
                        currentToken.mText.append(1, ch);
                        endToken(currentToken, tokens);
                    } else {
                        currentToken.mText.append(1, ch);
                    }
                    break;

                // WHITESPACE

                case ' ':
                case '\t':
                    if (currentToken.mType == STRING_LITERAL || currentToken.mType == COMMENT) {
                        currentToken.mText.append(1, ch);
                    } else {
                        endToken(currentToken, tokens);
                    }
                    break;

                case '\r':
                case '\n':
                    endToken(currentToken, tokens);
                    ++currentToken.mLineNumber;
                    break;

                // STRING

                case '\'':
                    if (currentToken.mType != STRING_LITERAL) {
                        endToken(currentToken, tokens);
                        currentToken.mType = STRING_LITERAL;
                    } else if (currentToken.mType == STRING_LITERAL) {
                        endToken(currentToken, tokens);
                    }
                    break;
                
                case '\\':
                    if (currentToken.mType == STRING_LITERAL) {
                        currentToken.mType = STRING_ESCAPE_SEQUENCE;
                    } else {
                        endToken(currentToken, tokens);
                        currentToken.mType = OPERATOR;
                        currentToken.mText.append(1, ch);
                        endToken(currentToken, tokens);
                    }
                    break;

                case '/':
                    if (currentToken.mType == STRING_LITERAL) {
                        currentToken.mText.append(1, ch);
                    } else if (currentToken.mType == POTENTIAL_COMMENT) {
                        currentToken.mType = COMMENT;
                        currentToken.mText.erase();
                    } else {
                        endToken(currentToken, tokens);
                        currentToken.mType = POTENTIAL_COMMENT;
                        currentToken.mText.append(1, ch);
                    }
                    break;

                // DEFAULT

                default:
                    if (currentToken.mType == WHITESPACE || currentToken.mType == INTEGER_LITERAL || currentToken.mType == FLOAT_LITERAL) {
                        endToken(currentToken, tokens);
                        currentToken.mType = IDENTIFIER;
                        currentToken.mText.append(1, ch);
                    } else {
                        currentToken.mText.append(1, ch);
                    }
                    break;
                }
        }

        endToken(currentToken, tokens);
        return tokens;
    }

    void Tokenizer::endToken(Token &token, vector<Token> &tokens) {
        if (token.mType == COMMENT) {
            cout << "Ignoring comment " + token.mText << endl;
        } else if (token.mType != WHITESPACE) {
            tokens.push_back(token);
        }
        if (token.mType == POTENTIAL_FLOAT) {
            if (token.mText.compare(".") == 0) {
                token.mType = OPERATOR;
            } else {
                token.mType = FLOAT_LITERAL;
            }
        }
        token.mType = WHITESPACE;
        token.mText.erase();
    }

    void Token::debugPrint() const {
        cout << "Token(" << sTokenTypeStrings[mType] << ", \"" << mText << "\", " << mLineNumber << ")" << endl;
    }
}
