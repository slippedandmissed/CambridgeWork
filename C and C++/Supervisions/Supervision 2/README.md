# C & C++ Supervision 2

## Lecture 5

1. 
    ,,,,,what

2. 
    When `char` fields are adjacent they are contiguous (e.g., they differ by 1 byte) however when an `int` follows a `char`, padding is inserted before the `int` to the nearest multiple of 4 bytes.

3. 
    gdb is able to access this information because it spawns the C program as a child process, and is therefore able to use a system call such as `ptrace` on linux in order to get information about the process..

    Large programs take a massive performance hit under valgrind because valgrind simulates the execution by interpreting the machine code instructions, rather than simply spawning the executable as a child process.

    ASan, MSan, and UBSan need access to the source code because they are compile-time tools, built in to the compiler. Valgrind on the other hand only needs the compiled binary because it simulates the program execution.

## Lectures 6 and 7

1. 

```c
struct tree {
    int *v;
    struct tree *left;
    struct tree *right;
};
typedef struct tree Tree;

void insert(int a, Tree *tree) {
    if (tree->v == NULL) {
        tree->v = malloc(sizeof(int));
        *(tree->v) = a;
    }
    else if (a < *(tree->v)) {
        if (tree->left == NULL) {
            tree->left = malloc(sizeof(Tree));
            tree->left->v = NULL;
            tree->left->left = NULL;
            tree->left->right = NULL;
        }
        insert(a, tree->left);
    } else {
        if (tree->right == NULL) {
            tree->right = malloc(sizeof(Tree));
            tree->right->v = NULL;
            tree->right->left = NULL;
            tree->right->right = NULL;
        }
        insert(a, tree->right);
    }
}

void heapify(int *a, int length, Tree *tree) {
    for (int i=0; i<length; i++) {
        insert(a[i], tree);
    }
}
```

2. 
    It could instead be represented by an array. This would be more memory efficient and also more time efficient because it removes the need to dereference long chains of pointers.

3. 
    `// TODO`

## Lecture 8

1. `// TODO`