#!/usr/bin/php
<?php
ini_set('display_errors', 'stderr');

$HEADER = ".IPPcode23";
$XMLHEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>";
$XMLPROGRAMSTART = "<program language=\"IPPcode23\">";

enum ScannerState {
	case S_HEADER;
	case S_HEADER_DOT;
	case S_HEADER_I;
	case S_HEADER_IP;
	case S_HEADER_IPP;
	case S_HEADER_C;
	case S_HEADER_CO;
	case S_HEADER_COD;
	case S_HEADER_CODE;
	case S_HEADER_CODE2;
	case S_HEADER_CODE23;
	case S_START;
	case S_CONSTANT;
	case S_IDENTIFIER;
	case S_COMMENT;
}

enum TokenType {
	case CONSTANT;
	case IDENTIFIER;
	case LABEL;
	case GF;
	case LF;
	case TF;
	case END;
}


class Parser {



	public function readSTDIN() {
		$input_data = file_get_contents("php://stdin");
		return $input_data;
	}

	public function getNextToken() {

	}

}

class Token {
	public $type;
	public $name;
	public $value;
	function __construct($type, $name, $value) {
		$this->type = $type;
		$this->name = $name;
		$this->value = $value;
	}
}

class XML {
	public function createStartTag($tagName, $args, $value) {
		$tag = "<". $tagname . " ";
		foreach($args as $arg) {
			$tag .= $arg . " ";
		}
		$tag .= ">" . $value;

		return $tag;
	}

	public function createEndTag($tagName) {
		$tag = "</" . $tagname . ">";
		return $tag;
	}
}

/*
class SyntaxAnalysis {

}

class SemanticAnalysis {

}

*/

function printHelp() {
	echo "TODO: print help";
 }



if($argc == 2) {
	if(!strcmp($argv[1], "--help") || !strcmp($argv[1], "-help")) {
		printHelp();
		exit(0);
	} else {
		echo "use -help or --help to print usage";
		exit(1);
	} 
}

$parser = new Parser();
$input_data = $parser->readSTDIN();
$lines = explode("\n", $input_data);

$linesWithoutComments = array_map(function($line) {
    return preg_replace('/#.*/', '', $line);
}, $lines);

$noBlankLines = preg_grep('/^[\s]*$/', $linesWithoutComments, PREG_GREP_INVERT);

foreach($noBlankLines as $line) {
	echo $line;
	echo "\n";
}


if(strcmp(strtolower($noBlankLines[0]), strtolower($HEADER))) {
	fwrite(STDERR, "Header is either missing or is incorrect");
	exit(1);
}

$instructions = array("MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", "RETURN","PUSHS", "POPS",
					"ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR", "STRI2INT",
					"READ", "WRITE",
					"CONCAT", "STRLEN", "GETCHAR", "SETCHAR",
					"TYPE",
					"LABEL", "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "EXIT",
					"DPRINT", "BREAK");

$commentRegex = "/\s#.*/";
$singleArgumentRegex = "";
$twoArgumentRegex = "";
$threeArgumentRegex = "";




/* 
plan
1. parse input into lines
2. remove comments from lines
3. remove empty lines
3. check line if its one of the possible options (instruction/label, ...)
4. check if the line makes sense in terms of syntax (undefined variable, redefined variable, scope etc)
5. if line is valid, add it to the output xml
*/



?>