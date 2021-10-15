# C & C++ Supervision 1

## Lecture 1

1. `'a'` is a char, whereas `"a"` is a string, which is a char array or char pointer.

2. This does always terminate. Even though we can't rely on `j` being initialised to 0, it will either be initialised to something greater than or equal to 5 in which case the program terminates immediately, or it will be less than 5 in which case it increments until it is 5, and then the program will terminate.

3.

```c
size_t n = sizeof(array)/sizeof(array[0]);
    
short unsigned int flag = 1;
while (flag) {
    flag = 0;
    for (int i=0; i<n-1; i++) {
        if (array[i] > array[i+1]) {
            int tmp = array[i];
            array[i] = array[i+1];
            array[i+1] = tmp;
            flag = 1;
        }
    }
}
```

4.

```c
size_t n = sizeof(array)/sizeof(array[0]);

short unsigned int flag = 1;
while (flag) {
    flag = 0;
    for (int i=0; i<n-1; i++) {
        int v1 = array[i] < 'a' ? array[i] + 32 : array[i];
        int v2 = array[i+1] < 'a' ? array[i+1] + 32 : array[i+1];
        if (v1 > v2) {
            int tmp = array[i];
            array[i] = array[i+1];
            array[i+1] = tmp;
            flag = 1;
        }
    }
}
```

## Lecture 2

1.

```c
int cntlower(char str[]) {
    int total = 0;
    for (int i=0; i<strlen(str); i++) {
        if (str[i] >= 'a' && str[i] <= 'z') {
            total++;
        } 
    }
    return total;
}
```

2. 

```c
void merge_sort(int array[], int start, int end) {
    if (start >= end - 1) return;
    
    int center = (start + end)/2;
    
    merge_sort(array, start, center);
    merge_sort(array, center, end);
    
    int buffer[end-start];
    
    int p1 = start;
    int p2 = center;
    int bi = 0;
    
    while (p1 < center && p2 < end) {
        if (array[p1] <= array[p2]) {
            buffer[bi++] = array[p1++];
        } else {
            buffer[bi++] = array[p2++];
        }
    }
    for (; p1 < center; p1++) {
        buffer[bi++] = array[p1];
    }
    for (; p2 < end; p2++) {
        buffer[bi++] = array[p2];
    }    
    for (int i=start; i<end; i++) {
        array[i] = buffer[i-start];
    }
}
```
My implementation uses `2n` memory.

3. `#define SWAP(t,x,y) t tmp = (x); y = (x); x = tmp`

4. No, as the `i++` expression is evaluated multiple times, in fact incrementing `i` by 3 by the end. Furthermore `f(x)` could be stateful and produce different results on different evaluations.

5. `#define SWAP(x,y) (x) += (y); (y) = (x)-(y); (x) -= (y)`

6. `*p` and `*q` are both zero.

## Lectures 3 & 4

1. `p[-2]` is the pointer to the item 2 before that pointed to by `p` where the item size is the size of the datatype pointed to. This is legal when `p` points to the 3<sup>rd</sup>-or-later element of an array.

2.

```c
const char *strfind(const char *needle, const char *hay) {
    for (int i=0; i<strlen(hay); i++) {
        if (*(hay+i) == *needle) {
            return hay+i;
        }
    }
    return NULL;
}
```

3.

```c
++p->i;                  // Advance p->i by sizeof(int)
p++->i;                  // Increment p by sizeof(struct data) and then access its i property
p--;                     // To avoid segfault
printf("%d\n", *p->i);   // Print the value pointed to by p->i
printf("%d\n", *p->i++); // Advance p->i by sizeof(int) and then print the value it pointed to originally
p->i -= 2;               // To avoid segfault;
(*p->i)++;               // Increment the value pointed to by p->i
printf("%d\n", *p++->i); // Increment p by sizeof(struct data) and print what its i property pointed to originally
```

4.
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int calc(int n, char *expressions[])
{

    int stack[n];
    int stack_pointer = -1;

    for (int i = 0; i < n; i++)
    {

        if (!strcmp(expressions[i], "+"))
        {
            int a = stack[stack_pointer--];
            stack[stack_pointer] += a;
        }
        else if (!strcmp(expressions[i], "x"))
        {
            int a = stack[stack_pointer--];
            stack[stack_pointer] *= a;
        }
        else
        {
            stack[++stack_pointer] = atoi(expressions[i]);
        }
    }

    return stack[stack_pointer];
}

int main(int argc, char *argv[])
{
    printf("%d\n", calc(argc - 1, argv + 1));
}
```

5.
    
    a. 1
    b. 4
    c. 4
    d. 5
    e. 8
    f. 8
    g. 8
    h. 80

6.

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{

    FILE *fp;

    fp = fopen(argv[1], "r");

    unsigned char c;
    unsigned char total = 0;

    while (1)
    {
        c = fgetc(fp);
        total += c;
        if (feof(fp))
        {
            break;
        }
    }
    fclose(fp);

    printf("%d\n", total);

    return 0;
}
```

7.

```c
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>

int main(int argc, char *argv[])
{

    unsigned char *file;
    unsigned char total = 0;

    int fd = open(argv[1], O_RDONLY);
    struct stat s;
    int status = fstat(fd, &s);
    int size = s.st_size;

    file = (char *) mmap(0, size, PROT_READ, MAP_PRIVATE, fd, 0);
    for (int i=0; i<size; i++) {
        total += (unsigned char) file[i];
    }

    printf("%d\n", total);

    return 0;
}
```

8.

    a. *(A+b)
    b. *(b+A)
    c. *(A+c)
    d. *((*(A+b)) + c)