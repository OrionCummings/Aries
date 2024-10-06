The Aries Programming Language (APL) is a statically-typed procedural language designed to write programs for the Aries Hardware Package. APL closely resembles C in syntax and feature set, but it supports several additional features from other popular languages like function overloading


APL currently uses the following EBNF grammar:

```
// Note: Tokens are capitalized or symbolic

<Aries Program> ::= <Declaration>*

<Declaration> ::= 
    <VariableDeclaration> | 
    <FunctionDeclaration>

<VariableDeclaration> ::=
    <Type> <Identifier> = VALUE ; |
    <Type> <Identifier> [ ] = VALUE ; |
    <Type> <Identifier> [ <DecimalConstant> ] = { <ConstantList> } ; |


<VariableDeclarationList> ::= 
    <VariableDeclarationList> , <VariableDeclarationIdentifier> |
    <VariableDeclarationIdentifier>

<VariableDeclarationIdentifier> ::=
    <Identifier> |
    <Identifier> [ ]

<FunctionDeclaration> ::= 
    def <Identifier>(<Parameters>) <Statement> | 
    def overload <Identifier>(<Parameters>) <Statement> | 
    def <Identifier>(<Parameters>) -> <Type> <Statement>
    def overload <Identifier>(<Parameters>) -> <Type> <Statement>

<StructDeclaration> ::=

<Parameters> ::= <ParameterList> | ε
<ParameterList> ::= (<ParameterIdentifier>,)*(<ParameterIdentifier>)

<ParameterIdentifier> ::=
    <Identifier> |
    <Identifier> []

<Statement> ::=

<Type> ::= int | uint | float | bool | char | void

<Digit> ::= [0-9]
<NonDigit> ::= [A-Za-z_]*
<Identifier> ::= <NonDigit> (<NonDigit> | <Digit>)*

// Expressions

<CastExpression> ::= <Identifier> as <Type>

<PrimaryExpression> ::= 
    <Identifier> |
    <Constant> |
    <CharacterConstant> |
    <StringConstant>

<PostfixExpression> ::=
    <PrimaryExpression> |
    <PostfixExpression> [ <Expression> ] |
    <PostfixExpression> ( ) |
    <PostfixExpression> ( <ParameterList> ) |
    <PostfixExpression> . <Identifier> |
    <PostfixExpression> OP_POINTER <Identifier>
    <PostfixExpression> OP_INC
    <PostfixExpression> OP_DEC

<UnaryExpression> ::= 
    <PostfixExpression> |
    OP_INC <UnaryExpression> |
    OP_DEC <UnaryExpression> |
    SIZEOF <UnaryExpression> |
    SIZEOF ( <Type> )

// Constants

<ConstantList> ::= <Constant> (, <Constant>)*

<Constant> ::=
    <IntegerConstant> |
    <FloatConstant> |
    <EnumerationConstant> |
    <CharacterConstant> |

<IntegerConstant> ::=
    <DecimalConstant> |
    <BinaryConstant> |
    <OctalConstant> |
    <HexadecimalConstant> |

<Sign> ::= - | +

<BinaryDigit> ::= [0-1]
<BinaryPrefix> ::= 0b | 0B
<BinaryConstant> ::= <BinaryPrefix> <BinaryDigit>+

<OctalDigit> ::= [0-7]
<OctalPrefix> ::= 0o | 0O
<OctalConstant> ::= <OctalPrefix> <OctalDigit>+

<HexadecimalDigit> ::= [0-9A-Fa-f]
<HexadecimalPrefix> ::= 0x | 0X
<HexConstant> ::= <HexadecimalPrefix><HexadecimalDigit>+

<DecimalDigit> ::= [0-9]
<DecimalConstant> ::= <DecimalDigit>+

<Float> ::= <DecimalDigit>+ f | <DecimalDigit>* . <DecimalDigit>*

<Character> ::= [A-Za-z_]
<CharacterConstant> ::= ' <Character> '

<StringConstant> ::= " <Character>* "
```