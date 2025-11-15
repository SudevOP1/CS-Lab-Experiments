import java.util.Arrays;

public class Perceptron {
    private double[] weights;
    private double bias;
    private double learningRate;
    private int epochs;

    public Perceptron(int nInputs, double learningRate, int epochs) {
        this.weights = new double[nInputs];
        this.bias = 0.0;
        this.learningRate = learningRate;
        this.epochs = epochs;
    }

    private int activation(double sum) {
        return sum >= 0 ? 1 : 0; // step activation
    }

    public void train(double[][] inputs, int[] targets) {
        int nSamples = inputs.length;

        for (int epoch = 0; epoch < epochs; epoch++) {
            int totalErrors = 0;

            for (int i = 0; i < nSamples; i++) {

                double linearOutput = dot(weights, inputs[i]) + bias;
                int prediction = activation(linearOutput);
                int error = targets[i] - prediction;
                if (error != 0) {
                    totalErrors++;
                }

                // update weights and bias
                for (int j = 0; j < weights.length; j++) {
                    weights[j] += learningRate * error * inputs[i][j];
                }
                bias += learningRate * error;
            }
            if (totalErrors == 0) {
                break;
            }
        }
    }

    public int predict(double[] input) {
        double linearOutput = dot(weights, input) + bias;
        return activation(linearOutput);
    }

    public double accuracy(double[][] inputs, int[] targets) {
        int correct = 0;
        for (int i = 0; i < inputs.length; i++) {
            if (predict(inputs[i]) == targets[i]) {
                correct++;
            }
        }
        return 100.0 * correct / inputs.length;
    }

    private double dot(double[] a, double[] b) {
        double sum = 0.0;
        for (int i = 0; i < a.length; i++) {
            sum += a[i] * b[i];
        }
        return sum;
    }

    public double[] getWeights() {
        return Arrays.copyOf(weights, weights.length);
    }

    public double getBias() {
        return bias;
    }

    public static void main(String[] args) {
        double[][] andInputs = { { 0, 0 }, { 0, 1 }, { 1, 0 }, { 1, 1 } };
        int[] andTargets = { 0, 0, 0, 1 };

        Perceptron perceptron = new Perceptron(2, 0.1, 100);
        perceptron.train(andInputs, andTargets);

        System.out.println("Trained weights: " + Arrays.toString(perceptron.getWeights()));
        System.out.println("Trained bias: " + perceptron.getBias());
        System.out.println("Accuracy on AND dataset: " + perceptron.accuracy(andInputs, andTargets) + "%");
        System.out.println("\nPredictions:");
        for (double[] inp : andInputs) {
            System.out.printf("input=%s -> predicted=%d%n", Arrays.toString(inp), perceptron.predict(inp));
        }
    }
}
