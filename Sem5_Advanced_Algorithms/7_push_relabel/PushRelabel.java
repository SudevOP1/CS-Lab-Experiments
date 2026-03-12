import java.util.*;

public class PushRelabel {

    public static int[][] inputCapactiy() {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter num nodes: ");
        int n = sc.nextInt();
        int[][] capacity = new int[n][n];

        System.out.printf("Enter Capacity Graph (0 = source, %d = sink)\n", n - 1);

        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                System.out.printf("Enter capacity of %d %d: ", i, j);
                capacity[i][j] = sc.nextInt();
                capacity[j][i] = capacity[i][j];
            }
        }

        return capacity;
    }

    static int n;
    static int[][] residual;
    static int[] height;
    static int[] excess;

    static void push(int u, int v) {
        int flow = Math.min(excess[u], residual[u][v]);

        residual[u][v] -= flow;
        residual[v][u] += flow;

        excess[u] -= flow;
        excess[v] += flow;
    }

    static void relabel(int u) {
        int minHeight = Integer.MAX_VALUE;

        for (int v = 0; v < n; v++) {
            if (residual[u][v] > 0) {
                minHeight = Math.min(minHeight, height[v]);
            }
        }

        if (minHeight < Integer.MAX_VALUE) {
            height[u] = minHeight + 1;
        }
    }

    static void discharge(int u) {
        while (excess[u] > 0) {
            boolean pushed = false;

            for (int v = 0; v < n; v++) {
                if (residual[u][v] > 0 && height[u] == height[v] + 1) {
                    push(u, v);
                    pushed = true;

                    if (excess[u] == 0)
                        break;
                }
            }

            if (!pushed) {
                relabel(u);
            }
        }
    }

    public static int pushRelabel(int[][] capacity) {

        n = capacity.length;
        residual = new int[n][n];
        height = new int[n];
        excess = new int[n];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                residual[i][j] = capacity[i][j];

        int source = 0;
        int sink = n - 1;

        height[source] = n;

        for (int v = 0; v < n; v++) {
            if (capacity[source][v] > 0) {
                residual[source][v] -= capacity[source][v];
                residual[v][source] += capacity[source][v];

                excess[v] = capacity[source][v];
                excess[source] -= capacity[source][v];
            }
        }

        Queue<Integer> queue = new LinkedList<>();

        for (int i = 1; i < n - 1; i++) {
            if (excess[i] > 0)
                queue.add(i);
        }

        while (!queue.isEmpty()) {
            int u = queue.poll();

            int oldHeight = height[u];
            discharge(u);

            if (height[u] > oldHeight) {
                queue.add(u);
            }
        }

        return excess[sink];
    }

    public static int[][] graphToTest = {
            { 0, 10, 5, 0 },
            { 0, 0, 15, 10 },
            { 0, 0, 0, 10 },
            { 0, 0, 0, 0 }
    };

    public static void main(String[] args) {

        // int maxFlow = pushRelabel(inputCapactiy());
        int maxFlow = pushRelabel(graphToTest);
        System.out.printf("Max flow = %d", maxFlow);
    }
}
