import java.util.*;

public class FordFulkerson {

    public static int[][] inputCapactiy() {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter num nodes: ");
        int n = sc.nextInt();
        int[][] capacity = new int[n][n];

        System.out.printf("Enter Capacity Graph (with 0=source, %d=sink):\n", n - 1);
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                System.out.printf("Enter capacity of %d %d: ", i, j);
                capacity[i][j] = sc.nextInt();
                capacity[j][i] = capacity[i][j];
            }
        }

        sc.close();
        return capacity;
    }

    public static int[] getAugumentingPath(int[][] currentFlow) {
        int n = currentFlow.length;
        boolean[] visited = new boolean[n];
        int[] parent = new int[n];
        Arrays.fill(parent, -1);

        Stack<Integer> stack = new Stack<>();
        stack.push(0);
        visited[0] = true;

        while (!stack.isEmpty()) {
            int from = stack.pop();
            if (from == n - 1) {
                break;
            }

            for (int to = 0; to < n; to++) {
                if (!visited[to] && currentFlow[from][to] > 0) {
                    parent[to] = from;
                    visited[to] = true;
                    stack.push(to);
                }
            }
        }

        if (!visited[n - 1]) {
            return new int[0];
        }

        List<Integer> pathList = new ArrayList<>();
        int current = n - 1;
        while (current != -1) {
            pathList.add(current);
            current = parent[current];
        }

        Collections.reverse(pathList);
        int numMembers = pathList.size();
        int[] path = new int[numMembers];
        for (int i = 0; i < numMembers; i++) {
            path[i] = pathList.get(i);
        }
        return path;
    }

    public static int fordFulkerson(int[][] capacity) {
        int n = capacity.length;
        int maxFlow = 0;
        int[][] currentFlow = new int[n][n];
        for (int i = 0; i < n; i++) {
            currentFlow[i] = capacity[i].clone();
        }

        while (true) {
            int[] augumentingPath = getAugumentingPath(currentFlow);
            int augumentingPathLen = augumentingPath.length;

            if (augumentingPathLen == 0) {
                break;
            }

            int bottleNeckCapacity = Integer.MAX_VALUE;
            for (int i = 0; i < augumentingPathLen - 1; i++) {
                int thisNode = augumentingPath[i];
                int nextNode = augumentingPath[i + 1];
                int possibleFlow = currentFlow[thisNode][nextNode];
                if (bottleNeckCapacity > possibleFlow) {
                    bottleNeckCapacity = possibleFlow;
                }
            }

            for (int i = 0; i < augumentingPathLen - 1; i++) {
                int thisNode = augumentingPath[i];
                int nextNode = augumentingPath[i + 1];
                currentFlow[thisNode][nextNode] -= bottleNeckCapacity;
                currentFlow[nextNode][thisNode] += bottleNeckCapacity;
            }
            maxFlow += bottleNeckCapacity;
        }

        return maxFlow;
    }

    public static int[][] graphToTest = {
            { 0, 10, 5, 0 },
            { 0, 0, 15, 10 },
            { 0, 0, 0, 10 },
            { 0, 0, 0, 0 }
    };

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // int maxFlow = fordFulkerson(inputCapactiy());
        int maxFlow = fordFulkerson(graphToTest);

        System.out.printf("Max flow for this graph = %d", maxFlow);

        sc.close();
    }
}
