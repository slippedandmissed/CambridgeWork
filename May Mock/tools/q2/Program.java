class FuncList {
    private Element myHead;

    public FuncList() {

    }

    private FuncList(Element head) {
        this.myHead = head;
    }

    public int head() {
        if (myHead == null) {
            throw new RuntimeException("The list is empty");
        } else {
            return myHead.item;
        }
    }

    public FuncList tail() {
        if (myHead == null) {
            throw new RuntimeException("The list is empty");
        } else {
            return new FuncList(myHead.next);
        }
    }

    public FuncList cons(int x) {
        Element newHead = new Element(x, this.myHead);
        return new FuncList(newHead);
    }

}