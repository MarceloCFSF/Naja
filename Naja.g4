grammar Naja;

///////////////////////////////////////////////////////////////////////////////

// Definindo Regras Sintáticas

prog	: 'head' decl bloco 'tail'
      ;

decl  :  (declaravar)+
      ;
       
declaravar :  tipo ID (VIR ID)*
           ;

tipo       : 'numero' | 'texto'  
           ;

bloco	: (cmd)+
      ;

cmd	:  cmdleitura  
    	|  cmdescrita 
 	|  cmdattrib
 	|  cmdselecao
    	|  cmdrepeticao  
	;

cmdleitura	: 'leia' AP ID FP 
	      ;

cmdescrita	: 'escreva' AP escrita FP 
	      ;

escrita     : ID | TEXTO
            ;

cmdattrib	:  ID ATTR expr 
            ;
			
cmdselecao  :  'se' cmdcondicao ACH 
                  (cmd)+ 
                FCH (cmdelse)?
            ;

cmdelse     : 'senao' ACH (cmd+) FCH
            ;

cmdrepeticao : 'enquanto' cmdcondicao ACH 
                  (cmd)+ 
                FCH
             ;
			
cmdcondicao : AP (ID | NUMBER) OPREL (ID | NUMBER) FP
            ;

expr		:  TEXTO | termo (OP termo)*
            ;
			
termo		:  ID 
            | NUMBER
            ;

///////////////////////////////////////////////////////////////////////////////

// Definindo Regras Léxicas

// Abre Parenteses
AP	: '('
      ;

// Fecha Parenteses
FP	: ')'
      ;

// Ponto e Virgula
SC	: ';'
  	;

// Operadores Aritéticos
OP	: '+' | '-' | '.' | '/'
      ;

// Atribuição
ATTR : ':'
     ;

// Virgula
VIR  : ','
     ;

// Abre Chaves     
ACH  : '{'
     ;

// Fecha Chaves
FCH  : '}'
     ;

// Operadores relacionais
OPREL : '>' | '<' | '>=' | '<=' | '=' | '!='
      ;

// Identificadores 
ID	: ([a-z] | [A-Z]) ([a-z] | [A-Z] | [0-9])*
	;

TEXTO : '"' ([0-9]|[a-z]|[A-Z]|' ')+ '"'
      ;

// Numeros (Inteiros ou Decimais)
NUMBER	: [0-9]+ (',' [0-9]+)?
            ;

// Espaço em Branco, Pula Linha, Tabulação -> IGNORAR
WS	: (' ' | '\t' | '\n' | '\r') -> skip;