#include <stdio.h>
#include <stdlib.h>
#include "list.h"

List *cons(int head, List *tail)
{
  /* malloc() will be explained in the next lecture! */
  List *cell = malloc(sizeof(List));
  cell->head = head;
  cell->tail = tail;
  return cell;
}

/* Functions for you to implement */

int sum(List *list)
{
  int s = 0;
  for (List *i = list; i != NULL; i = i->tail)
  {
    s += i->head;
  }
  return s;
}

void iterate(int (*f)(int), List *list)
{
  for (List *i = list; i != NULL; i = i->tail)
  {
    i->head = f(i->head);
  }
}

void print_list(List *list)
{
  printf("[");
  for (List *i = list; i != NULL; i = i->tail)
  {
    printf("%d", i->head);
    if (i->tail != NULL)
    {
      printf(", ");
    }
  }
  printf("]\n");
}

/**** CHALLENGE PROBLEMS ****/

List *merge(List *list1, List *list2)
{
  if (list1 == NULL)
  {
    return list2;
  }
  if (list2 == NULL)
  {
    return list1;
  }
  if (list1->head < list2->head)
  {
    list1->tail = merge(list1->tail, list2);
    return list1;
  }
  list2->tail = merge(list1, list2->tail);
  return list2;
}

void split(List *list, List **list1, List **list2)
{
  if (list == NULL)
  {
    *list1 = NULL;
    *list2 = NULL;
    return;
  }
  *list1 = list;
  if (list->tail == NULL)
  {
    *list2 = NULL;
    return;
  }
  *list2 = list->tail;
  list = list->tail->tail;

  List *p1 = *list1;
  List *p2 = *list2;

  unsigned short int flag = 1;
  while (list != NULL)
  {
    if (flag)
    {
      p1 = (p1->tail = list);
    }
    else
    {
      p2 = (p2->tail = list);
    }
    list = list->tail;
    flag = flag ? 0 : 1;
  }
  p1->tail = NULL;
  p2->tail = NULL;
}

/* You get the mergesort implementation for free. But it won't
   work unless you implement merge() and split() first! */

List *mergesort(List *list)
{
  if (list == NULL || list->tail == NULL)
  {
    return list;
  }
  else
  {
    List *list1;
    List *list2;
    split(list, &list1, &list2);
    list1 = mergesort(list1);
    list2 = mergesort(list2);
    return merge(list1, list2);
  }
}
