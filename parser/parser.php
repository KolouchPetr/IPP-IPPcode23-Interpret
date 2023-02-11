#!/usr/bin/php
<?php
ini_set('display_errors', 'stderr');

enum HeaderState {
	case HEADER;
	case HEADER_DOT;
	case HEADER_I;
	case HEADER_IP;
	case HEADER_IPP;
	case HEADER_C;
	case HEADER_CO;
	case HEADER_COD;
	case HEADER_CODE;
	case HEADER_CODE2;
	case HEADER_CODE23;
}

enum ScannerState {
	case START;
	case CONSTANT;
	case IDENTIFIER;
	case COMMENT;
}

enum TokenType {
	case CONSTANT;
	case IDENTIFIER;
	case LABEL;
	case GF;
	case LF;
	case TF;
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
	function __construct($type, ) {

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
	} else {
		echo "use -help or --help to print usage";
	} 
} 
$parser = new Parser();
$input_data = $parser->readSTDIN();
echo $input_data;

?>