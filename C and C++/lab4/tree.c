#include <stdlib.h>
#include <stdio.h>
#include "tree.h"

Tree *empty = NULL;

/* BASE EXERCISE */

int tree_member(int x, Tree *tree)
{
  if (!tree)
  {
    return 0;
  }
  if (x == tree->value)
  {
    return 1;
  }
  if (x < tree->value)
  {
    return tree_member(x, tree->left);
  }
  return tree_member(x, tree->right);
}

Tree *tree_insert(int x, Tree *tree)
{
  if (!tree)
  {
    tree = malloc(sizeof(Tree));
    tree->value = x;
    return tree;
  }
  else if (x < tree->value)
  {
    tree->left = tree_insert(x, tree->left);
  }
  else if (x > tree->value)
  {
    tree->right = tree_insert(x, tree->right);
  }

  return tree;
}

void tree_free(Tree *tree)
{
  if (!tree) {
    return;
  }
  tree_free(tree->left);
  tree_free(tree->right);
  free(tree);
}

/* CHALLENGE EXERCISE */

void pop_minimum(Tree *tree, int *min, Tree **new_tree)
{
  /* TODO */
}

Tree *tree_remove(int x, Tree *tree)
{
  /* TODO */
  return empty;
}
