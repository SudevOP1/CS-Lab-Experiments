import java.util.*;

public class RBTree {

    public static boolean RED = false;
    public static boolean BLACK = true;

    public static class Node {
        int value;
        boolean color;
        Node lChild;
        Node rChild;

        public Node(int value) {
            this.value = value;
            this.color = RED;
            this.lChild = null;
            this.rChild = null;
        }

        public Node insert(int value) {
            Node root = insertRec(this, value);
            root.color = BLACK;
            return root;
        }

        public Node delete(int value) {
            if (!contains(this, value))
                return this;

            Node root = deleteRec(this, value);
            if (root != null)
                root.color = BLACK;
            return root;
        }

        public List<Integer> getInorderList() {
            List<Integer> inorderList = new ArrayList<>();

            // left child
            if (this.lChild != null) {
                inorderList.addAll(this.lChild.getInorderList());
            }

            // self value
            inorderList.add(this.value);

            // right child
            if (this.rChild != null) {
                inorderList.addAll(this.rChild.getInorderList());
            }

            return inorderList;
        }

        public void printInorderList() {
            List<Integer> inorderList = this.getInorderList();
            for (Integer value : inorderList) {
                System.out.printf("%d ", value);
            }
            System.out.println("");
        }

        // Helper functions 👇

        private static Node insertRec(Node h, int value) {
            if (h == null) {
                return new Node(value);
            }

            if (value < h.value) {
                h.lChild = insertRec(h.lChild, value);
            } else if (value > h.value) {
                h.rChild = insertRec(h.rChild, value);
            } else {
                return h;
            }

            if (isRed(h.rChild) && !isRed(h.lChild)) {
                h = rotateLeft(h);
            }

            if (isRed(h.lChild) && isRed(h.lChild.lChild)) {
                h = rotateRight(h);
            }

            if (isRed(h.lChild) && isRed(h.rChild)) {
                flipColors(h);
            }

            return h;
        }

        private static Node deleteRec(Node h, int value) {
            if (value < h.value) {
                if (h.lChild != null) {
                    if (!isRed(h.lChild) && !isRed(h.lChild.lChild)) {
                        h = moveRedLeft(h);
                    }
                    h.lChild = deleteRec(h.lChild, value);
                }
            } else {
                if (isRed(h.lChild)) {
                    h = rotateRight(h);
                }

                if (value == h.value && h.rChild == null) {
                    return null;
                }

                if (h.rChild != null) {
                    if (!isRed(h.rChild) && !isRed(h.rChild.lChild)) {
                        h = moveRedRight(h);
                    }

                    if (value == h.value) {
                        Node min = min(h.rChild);
                        h.value = min.value;
                        h.rChild = deleteMin(h.rChild);
                    } else {
                        h.rChild = deleteRec(h.rChild, value);
                    }
                }
            }

            return fixUp(h);
        }

        private static boolean isRed(Node n) {
            return n != null && n.color == RED;
        }

        private static Node min(Node h) {
            while (h.lChild != null)
                h = h.lChild;
            return h;
        }

        private static Node deleteMin(Node h) {
            if (h.lChild == null) {
                return null;
            }

            if (!isRed(h.lChild) && !isRed(h.lChild.lChild)) {
                h = moveRedLeft(h);
            }

            h.lChild = deleteMin(h.lChild);
            return fixUp(h);
        }

        private static boolean contains(Node n, int value) {
            while (n != null) {
                if (value < n.value) {
                    n = n.lChild;
                } else if (value > n.value) {
                    n = n.rChild;
                } else {
                    return true;
                }
            }
            return false;
        }

        private static Node rotateLeft(Node h) {
            Node x = h.rChild;
            h.rChild = x.lChild;
            x.lChild = h;
            x.color = h.color;
            h.color = RED;
            return x;
        }

        private static Node rotateRight(Node h) {
            Node x = h.lChild;
            h.lChild = x.rChild;
            x.rChild = h;
            x.color = h.color;
            h.color = RED;
            return x;
        }

        private static void flipColors(Node h) {
            h.color = !h.color;
            if (h.lChild != null) {
                h.lChild.color = !h.lChild.color;
            }
            if (h.rChild != null) {
                h.rChild.color = !h.rChild.color;
            }
        }

        private static Node moveRedLeft(Node h) {
            flipColors(h);

            if (h.rChild != null && isRed(h.rChild.lChild)) {
                h.rChild = rotateRight(h.rChild);
                h = rotateLeft(h);
                flipColors(h);
            }

            return h;
        }

        private static Node moveRedRight(Node h) {
            flipColors(h);

            if (h.lChild != null && isRed(h.lChild.lChild)) {
                h = rotateRight(h);
                flipColors(h);
            }

            return h;
        }

        private static Node fixUp(Node h) {
            if (isRed(h.rChild)) {
                h = rotateLeft(h);
            }

            if (isRed(h.lChild) && isRed(h.lChild.lChild)) {
                h = rotateRight(h);
            }

            if (isRed(h.lChild) && isRed(h.rChild)) {
                flipColors(h);
            }

            return h;
        }

    }

    public static void main(String[] args) {

        // create initial parent node
        Node parentNode = new RBTree.Node(10);

        // insert values
        parentNode = parentNode.insert(20);
        parentNode = parentNode.insert(5);
        parentNode = parentNode.insert(15);
        parentNode = parentNode.insert(25);
        parentNode = parentNode.insert(3);
        parentNode = parentNode.insert(7);

        System.out.print("Inorder after inserts: ");
        parentNode.printInorderList();

        // delete some values
        parentNode = parentNode.delete(15);
        parentNode = parentNode.delete(5);

        System.out.print("Inorder after deleting 15 and 5: ");
        parentNode.printInorderList();

        // delete root
        parentNode = parentNode.delete(10);

        System.out.print("Inorder after deleting root 10: ");
        parentNode.printInorderList();

        // insert more values
        parentNode = parentNode.insert(30);
        parentNode = parentNode.insert(1);

        System.out.print("Final inorder list: ");
        parentNode.printInorderList();
    }
}