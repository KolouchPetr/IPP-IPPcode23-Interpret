#!/usr/bin/php
<?php
ini_set('display_errors', 'stderr');

$XMLHEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>";
$XMLPROGRAMSTART = "<program language=\"IPPcode23\">";

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

enum LineType {
	case singleArg;
	case doubleArg;
	case tripleArg;
}


class Parser {

	
	public function readSTDIN() {
		$input_data = file_get_contents("php://stdin");
		return $input_data;
	}

	public function getType($line) {

	}

	public function getInstructionFromLine($line) {
		$instruction = explode(' ', trim($line ))[0];
		return $instruction;
	}

	public function  getArgumentsFromLine($line) {
		$argumentsString = substr(strstr($line," "), 1);
		$arguments = explode(" ", $argumentsString);
		return $arguments;
	}

	public function checkHeader($line) {
		if(strcmp(strtolower($line), strtolower(".IPPcode23"))) {
			fwrite(STDERR, "Header is either missing or is incorrect");
			exit(21);
		}
	}

	public function createArgument($argument) {
		$parts = explode("@", $argument);
		$argType = $parts[0];
		
		switch ($argType) {
			case "GF":
			case "LF":
			case "TF":
			$argument = new Argument("var", $parts[0] . "@" . $parts[1]);
				break;
			case "int":
			$argument = new Argument("int", $parts[1]);
				break;
			case "bool":
			$argument = new Argument("bool", $parts[1]);
				break;
			case "string":
				if(!$parts[1]) {
					$argument = new Argument("string", "");
				} else {
					$argument = new Argument("string", $parts[1]);
				}
				break;
			case "nil":
				#FIXME: nil values
				$argument = new Argument("nil", "nil");
				break;
			case "type":
				#TODO:
				break;
			
		}
		return $argument;
	}

}

enum ArgumentTypes {
	case int;
	case bool;
	case string;
	case nil;
	case label;
	case type;
	case var;
}

class Argument {
	public $type;
	public $value;

	function __construct($type, $value) {
		$this->type = $type;
		$this->value = $value;
	}
}

class XML {
	public function createTag($tagName, $args, $value) {
		$tag = "<". $tagName . " ";
		foreach($args as $arg) {
			$tag .= $arg . " ";
		}
		$tag .= ">" . $value;

		echo $tag;
	}

	public function endTag($tagName) {
		$tag = "</" . $tagName . ">";
		echo $tag . "\n";
	}

	public function createInstruction($order, $opcode, $args) {
		$orderString = "order=\"" . $order . "\"";
		$this->createTag("instruction", [$orderString], "");
		$this->createTag("opcode", [], $opcode);
		$this->endTag("opcode");
		$argCount = 1;
		foreach($args as $arg) {
			#FIXME:
			if($arg->type != "" && $arg->value != ""){
				$tagName = "arg" . $argCount;
				$type = "type=\"" . $arg->type . "\"";
				$this->createTag($tagName, [$type], $arg->value);
				$this->endTag($tagName);
				$argCount++;
			}
		}
		$this->endTag("instruction");
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
$xml = new XML();
$input_data = $parser->readSTDIN();
$lines = explode("\n", $input_data);

$linesWithoutComments = array_map(function($line) {
    return preg_replace('/#.*/', '', $line);
}, $lines);

$noBlankLines = preg_grep('/^[\s]*$/', $linesWithoutComments, PREG_GREP_INVERT);


$lineNumber = 0;

echo $XMLHEADER . "\n";
echo $XMLPROGRAMSTART . "\n";
foreach($noBlankLines as $line) {
	if($lineNumber == 0) {
		$parser->checkHeader($line);
	} else {
	$instruction = $parser->getInstructionFromLine($line);
	$arguments = $parser->getArgumentsFromLine($line);

	if(!in_array($instruction, $instructions)) {
		fwrite("chybne zapsany nebo neznamy operacni kod");
		exit(22);
	}

	switch ($instruction) {
		case "CREATEFRAME":
		case "PUSHFRAME":
		case "POPFRAME":
		case "RETURN":
		case "BREAK":
			$xml->createInstruction($lineNumber, $instruction, []);
			break;

		case "LABEL":
		case "JUMP":
			$argument = new Argument("label", $arguments[0]);
			$xml->createInstruction($lineNumber, $instruction, [$argument]);
			break;

		default:
		$argumentList = array();
		foreach($arguments as $argument) {
			#echo "***creating argument with: " . $argument . " ***\n";
			$currentArgument = $parser->createArgument($argument);
			array_push($argumentList, $currentArgument);
		}
		$xml->createInstruction($lineNumber, $instruction, $argumentList);
		break;

	}
	}
	$lineNumber++;
}
$xml->endTag("program");








/* 
plan
1. parse input into lines - done
2. remove comments from lines - done
3. remove empty lines - done
4. check if line has valid instruction (valid OP code should be  the first string)
5. check if the instruction has valid number of arguments
5. check if the line makes sense in terms of syntax (undefined variable, redefined variable, scope etc)
6. if line is valid, add it to the output xml, go back to 4.
*/
?>