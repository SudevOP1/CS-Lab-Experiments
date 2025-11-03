import java.io.*;
import java.util.*;
import java.util.regex.*;

public class LexicalAnalyzer {

    public static String[] keywords = { "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
            "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short",
            "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile",
            "while" };

    public static String[] punctuators = { ",", ";", "(", ")", "{", "}", "[", "]", "#" };

    public static String[] operators = { "<<=", ">>=", "++", "--", "==", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
            "!=", ">=", "<=", "&&", "||", "<<", ">>", "+", "-", "*", "/", "%", "=", ">", "<", "!", "~" };

    public static List<String> readFileLines(String filepath) {
        List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filepath))) {
            String line;
            while ((line = br.readLine()) != null) {
                lines.add(line);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
        return lines;
    }

    public static int countRegex(String line, String token) {
        Pattern pattern = Pattern.compile("\\b" + Pattern.quote(token) + "\\b");
        Matcher matcher = pattern.matcher(line);
        int count = 0;
        while (matcher.find()) {
            count++;
        }
        return count;
    }

    public static int countSimple(String line, String token) {
        int count = 0;
        int index = 0;
        while ((index = line.indexOf(token, index)) != -1) {
            count++;
            index += token.length();
        }
        return count;
    }

    public static void main(String[] args) {
        List<String> lines = readFileLines("c_code.c");
        int[] keywordCount = new int[keywords.length];
        int[] punctCount = new int[punctuators.length];
        int[] operatorCount = new int[operators.length];

        for (String line : lines) {
            for (int i = 0; i < keywords.length; i++) {
                keywordCount[i] += countRegex(line, keywords[i]);
            }

            for (int i = 0; i < punctuators.length; i++) {
                punctCount[i] += countSimple(line, punctuators[i]);
            }

            for (int i = 0; i < operators.length; i++) {
                operatorCount[i] += countSimple(line, operators[i]);
            }
        }

        System.out.println("\nKeywords:");
        for (int i = 0; i < keywords.length; i++) {
            if (keywordCount[i] > 0) {
                System.out.println(keywords[i] + " : " + keywordCount[i]);
            }
        }

        System.out.println("\nPunctuators:");
        for (int i = 0; i < punctuators.length; i++) {
            if (punctCount[i] > 0) {
                System.out.println(punctuators[i] + " : " + punctCount[i]);
            }
        }

        System.out.println("\nOperators:");
        for (int i = 0; i < operators.length; i++) {
            if (operatorCount[i] > 0) {
                System.out.println(operators[i] + " : " + operatorCount[i]);
            }
        }
        System.out.println("");
    }
}
