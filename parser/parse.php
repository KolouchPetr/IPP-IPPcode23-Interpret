#!/usr/bin/php
<?php
ini_set('display_errors', 'stderr');

$instructions = array(
        "MOVE" => ["var", "symb"],
        "CREATEFRAME" => [],
        "PUSHFRAME" => [],
        "POPFRAME" => [],
        "DEFVAR" => ["var"],
        "CALL" => ["label"],
        "RETURN" => [],
        "PUSHS" => ["symb"],
        "POPS" => ["var"],
        "ADD" => ["var", "symb", "symb"],
        "SUB" => ["var", "symb", "symb"],
        "MUL" => ["var", "symb", "symb"],
        "IDIV" => ["var", "symb", "symb"],
        "LT" => ["var", "symb", "symb"],
        "GT" => ["var", "symb", "symb"],
        "EQ" => ["var", "symb", "symb"],
        "AND" => ["var", "symb", "symb"],
        "OR" => ["var", "symb", "symb"],
        "NOT" => ["var", "symb", "symb"],
        "INT2CHAR" => ["var", "symb"],
        "STRI2INT" => ["var", "symb", "symb"],
        "READ" => ["var", "type"],
        "WRITE" => ["symb"],
        "CONCAT" => ["var", "symb", "symb"],
        "STRLEN" => ["var", "symb"],
        "GETCHAR" => ["var", "symb", "symb"],
        "SETCHAR" => ["var", "symb", "symb"],
        "TYPE" => ["var", "symb"],
        "LABEL" => ["label"],
        "JUMP" => ["label"],
        "JUMPIFEQ" => ["label", "symb", "symb"],
        "JUMPIFNEQ" => ["label", "symb", "symb"],
        "EXIT" => ["symb"],
        "DPRINT" => ["symb"],
        "BREAK" => []
);

class Parser
{
        public function readSTDIN()
        {
                $input_data = file_get_contents("php://stdin");
                return $input_data;
        }

        public function checkArgs() {
        global $argc, $argv;
        if ($argc == 2) {
          if (!strcmp($argv[1], "--help") || !strcmp($argv[1], "-help")) {
                  printHelp();
                  exit(0);
          } else {
                  echo "použijte -help or --help pro zobrazení nápovědy";
                  exit(1);
            }
          }
        }

        public function parseInputLines() {
        
        $input_data = $this->readSTDIN();
        $lines = explode("\n", $input_data);

        $linesWithoutComments = array_map(function ($line) {
          return preg_replace('/#.*/', '', $line);
        }, $lines);

        $noBlankLines = preg_grep('/^[\s]*$/', $linesWithoutComments, PREG_GREP_INVERT);
        return $noBlankLines;
        }

        public function getInstructionFromLine($line)
        {
                $instruction = explode(' ', trim($line))[0];
                return $instruction;
        }

        public function  getArgumentsFromLine($line)
        {
                $argumentsString = substr(strstr($line, " "), 1);
                $arguments = explode(" ", $argumentsString);
                // Remove empty elements
                $arguments = array_filter($arguments);
                // Re-index the array starting from 0
                $arguments = array_values($arguments);
                if (count($arguments) > 3) {
                        fwrite(STDERR, "řádek " . $line . " obsahuje příliš mnoho argumentů!");
                        exit(23);
                }
                return $arguments;
        }

        public function checkHeader($line)
        {
                if (strcmp(strtolower($line), strtolower(".IPPcode23"))) {
                        fwrite(STDERR, "chybějící nebo chybně zadaná hlavička!");
                        exit(21);
                }
        }

        public function createArgument($argument)
        {
                $parts = explode("@", $argument);
                $argType = $parts[0];
                $parts[1] = htmlspecialchars($parts[1], ENT_XML1);

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
                                        $i = 1;
                                        $string = "";
                                        while (isset($parts[$i])) {
                                                $string .= $parts[$i];
                                                $i++;
                                        }
                                        $argument = new Argument("string", $string);
                                break;
                        case "nil":
                                #FIXME: nil values
                                $argument = new Argument("nil", "nil");
                                break;
                        case "type":
                                #TODO:
                                $argument = new Argument("type", $parts[1]);
                                break;
                        default:
                                $argument = new Argument("label", $parts[0]);
                                break;
                }
                return $argument;
        }
}

class Argument
{
        public $type;
        public $value;

        function __construct($type, $value)
        {
                $this->type = $type;
                $this->value = $value;
        }
}

class XML
{
       const XMLHEADER = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>";
       const XMLPROGRAMSTART = "<program language=\"IPPcode23\">";

        public function printProgramStart() {
          echo self::XMLHEADER . "\n";
          echo self::XMLPROGRAMSTART . "\n";
        }

        public function createTag($tagName, $args, $value)
        {
                $tag = "<" . $tagName . " ";
                foreach ($args as $arg) {
                        $tag .= $arg . " ";
                }
                $tag .= ">" . $value;

                echo $tag;
        }

        public function endTag($tagName)
        {
                $tag = "</" . $tagName . ">";
                echo $tag . "\n";
        }

