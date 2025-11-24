import java.util.*;

public class KDTree {

    public static class Node {

        int x;
        int y;
        Node lChild;
        Node rChild;

        public Node(int x, int y) {
            this.x = x;
            this.y = y;
            this.lChild = null;
            this.rChild = null;
        }

        public Node insert(Node newNode) {
            this.insert(newNode, 0);
            return this;
        }

        public Node insert(Node newNode, int depth) {

            // get dimension to check
            int thisDim, newNodeDim;
            if (depth % 2 == 0) {
                thisDim = this.x;
                newNodeDim = newNode.x;
            } else {
                thisDim = this.y;
                newNodeDim = newNode.y;
            }

            // left
            if (newNodeDim <= thisDim) {
                if (this.lChild == null) {
                    this.lChild = newNode;
                } else {
                    this.lChild.insert(newNode, depth + 1);
                }
            }
            // right
            else {
                if (this.rChild == null) {
                    this.rChild = newNode;
                } else {
                    this.rChild.insert(newNode, depth + 1);
                }
            }

            return this;
        }

        public Node delete(int x, int y) {
            return this.delete(x, y, 0);
        }

        private Node delete(int x, int y, int depth) {

            // get dimension to check
            int thisDim, queryDim;
            if (depth % 2 == 0) {
                thisDim = this.x;
                queryDim = x;
            } else {
                thisDim = this.y;
                queryDim = y;
            }

            // found the node to delete
            if (this.x == x && this.y == y) {

                // if right child exists, replace with min from right subtree
                if (this.rChild != null) {
                    Node minNode = this.rChild.findMin(depth);
                    this.x = minNode.x;
                    this.y = minNode.y;
                    this.rChild = this.rChild.delete(minNode.x, minNode.y, depth + 1);
                }
                // if only left child exists, replace with min from left subtree
                else if (this.lChild != null) {
                    Node minNode = this.lChild.findMin(depth);
                    this.x = minNode.x;
                    this.y = minNode.y;
                    this.rChild = this.lChild.delete(minNode.x, minNode.y, depth + 1);
                    this.lChild = null;
                }
                // leaf node, just delete
                else {
                    return null;
                }
            }
            // search in left subtree
            else if (queryDim <= thisDim) {
                this.lChild = (this.lChild != null) ? this.lChild.delete(x, y, depth + 1) : null;
            }
            // search in right subtree
            else {
                this.rChild = (this.rChild != null) ? this.rChild.delete(x, y, depth + 1) : null;
            }

            return this;
        }

        public int getDepth(int x, int y) {
            return this.getDepth(x, y, 0);
        }

        public int getDepth(int x, int y, int depth) {

            // element found
            if (this.x == x && this.y == y) {
                return depth + 1;
            }

            // get dimension to check
            int thisDim, queryDim;
            if (depth % 2 == 0) {
                thisDim = this.x;
                queryDim = x;
            } else {
                thisDim = this.y;
                queryDim = y;
            }

            // left
            if (queryDim <= thisDim && this.lChild != null) {
                return this.lChild.getDepth(x, y, depth + 1);
            }

            // right
            if (queryDim > thisDim && this.rChild != null) {
                return this.rChild.getDepth(x, y, depth + 1);
            }

            // element not found
            return -1;
        }

        public Node nearestNeighbor(int x, int y) {
            return this.nearestNeighbor(x, y, 0);
        }

        public Node nearestNeighbor(int x, int y, int depth) {

            // get dimension to check
            int thisDim, queryDim;
            if (depth % 2 == 0) {
                thisDim = this.x;
                queryDim = x;
            } else {
                thisDim = this.y;
                queryDim = y;
            }

            Node nextBranch = null;
            Node otherBranch = null;
            if (queryDim <= thisDim) {
                nextBranch = this.lChild;
                otherBranch = this.rChild;
            } else {
                nextBranch = this.rChild;
                otherBranch = this.lChild;
            }

            Node temp = null;
            if (nextBranch != null) {
                temp = nextBranch.nearestNeighbor(x, y, depth + 1);
            }
            Node best = closest(x, y, this, temp);

            long radiusSquared = distSquared(best.x, best.y, x, y);
            long dist = queryDim - thisDim;

            if (radiusSquared >= dist * dist) {
                if (otherBranch != null) {
                    temp = otherBranch.nearestNeighbor(x, y, depth + 1);
                    best = closest(x, y, best, temp);
                }
            }
            return best;
        }

        public List<Node> rangeQuery(int x1, int y1, int x2, int y2) {
            List<Node> result = new ArrayList<>();
            this.rangeQuery(x1, y1, x2, y2, 0, result);
            return result;
        }

