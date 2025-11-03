import java.util.*;

public class OddPalindrome {

    public static boolean isOddPalindrome(String input) {
        Stack<Character> stack = new Stack<>();
        int len = input.length();

        if (len % 2 == 0) {
            return false;
        }

        int mid = len / 2;
        for (int i = 0; i < mid; i++) {
            stack.push(input.charAt(i));
        }

        for (int i = mid + 1; i < len; i++) {
            if (stack.isEmpty()) {
                return false;
            }
            char top = stack.pop();
            if (top != input.charAt(i)) {
                return false;
            }
        }

        return stack.isEmpty();
    }

    public static void main(String[] args) {
        String[] inputStrings = { "aba", "aa", "abb" };
        for (String inputString : inputStrings) {
            if (isOddPalindrome(inputString)) {
                System.out.printf("Accepted: %s\n", inputString);
            } else {
                System.out.printf("Rejected: %s\n", inputString);
            }
        }
    }
}
