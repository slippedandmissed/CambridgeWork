# C & C++ Supervision 2

# Lecture 1



1. 

```c++
class LinkList {

    int head;
    LinkList *tail = NULL;

    public:
        LinkList() {
            this->head = -1;
        }

        LinkList(int* ints, int length) {
            if (length == 0) {
                this->head = -1;
            } else {
                this->head = ints[0];
                if (length > 1) {
                    this->tail = new LinkList(ints+1, length-1);
                }
            }
        }

        LinkList(const LinkList& x) {
            this->head = x.head;
            this->tail = new LinkList(*(x.tail));
        }

        ~LinkList() {
            delete this->tail;
        }

        int pop() {
            return this->head;
        }

};
```

2. 

The constructor would be called before the `main` function.

3. 

```c++
class Matrix {

    int a, b, c, d;

    public:
        Matrix(int a, int b, int c, int d) : a(a), b(b), c(c), d(d) {

        }
        
        Matrix& operator+(Matrix x) {
            return *(new Matrix(a+x.a, b+x.b, c+x.c, d+x.d));
        }

        Matrix& operator-(Matrix x) {
            return *(new Matrix(a-x.a, b-x.b, c-x.c, d-x.d));
        }

        Matrix& operator*(Matrix x) {
            return *(new Matrix(a*x.a+b*x.c, a*x.b+b*x.d, c*x.a+d*x.c, c*x.b+d*x.d));
        }

        Matrix& operator*(int k) {
            return *(new Matrix(k*a, k*b, k*c, k*d));
        }

        Matrix& operator/(int k) {
            return *(new Matrix(a/k, b/k, c/k, d/k));
        }

};
```

4.

```c++
class Vector {

    int a, b;

    friend class Matrix;

    public:
        Vector(int a, int b) : a(a), b(b) {

        }

};

class Matrix {

    int a, b, c, d;

    public:
        Matrix(int a, int b, int c, int d) : a(a), b(b), c(c), d(d) {

        }
        
        Matrix& operator+(Matrix x) {
            return *(new Matrix(a+x.a, b+x.b, c+x.c, d+x.d));
        }

        Matrix& operator-(Matrix x) {
            return *(new Matrix(a-x.a, b-x.b, c-x.c, d-x.d));
        }

        Matrix& operator*(Matrix x) {
            return *(new Matrix(a*x.a+b*x.c, a*x.b+b*x.d, c*x.a+d*x.c, c*x.b+d*x.d));
        }

        Matrix& operator*(int k) {
            return *(new Matrix(k*a, k*b, k*c, k*d));
        }

        Matrix& operator/(int k) {
            return *(new Matrix(a/k, b/k, c/k, d/k));
        }

        Vector& operator*(const Vector& x) {
            return *(new Vector(a*x.a+b*x.b, c*x.a+d*x.b));
        }

};
```

5. 

A subclass `B` of `A` might allocate many more resources than `A`.

A `B` pointer might be assigned to a variable of type `A *` and so when the destructor is invoked, `A`'s destructor is executed.

6. 

Abstract classes cannot be instantiated, so it is likely that their subclasses will be implementing a significant portion of their actual functionality. This means that the subclasses likely allocate their own resources, and so it is useful to have polymorphism of the destructor.

7. 

