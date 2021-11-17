# C & C++ Supervision 3

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

```c
int process_file(char *name) {
    FILE *p = fopen(name, "r");
    if (p == NULL) return ERR_NOTFOUND;
    while (...) {
        ...
        if (...) {
            fclose(p);  // Prevent memory leak
            return ERR_MALFORMED;
        }
        process_one_option();
        ...
    }
    flose(p);
    return SUCCESS;
}
```

```c++
class File {
    FILE *p;

    public:
        bool file_found;

        File(char *name) {
            *p = fopen(name, "r");
            file_found = (p != NULL);
        }

        ~File() {
            if (file_found) {
                fclose(p);
            }
        }
}

int process_file(char *name) {
    File file(name);
    if (!file.file_found) return ERR_NOTFOUND;
    while (...) {
        ...
        if (...) return ERR_MALFORMED;
        process_one_option();
        ...
    }
    return SUCCESS;
}
```

8. 

```c++
template<typename T> T Stack<T>::pop() {
    if (index == -1) {
        cout << "Tried to pop from empty stack" << endl;
        exit(1);
    }
    return array[index--];
}

template<typename T> Stack<T>::~Stack() {
    free(array);
}
```

9. 

```c++
Stack(const Stack& s) {
    memcpy(array, s.array, s.capacity);
    capacity = s.capacity;
    index = s.index;
}

Stack& operator=(const Stack& s) {
    Stack n = malloc(sizeof(Stack));
    n.array = s.array;
    n.capacity = s.capacity;
    n.index = s.index;
    return n;
}

```

10. 

```c++
template <unsigned A, unsigned B> struct divides {
    static constexpr bool value = (A % B == 0);
}

template <unsigned A, unsigned B> struct dividesAny {
    static constexpr bool value = divides<A,B>::value || dividesAny<A, B-1>::value;
}


template <unsigned A, 2> struct dividesAny {
    static constexpr bool value = divides<A, 2>::value;
}

template <unsigned N> struct is_prime {
    static constexpr bool value = dividesAny<N, N-1>::value;
}
```

11. 

Have a large input to the implementation and observe that compilation is very slow but execution is very fast.