        private void rangeQuery(int x1, int y1, int x2, int y2, int depth, List<Node> result) {

            // check if current node is in range
            if (this.x >= x1 && this.x <= x2 && this.y >= y1 && this.y <= y2) {
                result.add(this);
            }

            // get dimension to check
            int thisDim, minDim, maxDim;
            if (depth % 2 == 0) {
                thisDim = this.x;
                minDim = x1;
                maxDim = x2;
            } else {
                thisDim = this.y;
                minDim = y1;
                maxDim = y2;
            }

            // search left subtree
            if (minDim <= thisDim && this.lChild != null) {
                this.lChild.rangeQuery(x1, y1, x2, y2, depth + 1, result);
            }

            // search right subtree
            if (maxDim > thisDim && this.rChild != null) {
                this.rChild.rangeQuery(x1, y1, x2, y2, depth + 1, result);
            }
        }

        public List<KDTree.Node> getInorderList() {
            List<KDTree.Node> inorderList = new ArrayList<>();

            // left child
            if (this.lChild != null) {
                inorderList.addAll(this.lChild.getInorderList());
            }

            // self value
            inorderList.add(this);

            // right child
            if (this.rChild != null) {
                inorderList.addAll(this.rChild.getInorderList());
            }

            return inorderList;
        }

        public void printInorderList() {
            List<KDTree.Node> inorderList = this.getInorderList();
            int n = inorderList.size();

            for (int i = 0; i < n; i++) {
                System.out.printf("(%d, %d)", inorderList.get(i).x, inorderList.get(i).y);
                if (i != n - 1) {
                    System.out.println(",");
                }
            }
            System.out.println("");
        }

        private static Node closest(int x, int y, Node node1, Node node2) {

            if (node1 == null) {
                return node2;
            }
            if (node2 == null) {
                return node1;
            }

            long node1DistSquared = distSquared(x, y, node1.x, node1.y);
            long node2DistSquared = distSquared(x, y, node2.x, node2.y);

            if (node1DistSquared <= node2DistSquared) {
                return node1;
            }
            return node2;
        }

        private static long distSquared(int x1, int y1, int x2, int y2) {
            long xDiff = x1 - x2;
            long yDiff = y1 - y2;
            return xDiff * xDiff + yDiff * yDiff;
        }

        private Node findMin(int depth) {

            // get dimension to check
            int cutDim = depth % 2;

            return findMinHelper(cutDim, depth);
        }

        private Node findMinHelper(int cutDim, int depth) {

            int currentDim = depth % 2;

            // if current dimension matches the cut dimension
            if (currentDim == cutDim) {
                if (this.lChild == null) {
                    return this;
                }
                return this.lChild.findMinHelper(cutDim, depth + 1);
            }

            // if current dimension doesnt match, need to check both subtrees
            else {
                Node minNode = this;
                Node lMin = null;
                Node rMin = null;

                if (this.lChild != null) {
                    lMin = this.lChild.findMinHelper(cutDim, depth + 1);
                }
                if (this.rChild != null) {
                    rMin = this.rChild.findMinHelper(cutDim, depth + 1);
                }

                if (cutDim == 0) {
                    if (lMin != null && lMin.x < minNode.x) {
                        minNode = lMin;
                    }
                    if (rMin != null && rMin.x < minNode.x) {
                        minNode = rMin;
                    }
                } else {
                    if (lMin != null && lMin.y < minNode.y) {
                        minNode = lMin;
                    }
                    if (rMin != null && rMin.y < minNode.y) {
                        minNode = rMin;
                    }
                }

                return minNode;
            }
        }

    }

    public static void main(String[] args) {

        // Create root
        Node root = new KDTree.Node(10, 10);

        // Insert points
        root.insert(new KDTree.Node(5, 5));
        root.insert(new KDTree.Node(15, 5));
        root.insert(new KDTree.Node(3, 7));
        root.insert(new KDTree.Node(7, 12));
        root.insert(new KDTree.Node(12, 3));
        root.insert(new KDTree.Node(18, 8));

        // Print inorder (not meaningful for KD-tree order,
        // but useful to verify tree structure)
        System.out.println("Inorder traversal:");
        root.printInorderList();

        // Test depth lookup
        System.out.println("\nDepth tests:");
        System.out.println("(10,10) depth = " + root.getDepth(10, 10));
        System.out.println("(5,5) depth = " + root.getDepth(5, 5));
        System.out.println("(7,12) depth = " + root.getDepth(7, 12));
        System.out.println("(18,8) depth = " + root.getDepth(18, 8));
        System.out.println("(100,100) depth = " + root.getDepth(100, 100)); // should be -1

        // Nearest-neighbor tests
        System.out.println("\nNearest neighbor tests:");
        Node nn1 = root.nearestNeighbor(6, 6); // near (5,5)
        System.out.println("Nearest to (6,6) = (" + nn1.x + ", " + nn1.y + ")");

        Node nn2 = root.nearestNeighbor(14, 4); // near (12,3) or (15,5)
        System.out.println("Nearest to (14,4) = (" + nn2.x + ", " + nn2.y + ")");

        Node nn3 = root.nearestNeighbor(17, 9); // near (18,8)
        System.out.println("Nearest to (17,9) = (" + nn3.x + ", " + nn3.y + ")");
    }

}