        public function createInstruction($order, $opcode, $args)
        {
                $orderString = "order=\"" . $order . "\"";
                $opcodeString = "opcode=\"" . $opcode . "\"";
                $this->createTag("instruction", [$orderString, $opcodeString], "");
                #$this->createTag("opcode", [], $opcode);
                #$this->endTag("opcode");
                $argCount = 1;
                foreach ($args as $arg) {
                  if($arg->type != "string" && $arg->value == "") {
                    continue;
                  }
                  elseif ($arg->type != "") {
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

class SyntaxAnalysis {
  public function checkInstructionArgumentTypes($instruction, $arguments) {
    global $instructions;
    if($instruction == "NOT" && count($arguments) == 2) {
      if(!$this->checkType($arguments[0], "var") || !$this->checkType($arguments[1], "symb")) {
        fwrite(STDERR, "chybný typ argumentu u argumentu " . $instruction);
        exit(23);
      }

    } else{
    for($i = 0; $i < count($instructions[$instruction]); $i++) {
            if(!$this->checkType($arguments[$i], $instructions[$instruction][$i])) {
              fwrite(STDERR, "chybný typ argumentu u instrukce " . $instruction . " u argumentu " . $arguments[$i]);
              exit(23);
            }
          }
    }
  }

  public function checkType($argument, $type) {
          switch($type) {
            case "var":
              return preg_match("/^(GF|TF|LF)@[a-zA-Z_\$&%*!?][\w\$&%*!?-]*$/", $argument);
              break;
            case "symb":
              return (preg_match("/^int[@][+-]?((0x[\da-fA-F]+)|([0-7]+)|(\d+))$/", $argument) ||
                preg_match("/(true|false)/", $argument)      ||
                preg_match("/string@(?:[^\p{Z}\p{Cc}#\\\\]|\\\\(?:[0-2][0-9][0-9]|[0-9]{2}|035|092))*(?:[^\\\\\p{Z}\p{Cc}]|$)/", $argument) || !strcmp("string@", $argument) || 
                !strcmp("nil@nil", $argument) ||
                preg_match("/^(GF|TF|LF)@[a-zA-Z_\$&%*!?][\w\$&%*!?-]*$/", $argument));
              break;
            case "label":
              return preg_match("/^[a-zA-Z_\-\$&%\*\!?][\w\-\$&%\*\!?]*$/", $argument);
              break;
            case "type":
              return preg_match("/^(int|bool|string|nil)$/", $argument);
              break;
          }
  }
  public function instructionExists($instruction) {
    global $instructions;
    if (!array_key_exists($instruction, $instructions)) {
      fwrite(STDERR, "chybně zapsaný nebo neznámý operační kód");
      exit(22);
    }
  }

  public function checkArgumentCount($instruction, $arguments) {
    global $instructions;
    if($instruction != "NOT"){
     if(count($instructions[$instruction]) != count($arguments)) {
       fwrite(STDERR, "nesprávný počet argumentů");
       exit(23);
      }
    } else {
        if((count($instructions[$instruction]) != count($arguments)) && (count($arguments) != 2)) {
          fwrite(STDERR, "nesprávný počet argumentů");
          exit(23);
        }
      }
    }
}

class Main {
  public function printHelp() {
    echo "  Program parse.php slouží pro vytvoření XML souboru platného IPPcode23 kódu.
    Zdrojový kód je načítán ze standardního vstupu stdin. 
    Spusťte program pomocí příkazu php parse.php, napište program do stdin a pomocí <ctrl+d> ukončete vstup
    nebo přesměrujte obsah souboru s kódem na stdin způsobem: php parse.php < zdroj.IPPcode23";
  }

  public function Program() {
    global $instructions;
    $parser = new Parser();
    $parser->checkArgs();
    $xml = new XML();
    $SyntaxAnalysis = new SyntaxAnalysis();

    $noBlankLines = $parser->parseInputLines();
    $lineNumber = 0;

    $xml->printProgramStart();

    foreach ($noBlankLines as $line) {
      if ($lineNumber == 0) {
        $line = str_replace(' ', '', $line);
                    $parser->checkHeader($line);
            } else {
              $instruction = $parser->getInstructionFromLine($line);
              $instruction = strtoupper($instruction);
              $instruction = str_replace(array(' ', "\t"), '', $instruction);
              $arguments = $parser->getArgumentsFromLine($line);
              $arguments = array_filter($arguments, function($value) {
              return !empty(trim($value));
              });



              $SyntaxAnalysis->instructionExists($instruction);
              $SyntaxAnalysis->checkArgumentCount($instruction, $arguments);
              $SyntaxAnalysis->checkInstructionArgumentTypes($instruction, $arguments);

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
                                    #case "JUMPIFEQ":
                                    #case "JUMPIFNEQ":
                            case "READ":
                              $argument = new Argument("var", $arguments[0]);
                              $argument1 = new Argument("type", $arguments[1]);
                              $xml->createInstruction($lineNumber, $instruction, [$argument, $argument1]);
                              break;


                            default:
                                    $argumentList = array();
                                    foreach ($arguments as $argument) {
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
    exit(0);
  } 
}

$main = new Main();
$main->Program();

?>
