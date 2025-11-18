import java.util.*;

public class HiringProblem {

    public static int[] shuffle(int[] arr) {
        int n = arr.length;
        List<Integer> arrList = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            arrList.add(arr[i]);
        }
        Collections.shuffle(arrList);
        for (int i = 0; i < n; i++) {
            arr[i] = arrList.get(i);
        }
        return arr;
    }

    public static int getNumHires(int[] candidateScores) {
        int n = candidateScores.length;
        int numHires = 0;
        int selectedCandidateScore = 0;

        for (int i = 0; i < n; i++) {
            if (selectedCandidateScore < candidateScores[i]) {
                selectedCandidateScore = candidateScores[i];
                numHires += 1;
            }
        }

        return numHires;
    }

    public static int[] generateRandCandidateScores(int numCandidates) {
        int[] candidateScores = new int[numCandidates];
        for (int j = 0; j < numCandidates; j++) {
            candidateScores[j] = j;
        }
        candidateScores = shuffle(candidateScores);
        return candidateScores;
    }

    public static void main(String[] args) {
        int minNumCandidates = 5;
        int maxNumCandidates = 1000;
        int numTries = 10;
        int[][] numHires = new int[maxNumCandidates - minNumCandidates][numTries];

        for (int numCandidates = minNumCandidates; numCandidates < maxNumCandidates; numCandidates++) {
            for (int tryIndex = 0; tryIndex < numTries; tryIndex++) {
                int[] randCandidateScores = generateRandCandidateScores(numCandidates);
                numHires[numCandidates - minNumCandidates][tryIndex] = getNumHires(randCandidateScores);
            }
        }

        System.out.println("(numCandidates, avgHires)");
        for (int numCandidates = minNumCandidates; numCandidates < maxNumCandidates; numCandidates++) {

            float avgHires = 0;
            for (float numHire : numHires[numCandidates - minNumCandidates]) {
                avgHires += numHire;
            }

            avgHires /= numTries;

            System.out.printf("(%d, %f)\n", numCandidates, avgHires);
        }
    }

}
