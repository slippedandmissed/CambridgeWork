#include <ctype.h>
#include <string.h>
#include "revwords.h"

#define ALPHABETIC_CHARS "abcdefghijklmnopqrstuvwxyzABCDEFGHOJKLMNOPQRSTUVWXYZ"

void reverse_substring(char str[], int start, int end)
{
  for (int i = start, j = end; i < j; i++, j--)
  {
    char tmp = str[i];
    str[i] = str[j];
    str[j] = tmp;
  }
}

static short int is_word_char(char c)
{
  return strchr(ALPHABETIC_CHARS, c) == NULL ? 0 : 1;
}

int find_next_start(char str[], int len, int i)
{
  if ((i == 0 || !is_word_char(str[i - 1])) && is_word_char(str[i]))
  {
    return i;
  }
  short int outsideWord = 0;
  for (; i < len; i++)
  {
    if (!is_word_char(str[i]))
    {
      outsideWord = 1;
    }
    else if (outsideWord)
    {
      return i;
    }
  }
  return -1;
}

int find_next_end(char str[], int len, int i)
{
  if (is_word_char(str[i]))
  {
    for (; i < len; i++)
    {
      if (!is_word_char(str[i]))
      {
        return i - 1;
      }
    }
    return len-1;
  }
  else
  {
    int j = find_next_start(str, len, i);
    if (j == -1)
    {
      return -1;
    }
    return find_next_end(str, len, j);
  }
}

void reverse_words(char s[])
{
  int i=0;
  int len=strlen(s);
  while (i<len) {
    i = find_next_start(s, len, i);
    if (i == -1) {
      return;
    }
    int j = find_next_end(s, len, i);
    reverse_substring(s, i, j);
    i = j;
  }
}
